import sys

from core.modules.main import main
from core.utils.logger import logger

log = logger()

try:
    main()
    sys.exit(0)
except Exception as exc:
    log.EXCEPTION(f"Falha na automação: {exc}")
    sys.exit(1)
