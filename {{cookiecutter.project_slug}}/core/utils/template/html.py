import base64
from datetime import datetime

from config.email import AUTOMATION_NAME
from core.utils.template.design import EmailDesign


def render(status, title, message, details, screenshot_b64=""):
    if status == "erro":
        return _erro(title, message, details or {}, screenshot_b64)
    return _sucesso(title, message, details or {})


def _logo(design, status="sucesso"):
    url = design.logo_error_url if status == "erro" else design.logo_success_url
    if not url:
        return "", {}
    html = (
        f'<img src="{url}" width="48" height="48" alt="RPA" '
        f'style="display:block;border:0;" />'
    )
    return html, {}


def _tabela(details, design):
    if not details:
        return ""

    rows = ""
    items = list(details.items())
    for index, (key, value) in enumerate(items):
        border = f"border-bottom:1px solid {design.line};" if index < len(items) - 1 else ""
        rows += (
            f'<tr>'
            f'<td style="padding:12px 0;{border}font-family:Arial,Helvetica,sans-serif;font-size:12px;letter-spacing:0.4px;text-transform:uppercase;color:{design.muted};width:38%;">{key}</td>'
            f'<td style="padding:12px 0;{border}font-family:Arial,Helvetica,sans-serif;font-size:14px;color:{design.text};font-weight:600;">{value}</td>'
            f"</tr>"
        )

    return (
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        f'style="margin-top:22px;border-collapse:collapse;">{rows}</table>'
    )


def _cabecalho(design, logo, badge, badge_bg, badge_fg="#07110A"):
    return f"""
        <tr><td style="height:3px;background:{design.brand};font-size:0;line-height:0;">&nbsp;</td></tr>
        <tr>
          <td style="background:{design.header};padding:22px 28px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td width="56" valign="middle">{logo}</td>
                <td valign="middle" style="padding-left:14px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:{design.text};font-weight:700;">{AUTOMATION_NAME}</td>
                <td valign="middle" align="right">
                  <span style="background:{badge_bg};color:{badge_fg};font-family:Arial,Helvetica,sans-serif;font-size:10px;font-weight:700;letter-spacing:1.2px;padding:7px 11px;">{badge}</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>
"""


def _sucesso(title, message, details):
    design = EmailDesign()
    logo, images = _logo(design, "sucesso")
    title = title or "Automação concluída"
    message = message or "O fluxo terminou sem erros. O arquivo segue em anexo, se houver."
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<body style="margin:0;padding:0;background:{design.page};">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{design.page};padding:32px 0;">
    <tr><td align="center">
      <table role="presentation" width="{design.width}" cellpadding="0" cellspacing="0" style="width:{design.width}px;background:{design.card};border:1px solid {design.line};">
        {_cabecalho(design, logo, "SUCESSO", design.brand)}
        <tr>
          <td style="padding:28px 28px 8px;font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:{design.brand};font-weight:700;">Relatório de execução</td>
        </tr>
        <tr>
          <td style="padding:4px 28px 10px;font-family:Arial,Helvetica,sans-serif;color:{design.text};font-size:22px;font-weight:700;line-height:30px;">{title}</td>
        </tr>
        <tr>
          <td style="padding:0 28px 18px;font-family:Arial,Helvetica,sans-serif;color:{design.muted};font-size:14px;line-height:22px;">{message}</td>
        </tr>
        <tr>
          <td style="padding:0 28px 28px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{design.brand_soft};border-left:3px solid {design.brand};">
              <tr>
                <td style="padding:12px 16px;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:{design.text};">Processamento finalizado com sucesso.</td>
              </tr>
            </table>
            {_tabela(details, design)}
            <p style="margin:22px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;color:{design.muted};">Enviado em {data}</p>
          </td>
        </tr>
        <tr>
          <td style="background:{design.footer};padding:16px 28px;font-family:Arial,Helvetica,sans-serif;font-size:11px;color:{design.muted};border-top:1px solid {design.line};">
            E-mail automático · {AUTOMATION_NAME}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""
    return html, images


def _erro(title, message, details, screenshot_b64=""):
    design = EmailDesign()
    logo, images = _logo(design, "erro")
    title = title or "Falha na automação"
    message = message or "O fluxo parou. O print da tela está abaixo. Log em output/logs/rpa.log."
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    foto = ""
    if screenshot_b64:
        cid = "print-erro@rpa.local"
        images[cid] = (base64.b64decode(screenshot_b64), "print_erro.png")
        foto = (
            f'<tr><td align="center" style="padding:4px 28px 20px;">'
            f'<img src="cid:{cid}" alt="Print do erro" '
            f'width="584" style="display:block;margin:0 auto;max-width:100%;height:auto;border:1px solid {design.line};" />'
            f"</td></tr>"
        )

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<body style="margin:0;padding:0;background:{design.page};">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{design.page};padding:32px 0;">
    <tr><td align="center">
      <table role="presentation" width="{design.width}" cellpadding="0" cellspacing="0" style="width:{design.width}px;background:{design.card};border:1px solid {design.line};">
        {_cabecalho(design, logo, "ERRO", design.error, "#FFFFFF")}
        <tr>
          <td style="padding:28px 28px 8px;font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:{design.error};font-weight:700;">Falha de execução</td>
        </tr>
        <tr>
          <td style="padding:4px 28px 10px;font-family:Arial,Helvetica,sans-serif;color:{design.text};font-size:22px;font-weight:700;line-height:30px;">{title}</td>
        </tr>
        <tr>
          <td style="padding:0 28px 18px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{design.error_soft};border-left:3px solid {design.error};">
              <tr>
                <td style="padding:12px 16px;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:22px;color:{design.text};">{message}</td>
              </tr>
            </table>
          </td>
        </tr>
        {foto}
        <tr>
          <td style="padding:0 28px 28px;">
            {_tabela(details, design)}
            <p style="margin:22px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;color:{design.muted};">Enviado em {data}</p>
          </td>
        </tr>
        <tr>
          <td style="background:{design.footer};padding:16px 28px;font-family:Arial,Helvetica,sans-serif;font-size:11px;color:{design.muted};border-top:1px solid {design.line};">
            Falha automática · {AUTOMATION_NAME}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""
    return html, images
