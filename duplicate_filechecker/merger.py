import os
import shutil


class Merger:
    def merge(
        self,
        duplicates: dict[str, list[str]],
        trash_dir: str,
        source_dir: str,
        logger,
    ) -> int:
        moved_count = 0
        os.makedirs(trash_dir, exist_ok=True)
        source_root = os.path.abspath(source_dir)

        for files in duplicates.values():
            if len(files) > 1:
                sorted_files = sorted(files)
                stem = sorted_files[0]
                branches = sorted_files[1:]

                for branch in branches:
                    branch_path = os.path.abspath(branch)
                    rel_path = os.path.relpath(branch_path, source_root)
                    target_path = os.path.join(trash_dir, rel_path)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)

                    if os.path.exists(target_path):
                        logger.logger.info(f"Destination conflict: source={branch_path}, destination={target_path}")
                        target_path = self._get_unique_target_path(target_path)

                    shutil.move(branch_path, target_path)
                    moved_count += 1

        return moved_count

    def _get_unique_target_path(self, path: str) -> str:
        directory, filename = os.path.split(path)
        stem, ext = os.path.splitext(filename)
        index = 1
        candidate = os.path.join(directory, f"{stem}_{index}{ext}")

        while os.path.exists(candidate):
            index += 1
            candidate = os.path.join(directory, f"{stem}_{index}{ext}")

        return candidate
