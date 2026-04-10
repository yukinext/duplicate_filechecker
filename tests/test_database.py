import pytest
from duplicate_filechecker.database import Database

def test_save_and_get_hash(tmp_path):
    db_path = str(tmp_path / "test.db")
    db = Database(db_path)
    
    db.save("/path/to/file", "hash123")
    retrieved = db.get_hash("/path/to/file")
    assert retrieved == "hash123"
    
    assert db.get_hash("/nonexistent") is None