# {{ cookiecutter.automation_name }}

Ponto de entrada: `python bot.py`

## Setup

```powershell
copy .env.example .env
copy config\keys\account.env.example config\keys\account.env
copy config\keys\email.env.example config\keys\email.env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Fluxo em `core/modules/main.py`. Pandas em `core/modules/actions.py` (`tratar()`). Destinatários em `config/email.py`.
