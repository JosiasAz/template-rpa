import base64
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import smtplib

import config.config
from config.email import SUBJECT, TO_CC, TO_CC_TEST, TO_EMAIL, TO_EMAIL_TEST
from core.utils.logger import logger
from core.utils.template.html import render


def send_email(is_test, arquivos, title="", message="", details=None):
    return _enviar(is_test, arquivos, "sucesso", title, message, details)


def send_email_error(is_test, arquivos, title="", message="", details=None):
    b64 = ""
    for item in arquivos or []:
        path = Path(item)
        if path.is_file():
            b64 = base64.b64encode(path.read_bytes()).decode()
            break
    return _enviar(is_test, [], "erro", title, message, details, screenshot_b64=b64)


def _enviar(is_test, arquivos, status, title, message, details, screenshot_b64=""):
    log = logger()
    files = [Path(item) for item in (arquivos or [])]
    ok = Mailer(is_test=is_test).send(
        status=status,
        title=title,
        message=message,
        details=details,
        attachments=files,
        screenshot_b64=screenshot_b64,
    )
    if ok:
        log.OK("E-mail enviado")
    else:
        log.WARNING("E-mail não enviado")
    return ok


class Mailer:
    def __init__(self, is_test=False):
        self.is_test = is_test

    def send(self, status="sucesso", title="", message="", details=None, attachments=None, screenshot_b64=""):
        if not self.configured():
            return False

        try:
            html, images = render(status, title, message, details or {}, screenshot_b64)
            cfg = self._smtp()
            to = self._destinatarios()
            cc = self._valid(TO_CC_TEST if self.is_test else TO_CC)
            assunto = SUBJECT if status != "erro" else f"[ERRO] {SUBJECT}"
            msg = self._montar(
                html=html,
                texto=f"{title}\n\n{message}",
                images=images,
                attachments=attachments or [],
            )
            msg["From"] = cfg["user"]
            msg["To"] = ", ".join(to)
            if cc:
                msg["Cc"] = ", ".join(cc)
            msg["Subject"] = f"[TESTE] {assunto}" if self.is_test else assunto

            with smtplib.SMTP(cfg["host"], int(cfg["port"])) as server:
                server.starttls()
                if cfg["password"]:
                    server.login(cfg["user"], cfg["password"])
                server.send_message(msg)
            return True
        except Exception as exc:
            logger().ERROR(str(exc))
            return False

    def _montar(self, html, texto, images, attachments):
        related = MIMEMultipart("related")
        related.attach(MIMEText(html, "html", "utf-8"))
        for cid, (data, _filename) in images.items():
            image = MIMEImage(data, _subtype="png")
            if image.get("Content-Disposition"):
                del image["Content-Disposition"]
            if image.get("Content-ID"):
                del image["Content-ID"]
            image["Content-ID"] = f"<{cid}>"
            related.attach(image)

        alternative = MIMEMultipart("alternative")
        alternative.attach(MIMEText(texto, "plain", "utf-8"))
        alternative.attach(related)

        files = [Path(item) for item in attachments if Path(item).is_file()]
        if not files:
            return alternative

        mixed = MIMEMultipart("mixed")
        mixed.attach(alternative)
        for file in files:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read_bytes())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=file.name)
            mixed.attach(part)
        return mixed

    def configured(self):
        cfg = self._smtp()
        if not cfg["host"] or not cfg["port"] or not cfg["user"] or not cfg["password"]:
            return False
        return bool(self._destinatarios())

    def _destinatarios(self):
        return self._valid(TO_EMAIL_TEST if self.is_test else TO_EMAIL)

    def _valid(self, addresses):
        result = []
        for item in addresses:
            value = str(item).strip()
            if not value or value.isdigit():
                continue
            if "@" not in value or "." not in value.split("@")[-1]:
                continue
            result.append(value)
        return result

    def _smtp(self):
        return {
            "host": os.getenv("SMTP_SERVER") or "",
            "port": (os.getenv("SMTP_PORT") or "").strip(),
            "user": os.getenv("EMAIL") or "",
            "password": (os.getenv("SMTP_PASSWORD") or "").strip(),
        }
