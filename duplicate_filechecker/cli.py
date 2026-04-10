import time
from pathlib import Path

import typer

from .database import Database
from .hasher import Hasher
from .logger import Logger
from .maintenance import MaintenanceService, PurgeAuditWriter
from .merger import Merger
from .scanner import Scanner

app = typer.Typer()
maint_app = typer.Typer()
app.add_typer(maint_app, name="maint")


@app.command("check")
def check(
    directory: str = typer.Argument(..., help="Directory to scan"),
    pattern: str = "*.mp4",
    trash_dir: str | None = None,
    merge: bool = False,
):
    start_time = time.time()

    if trash_dir is None:
        # Default: append .dup_trash to the source directory path
        trash_dir = str(Path(directory).with_name(Path(directory).name + ".dup_trash"))

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
            hash_value, skipped_by_cache = hasher.calculate_hash(file_path)
            if skipped_by_cache:
                skipped += 1
                stem_file = db.get_stem_file(hash_value) or "unknown"
                logger.log_skip(file_path, stem_file)
            else:
                processed += 1

            if hash_value in hash_map:
                if hash_value not in duplicates:
                    duplicates[hash_value] = [hash_map[hash_value]]
                duplicates[hash_value].append(file_path)
            else:
                hash_map[hash_value] = file_path
        except Exception:
            logger.logger.exception(f"Error processing {file_path}")
            skipped += 1

    # Report
    unique_files = len(hash_map)

    logger.logger.info(f"探索したファイルの総数: {total_files}")
    logger.logger.info(f"スキップしたファイルの総数: {skipped}")
    logger.logger.info(f"今回処理したファイルの総数: {processed}")
    logger.logger.info(f"ユニークなファイルの総数: {unique_files}")

    moved = 0
    if merge:
        moved = merger.merge(duplicates, trash_dir, directory, logger)
        logger.logger.info(f"今回移動したファイルの総数: {moved}")

    duration = time.time() - start_time
    logger.log_duration(duration)

    logger.logger.info("処理が完了しました。")


@maint_app.command("purge-missing")
def maint_purge_missing(db_path: str = "duplicates.db"):
    logger = Logger()
    db = Database(db_path)
    service = MaintenanceService(db=db, logger=logger, audit_writer=PurgeAuditWriter())
    summary = service.purge_missing_entries()

    logger.logger.info(f"メンテナンス完了: scanned={summary.scanned}, purged={summary.purged}, failed={summary.failed}")


def main(
    directory: str,
    pattern: str = "*.mp4",
    trash_dir: str | None = None,
    merge: bool = False,
):
    # Backward compatible call path for direct function usage in existing tests/tools.
    check(directory=directory, pattern=pattern, trash_dir=trash_dir, merge=merge)


if __name__ == "__main__":
    app()
