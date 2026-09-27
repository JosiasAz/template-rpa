import logging

from colorama import Fore, Style, init

from config.paths import LOG_FILE

init(autoreset=True)

ESTILO = {
    "START": (Fore.CYAN, "START"),
    "PASSO": (Fore.WHITE, "PASSO"),
    "OK": (Fore.GREEN, "OK"),
    "AGUARDE": (Fore.YELLOW, "....."),
    "AVISO": (Fore.YELLOW, "AVISO"),
    "ERRO": (Fore.RED, "ERRO"),
    "FIM": (Fore.CYAN, "FIM"),
    "VISAO": (Fore.MAGENTA, "VISAO"),
    "DEBUG": (Fore.CYAN, "DEBUG"),
    "INFO": (Fore.GREEN, "INFO"),
    "WARNING": (Fore.YELLOW, "AVISO"),
    "ERROR": (Fore.RED, "ERRO"),
    "CRITICAL": (Fore.RED, "ERRO"),
}


class TagFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "tag"):
            record.tag = "VISAO" if record.name.startswith("pyvizion") else record.levelname
        return True


class ColorFormatter(logging.Formatter):
    def format(self, record):
        cor, marca = ESTILO.get(record.tag, ESTILO.get(record.levelname, (Fore.WHITE, record.levelname)))
        hora = self.formatTime(record, "%H:%M:%S")
        return f"{cor}{hora}  {marca:<7} {record.getMessage()}{Style.RESET_ALL}"


class FileFormatter(logging.Formatter):
    def format(self, record):
        hora = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        tag = getattr(record, "tag", record.levelname)
        return f"{hora} | {tag:<7} | {record.getMessage()}"


class logger:
    """Log da automação: console colorido + output/logs/rpa.log."""

    _ready = False

    def __init__(self):
        self._logger = logging.getLogger("rpa")
        if not logger._ready:
            self._setup()
            logger._ready = True

    def _setup(self):
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        self._logger.setLevel(logging.INFO)
        self._logger.handlers.clear()
        self._logger.propagate = False

        filtro = TagFilter()
        arquivo = logging.FileHandler(LOG_FILE, encoding="utf-8")
        arquivo.setFormatter(FileFormatter())
        arquivo.addFilter(filtro)
        console = logging.StreamHandler()
        console.setFormatter(ColorFormatter())
        console.addFilter(filtro)
        self._logger.addHandler(arquivo)
        self._logger.addHandler(console)

        viz = logging.getLogger("pyvizion")
        viz.handlers.clear()
        viz.addHandler(arquivo)
        viz.addHandler(console)
        viz.setLevel(logging.INFO)
        viz.propagate = False

    def _emit(self, level, tag, message, *args):
        self._logger.log(level, message, *args, extra={"tag": tag})

    def START(self, message, *args):
        self._emit(logging.INFO, "START", message, *args)

    def STEP(self, message, *args):
        self._emit(logging.INFO, "PASSO", message, *args)

    def OK(self, message, *args):
        self._emit(logging.INFO, "OK", message, *args)

    def WAIT(self, message, *args):
        self._emit(logging.INFO, "AGUARDE", message, *args)

    def INFO(self, message, *args):
        self._emit(logging.INFO, "OK", message, *args)

    def WARNING(self, message, *args):
        self._emit(logging.WARNING, "AVISO", message, *args)

    def ERROR(self, message, *args):
        self._emit(logging.ERROR, "ERRO", message, *args)

    def EXCEPTION(self, message, *args):
        self._logger.exception(message, *args, extra={"tag": "ERRO"})

    def DEBUG(self, message, *args):
        self._emit(logging.DEBUG, "DEBUG", message, *args)

    def END(self, message, *args):
        self._emit(logging.INFO, "FIM", message, *args)
