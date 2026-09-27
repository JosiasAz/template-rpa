from core.utils.logger import logger
from core.utils.manager_path import PathManager
from core.utils.sanitizer import DataSanitizer

log = logger()
paths = PathManager()
sanitizer = DataSanitizer()


def ler_planilha(nome, pasta=None):
    """Lê o arquivo e devolve o DataFrame já tratado. No main, chame só isto."""
    log.STEP(f"Lendo planilha: {nome}")
    df = paths.planilha(nome, pasta)
    log.OK(f"{len(df)} linhas lidas")
    return tratar(df) # Retorna o DataFrame já tratado


def tratar(df):
    """Manipulação do DataFrame. Escreva o pandas aqui."""
    df = sanitizer.clean(df) # Limpa o DataFrame

    # --- personalize aqui ---
    # df = df.dropna(how="all")
    # df = df.rename(columns={})
    # df = df[["COLUNA_A", "COLUNA_B"]]

    return df
