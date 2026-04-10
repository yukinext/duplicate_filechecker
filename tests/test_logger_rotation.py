import logging
import time
from pathlib import Path
from logging.handlers import RotatingFileHandler
from duplicate_filechecker.logger import Logger


def test_logger_creates_logs_directory(tmp_path, monkeypatch):
    # Change to temp directory
    monkeypatch.chdir(tmp_path)

    logger = Logger("test.log")

    assert (tmp_path / "logs").exists()
    assert (tmp_path / "logs" / "test.log").exists()


def test_logger_rotating_file_handler(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    logger = Logger("rotating_test.log")

    # Check that file handler is RotatingFileHandler
    file_handlers = [h for h in logger.logger.handlers if isinstance(h, RotatingFileHandler)]
    assert len(file_handlers) > 0

    handler = file_handlers[0]
    assert handler.backupCount == 7
    assert handler.maxBytes == 0


def test_logger_outputs_to_file_and_console(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    logger = Logger("output_test.log")
    logger.log_file("/path/to/test.mp4")

    # Check console output
    captured = capsys.readouterr()
    assert "Processing file" in captured.out

    # Check file output
    log_file = tmp_path / "logs" / "output_test.log"
    assert log_file.exists()
    content = log_file.read_text()
    assert "Processing file" in content
