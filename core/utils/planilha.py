from pathlib import Path

EXTS = {".xlsx", ".xlsm", ".xls", ".xlsb", ".csv", ".tsv"}


def resolver(nome, pasta):
    path = Path(nome)
    if not path.is_absolute():
        path = Path(pasta) / path
    return path


def ler(path):
    import pandas as pd

    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext == ".tsv":
        return pd.read_csv(path, sep="\t")
    if ext == ".xls":
        return pd.read_excel(path, engine="xlrd")
    if ext == ".xlsb":
        return pd.read_excel(path, engine="pyxlsb")
    return pd.read_excel(path)
