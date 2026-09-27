from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"


@dataclass
class EmailDesign:
    """Identidade visual preto e verde."""

    width: int = 640
    logo: Path = ASSETS / "happy_rpa.png"
    logo_success: Path = ASSETS / "happy_rpa.png"
    logo_error: Path = ASSETS / "sad_rpa.png"
    logo_success_url: str = "https://files.catbox.moe/v8l9o6.png"
    logo_error_url: str = "https://files.catbox.moe/4pinm0.png"

    page: str = "#070807"
    card: str = "#101211"
    header: str = "#0A0C0B"
    text: str = "#F2F5F3"
    muted: str = "#8B938C"
    line: str = "#222826"
    footer: str = "#0A0C0B"

    brand: str = "#1DB954"
    brand_dark: str = "#14863C"
    brand_soft: str = "#13261A"

    error: str = "#E24B4B"
    error_soft: str = "#2A1414"

    status: dict[str, str] | None = None

    def __post_init__(self) -> None:
        if self.status is None:
            self.status = {
                "sucesso": self.brand,
                "erro": self.error,
                "alerta": "#D4A017",
                "info": self.brand,
            }

    def color(self, status: str) -> str:
        return self.status.get(status, self.status["info"])
