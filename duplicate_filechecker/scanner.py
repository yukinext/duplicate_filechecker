import glob
import os
from pathlib import Path

class Scanner:
    def scan(self, directory: str, pattern: str = "*.mp4") -> list[str]:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist")
        
        path_pattern = os.path.join(directory, pattern)
        files = glob.glob(path_pattern)
        return sorted(files)