import fnmatch
import os


class Scanner:
    def scan(self, directory: str, pattern: str = "*.mp4") -> list[str]:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist")

        files = []
        # Recursively walk through directory
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                if fnmatch.fnmatch(filename, pattern):
                    files.append(os.path.join(root, filename))
        return sorted(files)
