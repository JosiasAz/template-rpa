import os
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from sqlalchemy import MetaData, Table, create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker
import config.config
from core.database.models import AUTOMATIC, TABLE_NAME, UNIQUE, UPLOAD_FILE, Base, Record
from core.utils.planilha import EXTS, ler
from core.utils.sanitizer import DataSanitizer
from core.utils.upsert import upsert as apply_upsert


class Database:
    def __init__(self):
        url = self._url(os.getenv("SESSION_CREDENTIAL"))
        if not url:
            raise ValueError("Preencha SESSION_CREDENTIAL em keys/account.env")
        self.engine = create_engine(url, pool_pre_ping=True)
        self._session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self._ensure_table()

    def session(self) -> Session:
        return self._session()

    def _ensure_table(self):
        if not inspect(self.engine).has_table(TABLE_NAME):
            Base.metadata.create_all(self.engine)

    def publish(self, folder=None, rows=None, files=None):
        if AUTOMATIC:
            if UPLOAD_FILE:
                self.save_files(files or self._files(folder))
            else:
                self.save_auto(folder)
            return
        if UPLOAD_FILE:
            self.save_files(files or self._files(folder))
            return
        if rows:
            self.save_rows(rows)

    def save_rows(self, rows, unique_by=None):
        payload = self._with_meta(rows)
        with self.session() as db:
            apply_upsert(db, Record, payload, unique_by or UNIQUE)
            db.commit()

    def save_files(self, files):
        rows = []
        for path in files or []:
            path = Path(path)
            if not path.is_file():
                continue
            content = path.read_bytes()
            rows.append(
                {
                    "HASH_UNIQUE": sha256(content).hexdigest(),
                    "FILE_NAME": path.name,
                    "FILE_CONTENT": content,
                    "LAST_UPDATE": datetime.now(),
                }
            )
        if rows:
            self.save_rows(rows)

    def save_auto(self, folder):
        planilha = self._planilha(folder)
        if planilha is None:
            return
        tabela = self._reflect()
        colunas = {c.lower(): c for c in tabela.columns.keys()}
        limpo = DataSanitizer().clean(self._ler(planilha))
        rows = []
        for item in limpo.to_dict(orient="records"):
            row = {}
            for key, value in item.items():
                real = colunas.get(str(key).lower())
                if real:
                    row[real] = value
            if not row:
                continue
            if "HASH_UNIQUE" in tabela.columns and "HASH_UNIQUE" not in row:
                row["HASH_UNIQUE"] = self._hash_row(row)
            if "LAST_UPDATE" in tabela.columns:
                row["LAST_UPDATE"] = datetime.now()
            rows.append(row)
        if not rows:
            return
        chave = [c for c in UNIQUE if c in tabela.columns] or [list(tabela.columns.keys())[0]]
        with self.session() as db:
            apply_upsert(db, tabela, rows, chave)
            db.commit()

    def _reflect(self):
        meta = MetaData()
        return Table(TABLE_NAME, meta, autoload_with=self.engine)

    def _hash_row(self, item):
        base = {k: v for k, v in item.items() if k not in ("HASH_UNIQUE", "LAST_UPDATE")}
        return sha256(repr(sorted(base.items())).encode()).hexdigest()

    def _with_meta(self, rows):
        now = datetime.now()
        payload = []
        for row in rows:
            item = dict(row)
            if "HASH_UNIQUE" not in item:
                item["HASH_UNIQUE"] = self._hash_row(item)
            item.setdefault("LAST_UPDATE", now)
            payload.append(item)
        return payload

    def _files(self, folder):
        if not folder:
            return []
        return [p for p in Path(folder).iterdir() if p.is_file()]

    def _planilha(self, folder):
        if not folder:
            return None
        for path in Path(folder).iterdir():
            if path.suffix.lower() in EXTS:
                return path
        return None

    def _ler(self, path):
        return ler(path)

    def _url(self, credential):
        value = (credential or "").strip()
        if not value or "://" not in value:
            return value
        head, rest = value.split("://", 1)
        if "+" not in head and ":" in head:
            driver, dialect = head.split(":", 1)
            return f"{dialect}+{driver}://{rest}"
        return value
