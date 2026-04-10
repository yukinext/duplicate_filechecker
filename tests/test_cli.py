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