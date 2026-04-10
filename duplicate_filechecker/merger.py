import shutil
import os
from pathlib import Path

class Merger:
    def merge(self, duplicates: dict[str, list[str]], trash_dir: str) -> int:
        moved_count = 0
        for files in duplicates.values():
            if len(files) > 1:
                # Sort and keep first (stem), move others (branches)
                sorted_files = sorted(files)
                stem = sorted_files[0]
                branches = sorted_files[1:]
                
                for branch in branches:
                    # Calculate relative path from original directory
                    # Assuming trash_dir is at same level as the directory containing the files
                    rel_path = os.path.relpath(branch, os.path.dirname(os.path.dirname(branch)))
                    target_path = os.path.join(trash_dir, rel_path)
                    
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.move(branch, target_path)
                    moved_count += 1
        
        return moved_count