"""Limpa DataFrames de Excel/CSV antes do envio ao banco (to_sql / SQLAlchemy)."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
import re

import pandas as pd

_VAZIOS = {"", "nan", "nat", "none", "null", "n/a", "#n/a"}
_MOEDA_BR = re.compile(r"r\$|\d{1,3}(?:\.\d{3})+,\d{2}")


class DataSanitizer:
    """Sanitiza um DataFrame para upload em banco relacional.

    Parameters
    ----------
    id_columns :
        CPF, código de barras, IDs. Viram texto sem notação científica e sem ``.0``.
    money_columns :
        Valores em real (``R$ 1.250,50``). Viram ``Decimal`` com 2 casas.
    date_columns :
        Datas em formatos mistos. Perdem fuso horário.
    numeric_default :
        Se informado (``0`` ou ``0.0``), nulos em colunas numéricas/financeiras
        recebem esse valor. Se ``None``, o banco recebe NULL.
    """

    def __init__(
        self,
        id_columns=None,
        money_columns=None,
        date_columns=None,
        numeric_default=None,
    ):
        self.id_columns = list(id_columns or [])
        self.money_columns = list(money_columns or [])
        self.date_columns = list(date_columns or [])
        self.numeric_default = numeric_default

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Retorna cópia pronta para ``DataFrame.to_sql``."""
        out = df.copy()
        self._strip_texto(out)
        for col in self._existentes(out, self.id_columns):
            out[col] = out[col].map(self._como_id)
        money = self._existentes(out, self.money_columns) or self._detectar_moeda(out)
        for col in money:
            out[col] = out[col].map(self._como_decimal)
        for col in self._existentes(out, self.date_columns):
            out[col] = self._como_data(out[col])
        self._nulos(out, money)
        return out

    def _existentes(self, df, colunas):
        return [c for c in colunas if c in df.columns]

    def _strip_texto(self, df):
        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]) or df[col].dtype == object:
                df[col] = df[col].map(self._strip_celula)

    def _strip_celula(self, valor):
        if isinstance(valor, str):
            return valor.strip()
        return valor

    def _como_id(self, valor):
        if self._e_nulo(valor):
            return None
        if isinstance(valor, float):
            if valor.is_integer():
                return str(int(valor))
            return format(valor, "f").rstrip("0").rstrip(".")
        texto = str(valor).strip()
        if "e" in texto.lower():
            try:
                return str(int(Decimal(texto)))
            except (InvalidOperation, ValueError):
                return texto
        if texto.endswith(".0"):
            return texto[:-2]
        return texto

    def _como_decimal(self, valor):
        if self._e_nulo(valor):
            return self.numeric_default
        if isinstance(valor, (int, float, Decimal)) and not isinstance(valor, bool):
            numero = Decimal(str(valor))
        else:
            texto = re.sub(r"[rR\$\s]", "", str(valor).strip())
            if "," in texto and "." in texto:
                texto = texto.replace(".", "").replace(",", ".")
            elif "," in texto:
                texto = texto.replace(",", ".")
            try:
                numero = Decimal(texto)
            except InvalidOperation:
                return self.numeric_default
        return numero.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _como_data(self, serie):
        return serie.map(self._parse_data)

    def _parse_data(self, valor):
        if self._e_nulo(valor):
            return None
        data = pd.to_datetime(valor, format="mixed", dayfirst=True, errors="coerce")
        if pd.isna(data):
            return None
        if getattr(data, "tzinfo", None) is not None:
            return data.replace(tzinfo=None).to_pydatetime()
        return data.to_pydatetime() if hasattr(data, "to_pydatetime") else data

    def _detectar_moeda(self, df):
        achadas = []
        ids = set(self.id_columns)
        for col in df.columns:
            if col in ids or col in self.date_columns:
                continue
            amostra = df[col].dropna().astype(str).head(20)
            if amostra.map(lambda v: bool(_MOEDA_BR.search(v.lower()))).any():
                achadas.append(col)
        return achadas

    def _nulos(self, df, money_cols):
        numericas = set(money_cols)
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                numericas.add(col)

        for col in df.columns:
            valores = []
            for valor in df[col]:
                if self._e_nulo(valor):
                    valores.append(
                        self.numeric_default if col in numericas and self.numeric_default is not None else None
                    )
                else:
                    valores.append(valor)
            df[col] = pd.Series(valores, index=df.index, dtype=object)

    def _e_nulo(self, valor):
        if valor is None:
            return True
        try:
            if pd.isna(valor):
                return True
        except (TypeError, ValueError):
            pass
        if isinstance(valor, str) and valor.strip().lower() in _VAZIOS:
            return True
        return False
