from pathlib import Path
from unittest.mock import MagicMock

from duplicate_filechecker.database import Database
from duplicate_filechecker.maintenance import MaintenanceService, PurgeAuditWriter


def test_maintenance_purges_missing_and_writes_audit(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    existing = tmp_path / "exists.mp4"
    existing.write_text("ok")
    missing = tmp_path / "missing.mp4"

    db = Database(str(tmp_path / "test.db"))
    db.save(str(existing), "hash_exists")
    db.save(str(missing), "hash_missing")

    logger = MagicMock()
    logger.logger = MagicMock()

    writer = PurgeAuditWriter("logs/purged_entry.csv")
    service = MaintenanceService(db=db, logger=logger, audit_writer=writer)

    summary = service.purge_missing_entries()

    assert summary.scanned == 2
    assert summary.purged == 1
    assert summary.failed == 0
    assert db.get_hash(str(existing)) == "hash_exists"
    assert db.get_hash(str(missing)) is None

    audit_path = tmp_path / "logs" / "purged_entry.csv"
    assert audit_path.exists()
    row = audit_path.read_text(encoding="utf-8").strip().split("\t")
    assert row[0] == str(missing)
    assert row[1] == "hash_missing"
    assert "T" in row[2]
    assert row[2].endswith("+00:00")


def test_maintenance_continues_when_delete_entry_fails(tmp_path):
    logger = MagicMock()
    logger.logger = MagicMock()

    class FakeDb:
        def list_entries(self):
            return [
                (str(tmp_path / "missing1.mp4"), "h1"),
                (str(tmp_path / "missing2.mp4"), "h2"),
            ]

        def delete_entry(self, file_path: str):
            if file_path.endswith("missing1.mp4"):
                raise RuntimeError("boom")

    writer = MagicMock()
    service = MaintenanceService(db=FakeDb(), logger=logger, audit_writer=writer)

    summary = service.purge_missing_entries()

    assert summary.scanned == 2
    assert summary.purged == 1
    assert summary.failed == 1
    logger.logger.exception.assert_called()


def test_purge_audit_writer_creates_logs_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    writer = PurgeAuditWriter("logs/purged_entry.csv")
    writer.append("/tmp/a.mp4", "hash")

    assert (tmp_path / "logs" / "purged_entry.csv").exists()
