import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:
    def __init__(self, log_file: str = "duplicate_checker.log"):
        self.logger = logging.getLogger("duplicate_checker")
        self.logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # Use logs directory for log file
        log_path = logs_dir / log_file

        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Rotating file handler for daily rotation with 7-day retention
        # maxBytes = 0 enables size-based rotation disabled, only daily rotation enabled
        file_handler = RotatingFileHandler(log_path, maxBytes=0, backupCount=7, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_file(self, file_path: str):
        self.logger.info(f"Processing file: {file_path}")

    def log_skip(self, skipped_file: str, stem_file: str):
        self.logger.info(f"Skipped file {skipped_file} (cached, stem: {stem_file})")

    def log_move(self, source_path: str, target_path: str, stem_path: str):
        self.logger.info(f"Moved duplicate file from {source_path} to {target_path} (stem: {stem_path})")

    def log_duration(self, duration: float):
        self.logger.info(f"Processing completed in {duration:.2f} seconds")
