from datetime import datetime
from sqlalchemy import DateTime, Integer, LargeBinary, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


## AUTOMATIC:
AUTOMATIC = False
# True  = lê a tabela no banco e sobe o que estiver em rpa_output
# False = você personaliza o model e o que sobe

# UPLOAD_FILE:
UPLOAD_FILE = False
# True  = sobe arquivo (BLOB)
# False = sobe colunas da tabela

TABLE_NAME = "rpa_result"
UNIQUE = ["HASH_UNIQUE"]


class Base(DeclarativeBase):
    pass


class Record(Base):
    __tablename__ = TABLE_NAME

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HASH_UNIQUE: Mapped[str] = mapped_column(String(64), unique=True)

    # --- colunas da automação (personalize aqui) ---
    # NOME: Mapped[str] = mapped_column(String(200))
    # VALOR: Mapped[str] = mapped_column(String(50))

    FILE_NAME: Mapped[str | None] = mapped_column(String(255), nullable=True)
    FILE_CONTENT: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    LAST_UPDATE: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
