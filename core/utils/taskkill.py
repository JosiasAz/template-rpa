import csv
import subprocess
from io import StringIO

from core.utils.logger import logger

APPS = (
    "excel.exe",
    "chrome.exe",
    "msedge.exe",
    "firefox.exe",
    "chromedriver.exe",
    "msedgedriver.exe",
)


class TaskKiller:
    """Fecha só os processos que nasceram depois do início da automação."""

    def __init__(self, *names):
        self.apps = names or APPS
        self._antes = self._pids(self.apps)

    def close(self, *names):
        """Sem argumentos fecha os novos da lista. Com nome, fecha só esses novos."""
        log = logger()
        alvos = names or self.apps
        novos = self._pids(alvos) - self._antes
        if not novos:
            log.OK("Nenhum app aberto pela automação")
            return
        log.WAIT("Encerrando apps da automação...")
        for pid in novos:
            result = subprocess.run(
                ["taskkill", "/F", "/PID", str(pid)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                log.OK(f"Fechado PID {pid}")

    def _pids(self, names):
        found = set()
        for name in names:
            result = subprocess.run(
                ["tasklist", "/FI", f"IMAGENAME eq {name}", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                check=False,
                encoding="oem",
                errors="replace",
            )
            text = (result.stdout or "").strip()
            if not text or text.upper().startswith("INFO:"):
                continue
            for row in csv.reader(StringIO(text)):
                if len(row) >= 2 and row[1].isdigit():
                    found.add(int(row[1]))
        return found
