import pytest
import tempfile
import os
from duplicate_filechecker.hasher import Hasher
from duplicate_filechecker.database import Database

def test_calculate_hash():
    hasher = Hasher()
    # Create a test file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"test content")
        test_file = f.name
    
    try:
        hash_value, skipped = hasher.calculate_hash(test_file)
        assert isinstance(hash_value, str)
        assert len(hash_value) > 0
        assert skipped is False
    finally:
        os.unlink(test_file)

def test_hash_skip_if_cached(tmp_path):
    db_path = str(tmp_path / "test.db")
    db = Database(db_path)
    hasher = Hasher(db)
    
    # Create test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    
    # First call should calculate
    hash1, skipped1 = hasher.calculate_hash(str(test_file))
    # Second call should return cached
    hash2, skipped2 = hasher.calculate_hash(str(test_file))
    assert hash1 == hash2
    assert skipped1 is False
    assert skipped2 is True