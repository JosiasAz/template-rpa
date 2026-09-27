# Template RPA

Base reutilizável em Python para novas automações: planilha, desktop, web, banco e e-mail de status.

**Autor:** Josias Azevedo da Silva  
**Licença:** MIT

---

## Tecnologias

| Camada | Stack |
|--------|--------|
| Linguagem | Python 3 |
| Visão / desktop | PyVizion, PyAutoGUI, Tesseract |
| Web | Selenium |
| Dados | Pandas, OpenPyXL, xlrd, pyxlsb |
| Banco | SQLAlchemy, PostgreSQL, MySQL |
| E-mail | SMTP (Gmail), HTML corporativo |
| Configuração | python-dotenv |

---

## Árvore do projeto

```
template-rpa/
├── bot.py                      # ponto de entrada
├── requirements.txt
├── .env / .env.example
├── config/
│   ├── config.py               # IS_TEST, Vizion, credenciais
│   ├── email.py                # nome, assunto, destinatários
│   ├── paths.py                # output, screenshots, Documents/rpa_output
│   └── keys/
│       ├── account.env.example
│       └── email.env.example
├── core/
│   ├── modules/
│   │   ├── main.py             # fluxo da automação
│   │   └── actions.py          # ler_planilha() + tratar()
│   ├── database/               # models + publish / upsert
│   └── utils/
│       ├── logger.py
│       ├── manager_path.py
│       ├── web.py
│       ├── desktop.py
│       ├── taskkill.py
│       └── template/           # e-mail sucesso / erro
├── resources/                  # imagens do Vizion
└── output/
    ├── logs/
    └── screenshots/
```

Planilhas de entrada: `Documents/rpa_output`.

Nome e assunto da automação ficam só em `config/email.py`.

---

## O que este template melhora

- **Um único ponto de escrita** — o fluxo fica em `main()`; pandas em `tratar()`.
- **Falhas visíveis** — log colorido, print da tela e e-mail de erro.
- **E-mail corporativo** — sucesso e erro no mesmo visual (preto e verde), sem anexo fantasma do logo.
- **Encerramento limpo** — o `TaskKiller` fecha só o que a automação abriu.
- **Banco pronto** — upsert com chave única, modo automático ou colunas personalizadas.
- **Projeto novo em um comando** — clone o repositório ou use Cookiecutter.

### Git clone (projeto pronto)

```powershell
git clone https://github.com/JosiasAz/template-rpa.git
cd template-rpa
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python bot.py
```

### Cookiecutter (gera pasta com o nome do RPA)

```powershell
pip install cookiecutter
cookiecutter gh:JosiasAz/template-rpa --checkout cookiecutter
```

---

**Josias Azevedo da Silva** · [MIT License](LICENSE)
