import time
from pathlib import Path
from unittest.mock import patch
from duplicate_filechecker.cli import main


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
            main(str(test_dir), merge=True)

            # Check that log_duration was called with 5.5
            mock_logger.log_duration.assert_called_once_with(5.5)


def test_maintenance_purge_missing_command_runs_service(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    db_path = tmp_path / "maintenance.db"

    with patch("duplicate_filechecker.cli.MaintenanceService") as mock_service_class:
        mock_service = mock_service_class.return_value
        mock_service.purge_missing_entries.return_value = type(
            "Summary", (), {"scanned": 3, "purged": 1, "failed": 0}
        )()

        from duplicate_filechecker.cli import maintenance_purge_missing

        maintenance_purge_missing(str(db_path))

        mock_service.purge_missing_entries.assert_called_once()