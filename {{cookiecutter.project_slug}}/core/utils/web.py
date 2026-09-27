from __future__ import annotations
import time
from pathlib import Path
from typing import Literal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = Literal["id", "name", "xpath", "css", "class", "tag", "link", "partial_link"]

_BY: dict[str, str] = {
    "id": By.ID,
    "name": By.NAME,
    "xpath": By.XPATH,
    "css": By.CSS_SELECTOR,
    "class": By.CLASS_NAME,
    "tag": By.TAG_NAME,
    "link": By.LINK_TEXT,
    "partial_link": By.PARTIAL_LINK_TEXT,
}


class Web:
    """Automação de navegador com Selenium."""

    def __init__(self, *, headless: bool = False, timeout: float = 15.0) -> None:
        self.timeout = timeout
        self.headless = headless
        self.driver: WebDriver | None = None

    def _browser(self) -> WebDriver:
        if self.driver is None:
            options = Options()
            options.add_argument("--start-maximized")
            if self.headless:
                options.add_argument("--headless=new")
            self.driver = webdriver.Chrome(options=options)
        return self.driver

    def __enter__(self) -> Web:
        return self

    def __exit__(self, *_: object) -> None:
        self.quit()

    def open(self, url: str) -> None:
        self._browser().get(url)

    def find(self, by: Locator, value: str) -> WebElement:
        return WebDriverWait(self._browser(), self.timeout).until(
            EC.presence_of_element_located((_BY[by], value))
        )

    def click(self, by: Locator, value: str) -> None:
        WebDriverWait(self._browser(), self.timeout).until(
            EC.element_to_be_clickable((_BY[by], value))
        ).click()

    def type(self, by: Locator, value: str, text: str, *, clear: bool = True) -> None:
        field = self.find(by, value)
        if clear:
            field.clear()
        field.send_keys(text)

    def text(self, by: Locator, value: str) -> str:
        return self.find(by, value).text

    def wait(self, seconds: float) -> None:
        time.sleep(seconds)

    def screenshot(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._browser().save_screenshot(str(path))
        return path

    @property
    def url(self) -> str:
        return self._browser().current_url

    @property
    def title(self) -> str:
        return self._browser().title

    def quit(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None
