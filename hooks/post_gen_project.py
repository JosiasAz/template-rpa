from pathlib import Path

env = Path(".env")
if not env.exists():
    env.write_text("IS_TEST={{ cookiecutter.is_test }}\n", encoding="utf-8")

for folder in ("output/logs", "output/screenshots", "resources"):
    Path(folder).mkdir(parents=True, exist_ok=True)
