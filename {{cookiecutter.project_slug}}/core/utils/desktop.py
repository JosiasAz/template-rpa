from __future__ import annotations

from pathlib import Path

import pyautogui
import pyperclip


class Desktop:
    """Automação de tela com PyAutoGUI."""

    def __init__(self, *, timeout: float = 15.0, pause: float = 0.3) -> None:
        self.timeout = timeout
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = pause

    def click(self, x: int, y: int, clicks: int = 1, button: str = "left") -> None:
        pyautogui.click(x, y, clicks=clicks, button=button)

    def double_click(self, x: int, y: int) -> None:
        pyautogui.doubleClick(x, y)

    def right_click(self, x: int, y: int) -> None:
        pyautogui.rightClick(x, y)

    def move_to(self, x: int, y: int, duration: float = 0.2) -> None:
        pyautogui.moveTo(x, y, duration=duration)

    def scroll(self, clicks: int) -> None:
        pyautogui.scroll(clicks)

    def type_text(self, text: str, *, interval: float = 0.02) -> None:
        pyautogui.write(text, interval=interval)

    def paste(self, text: str) -> None:
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")

    def hotkey(self, *keys: str) -> None:
        pyautogui.hotkey(*keys)

    def press(self, key: str) -> None:
        pyautogui.press(key)

    def locate_image(
        self,
        image: str | Path,
        *,
        confidence: float = 0.8,
    ) -> pyautogui.Point | None:
        box = pyautogui.locateOnScreen(str(image), confidence=confidence)
        return pyautogui.center(box) if box else None

    def click_image(
        self,
        image: str | Path,
        *,
        confidence: float = 0.8,
        timeout: float | None = None,
    ) -> bool:
        point = self.wait_image(image, confidence=confidence, timeout=timeout)
        if point is None:
            return False
        pyautogui.click(point)
        return True

    def wait_image(
        self,
        image: str | Path,
        *,
        confidence: float = 0.8,
        timeout: float | None = None,
    ) -> pyautogui.Point | None:
        import time

        deadline = time.monotonic() + (timeout if timeout is not None else self.timeout)
        while time.monotonic() < deadline:
            point = self.locate_image(image, confidence=confidence)
            if point is not None:
                return point
            time.sleep(0.4)
        return None

    def screenshot(self, path: Path, region: tuple[int, int, int, int] | None = None) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        pyautogui.screenshot(str(path), region=region)
        return path
