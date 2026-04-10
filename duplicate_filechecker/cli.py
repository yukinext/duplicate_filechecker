from pathlib import Path

import typer

from .database import Database
from .hasher import Hasher
from .logger import Logger
from .merger import Merger
from .scanner import Scanner

app = typer.Typer()


@app.command()
def main(
    directory: str = typer.Argument(..., help="Directory to scan"),
    pattern: str = "*.mp4",
    trash_dir: str | None = None,
    merge: bool = False,
):
    if trash_dir is None:
        # Default: same level as directory, .dup_trash
        parent_dir = Path(directory).parent
        trash_dir = str(parent_dir / ".dup_trash")

    logger = Logger()
    scanner = Scanner()
    db = Database()
    hasher = Hasher(db)
    merger = Merger()

    # Scan files
    files = scanner.scan(directory, pattern)
    total_files = len(files)
    skipped = 0
    processed = 0

    hash_map = {}
    duplicates = {}

    for file_path in files:
        logger.log_file(file_path)
        try:
            hash_value = hasher.calculate_hash(file_path)
            processed += 1

            if hash_value in hash_map:
                if hash_value not in duplicates:
                    duplicates[hash_value] = [hash_map[hash_value]]
                duplicates[hash_value].append(file_path)
            else:
                hash_map[hash_value] = file_path
        except Exception as e:
            logger.logger.error(f"Error processing {file_path}: {e}")
            skipped += 1

    # Report
    unique_files = len(hash_map)

    logger.logger.info(f"探索したファイルの総数: {total_files}")
    logger.logger.info(f"スキップしたファイルの総数: {skipped}")
    logger.logger.info(f"今回処理したファイルの総数: {processed}")
    logger.logger.info(f"ユニークなファイルの総数: {unique_files}")

    moved = 0
    if merge:
        moved = merger.merge(duplicates, trash_dir)
        logger.logger.info(f"今回移動したファイルの総数: {moved}")

    logger.logger.info("処理が完了しました。")


if __name__ == "__main__":
    app()
