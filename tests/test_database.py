import pytest
from duplicate_filechecker.database import Database

def test_save_and_get_hash(tmp_path):
    db_path = str(tmp_path / "test.db")
    db = Database(db_path)
    
    db.save("/path/to/file", "hash123")
    retrieved = db.get_hash("/path/to/file")
    assert retrieved == "hash123"
    
    assert db.get_hash("/nonexistent") is None


def test_list_entries_returns_all_rows(tmp_path):
    db_path = str(tmp_path / "test.db")
    db = Database(db_path)

    db.save("/path/to/file1", "hash1")
    db.save("/path/to/file2", "hash2")

    entries = db.list_entries()

    assert ("/path/to/file1", "hash1") in entries
    assert ("/path/to/file2", "hash2") in entries


def test_delete_entry_removes_only_target_row(tmp_path):
    db_path = str(tmp_path / "test.db")
    db = Database(db_path)

    db.save("/path/to/file1", "hash1")
    db.save("/path/to/file2", "hash2")

    db.delete_entry("/path/to/file1")

    assert db.get_hash("/path/to/file1") is None
    assert db.get_hash("/path/to/file2") == "hash2"