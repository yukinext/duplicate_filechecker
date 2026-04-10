import logging
import sys
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

        # File handler
        file_handler = logging.FileHandler(log_path)
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
