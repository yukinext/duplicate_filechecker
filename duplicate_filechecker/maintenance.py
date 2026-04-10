import csv
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class PurgeSummary:
    scanned: int
    purged: int
    failed: int


class PurgeAuditWriter:
    def __init__(self, output_path: str = "logs/purged_entry.csv"):
        self.output_path = Path(output_path)

    def append(self, file_path: str, hash_value: str):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        processed_at = datetime.now(UTC).isoformat()

        with self.output_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="\t", lineterminator="\n")
            writer.writerow([file_path, hash_value, processed_at])


class MaintenanceService:
    def __init__(self, db, logger, audit_writer: PurgeAuditWriter):
        self.db = db
        self.logger = logger
        self.audit_writer = audit_writer

    def purge_missing_entries(self) -> PurgeSummary:
        scanned = 0
        purged = 0
        failed = 0

        for file_path, hash_value in self.db.list_entries():
            scanned += 1
            try:
                if Path(file_path).exists():
                    continue

                self.db.delete_entry(file_path)
                self.audit_writer.append(file_path, hash_value)
                purged += 1
            except Exception as exc:
                failed += 1
                self.logger.logger.exception(f"Error purging entry path={file_path}: {exc}")

        return PurgeSummary(scanned=scanned, purged=purged, failed=failed)
