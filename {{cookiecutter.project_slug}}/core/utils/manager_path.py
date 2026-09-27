from __future__ import annotations

import shutil
from pathlib import Path

from config.paths import RPA_OUTPUT
from core.utils.planilha import EXTS, ler, resolver


class PathManager:
    """Pastas e arquivos da automação."""

    def __init__(self):
        self.rpa_output = RPA_OUTPUT

    def create(self, path):
        folder = Path(path)
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def delete(self, path):
        folder = Path(path)
        if folder.is_dir():
            shutil.rmtree(folder)

    def recreate(self, path):
        self.delete(path)
        return self.create(path)

    def clear(self, path):
        folder = Path(path)
        if folder.is_dir():
            for item in folder.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        return self.create(folder)

    def delete_file(self, path):
        file = Path(path)
        if file.is_file():
            file.unlink()

    def files(self, path, pattern="*"):
        folder = Path(path)
        if not folder.is_dir():
            return []
        return sorted(item for item in folder.glob(pattern) if item.is_file())

    def folders(self, path):
        folder = Path(path)
        if not folder.is_dir():
            return []
        return sorted(item for item in folder.iterdir() if item.is_dir())

    def latest(self, path, pattern="*"):
        items = self.files(path, pattern)
        return max(items, key=lambda item: item.stat().st_mtime) if items else None

    def copy(self, source, destination):
        dest = Path(destination)
        dest.parent.mkdir(parents=True, exist_ok=True)
        return Path(shutil.copy2(source, dest))

    def move(self, source, destination):
        dest = Path(destination)
        dest.parent.mkdir(parents=True, exist_ok=True)
        return Path(shutil.move(str(source), str(dest)))

    def planilha(self, nome, pasta=None):
        """Lê csv/tsv/xls/xlsx/xlsm/xlsb em Documents/rpa_output. Nome ou caminho absoluto."""
        path = resolver(nome, pasta or self.rpa_output)
        if not path.is_file():
            raise FileNotFoundError(f"Planilha não encontrada: {path}")
        if path.suffix.lower() not in EXTS:
            raise ValueError(f"Formato não suportado: {path.suffix}")
        return ler(path)
