import os
from dotenv import load_dotenv
from config.paths import RESOURCES_DIR, SCREENSHOTS_DIR

load_dotenv(".env")
load_dotenv("config/keys/account.env")
load_dotenv("config/keys/email.env")

IS_TEST = os.getenv("IS_TEST", "1") == "1"
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SESSION_CREDENTIAL = os.getenv("SESSION_CREDENTIAL")

EMAIL = os.getenv("EMAIL")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


VIZION = {
    "image_folders": [str(RESOURCES_DIR)],
    "tesseract_lang": "por",
    "confidence_threshold": 75,
    "show_overlay": False,
    "save_failure_screenshots": True,
    "failure_screenshot_dir": str(SCREENSHOTS_DIR),
}
