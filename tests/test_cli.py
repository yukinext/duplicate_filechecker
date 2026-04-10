import time
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from duplicate_filechecker.cli import app, check

runner = CliRunner()


def test_cli_logs_duration(tmp_path, monkeypatch):
    # Create test directory with duplicate files
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    # Create duplicate files
    file1 = test_dir / "file1.mp4"
    file2 = test_dir / "file2.mp4"
    file1.write_text("content")
    file2.write_text("content")

    monkeypatch.chdir(tmp_path)

    # Mock time to control duration
    with patch('time.time') as mock_time:
        mock_time.side_effect = [0.0, 5.5]  # start at 0, end at 5.5

        with patch('duplicate_filechecker.cli.Logger') as mock_logger_class:
            mock_logger = mock_logger_class.return_value
            check(str(test_dir), merge=True)

            # Check that log_duration was called with 5.5
            mock_logger.log_duration.assert_called_once_with(5.5)


def test_maint_purge_missing_subcommand_runs_service(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    db_path = tmp_path / "maintenance.db"

    with patch("duplicate_filechecker.cli.MaintenanceService") as mock_service_class:
        mock_service = mock_service_class.return_value
        mock_service.purge_missing_entries.return_value = type(
            "Summary", (), {"scanned": 3, "purged": 1, "failed": 0}
        )()

        result = runner.invoke(app, ["maint", "purge-missing", "--db-path", str(db_path)])

        assert result.exit_code == 0
        mock_service.purge_missing_entries.assert_called_once()


def test_check_subcommand_invokes_duplicate_check_flow(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    test_dir = tmp_path / "target"
    test_dir.mkdir()
    (test_dir / "a.mp4").write_text("same")
    (test_dir / "b.mp4").write_text("same")

    with patch("duplicate_filechecker.cli.Logger") as mock_logger_class:
        mock_logger = mock_logger_class.return_value
        result = runner.invoke(app, ["check", str(test_dir)])

    assert result.exit_code == 0
    assert mock_logger.log_file.called