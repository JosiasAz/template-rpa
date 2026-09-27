from pyvizion import Vizion

from config.config import IS_TEST, VIZION
from config.email import AUTOMATION_NAME
from config.paths import RPA_OUTPUT, SCREENSHOTS_DIR
from core.utils.logger import logger
from core.utils.manager_path import PathManager
from core.utils.taskkill import TaskKiller
# from core.database import Database
# from core.modules.actions import ler_planilha
# from core.utils.desktop import Desktop
# from core.utils.template import send_email, send_email_error
# from core.utils.web import Web

killer = TaskKiller()
paths = PathManager()
log = logger()
bot = Vizion(config=VIZION)
# desk = Desktop()
# web = Web()
# db = Database()


def main():
    log.START(AUTOMATION_NAME)
    paths.create(RPA_OUTPUT)
    paths.clear(SCREENSHOTS_DIR)

    try:
        """digite seu codigo aqui"""

        # web.open("https://exemplo.com")
        # desk.click_image("botao.png")

        # df = ler_planilha("arquivo.xlsx")
        # db.publish(rows=df.to_dict(orient="records"))

        # send_email(is_test=IS_TEST, arquivos=[RPA_OUTPUT / "arquivo.xlsx"])
        pass

    except Exception as e:
        log.EXCEPTION(f"Erro na automação: {e}")
        bot.screenshot(str(SCREENSHOTS_DIR / "falha.png"))
        # send_email_error(is_test=IS_TEST, arquivos=[SCREENSHOTS_DIR / "falha.png"])
        raise

    finally:
        killer.close()
        log.END(AUTOMATION_NAME)
