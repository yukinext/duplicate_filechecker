import runpy
from pathlib import Path
from unittest.mock import patch


def test_main_py_always_delegates_to_typer_app(monkeypatch):
    repo_root = Path(__file__).resolve().parent.parent
    script = repo_root / "main.py"

    monkeypatch.setattr("sys.argv", ["main.py", "maint", "purge-missing", "--db-path", "custom.db"])

    with patch("duplicate_filechecker.cli.app") as mock_app:
        runpy.run_path(str(script), run_name="__main__")

    mock_app.assert_called_once()


def test_main_py_uses_existing_app_for_normal_mode(monkeypatch):
    repo_root = Path(__file__).resolve().parent.parent
    script = repo_root / "main.py"

    monkeypatch.setattr("sys.argv", ["main.py", "/tmp/target"])

    with patch("duplicate_filechecker.cli.app") as mock_app:
        runpy.run_path(str(script), run_name="__main__")

    mock_app.assert_called_once()
