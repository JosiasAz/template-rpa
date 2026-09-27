# Template RPA

Gere um projeto novo:

```powershell
pip install cookiecutter
cookiecutter gh:JosiasAz/template-rpa
```

O gerador pergunta empresa, nome do RPA e e-mails.

```powershell
cd nome-do-projeto
copy .env.example .env
copy config\keys\account.env.example config\keys\account.env
copy config\keys\email.env.example config\keys\email.env
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python bot.py
```

Autor: Josias Azevedo da Silva · MIT
