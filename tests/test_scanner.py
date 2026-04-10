import pytest
from pathlib import Path
from duplicate_filechecker.scanner import Scanner

def test_scan_existing_directory(tmp_path):
    # Create test files
    (tmp_path / "file1.mp4").touch()
    (tmp_path / "file2.mp4").touch()
    (tmp_path / "file3.txt").touch()
    
    scanner = Scanner()
    files = scanner.scan(str(tmp_path), "*.mp4")
    
    assert len(files) == 2
    assert str(tmp_path / "file1.mp4") in files
    assert str(tmp_path / "file2.mp4") in files
    assert str(tmp_path / "file3.txt") not in files

def test_scan_nonexistent_directory():
    scanner = Scanner()
    with pytest.raises(FileNotFoundError):
        scanner.scan("/nonexistent", "*.mp4")

def test_scan_default_pattern(tmp_path):
    (tmp_path / "file1.mp4").touch()
    (tmp_path / "file2.mp4").touch()
    
    scanner = Scanner()
    files = scanner.scan(str(tmp_path))  # No pattern specified
    
    assert len(files) == 2