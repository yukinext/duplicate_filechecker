import pytest
from pathlib import Path
from duplicate_filechecker.scanner import Scanner


def test_scan_recursive_subdirectories(tmp_path):
    # Create nested directory structure with files
    (tmp_path / "level1").mkdir()
    (tmp_path / "level1" / "level2").mkdir()

    (tmp_path / "file1.mp4").touch()
    (tmp_path / "level1" / "file2.mp4").touch()
    (tmp_path / "level1" / "level2" / "file3.mp4").touch()
    (tmp_path / "file4.txt").touch()

    scanner = Scanner()
    files = scanner.scan(str(tmp_path), "*.mp4")

    assert len(files) == 3
    assert str(tmp_path / "file1.mp4") in files
    assert str(tmp_path / "level1" / "file2.mp4") in files
    assert str(tmp_path / "level1" / "level2" / "file3.mp4") in files
    assert str(tmp_path / "file4.txt") not in files


def test_scan_deep_nesting(tmp_path):
    # Create deeply nested structure
    deep_path = tmp_path
    for i in range(5):
        deep_path = deep_path / f"dir{i}"
        deep_path.mkdir()

    (deep_path / "deep_file.mp4").touch()

    scanner = Scanner()
    files = scanner.scan(str(tmp_path), "*.mp4")

    assert len(files) == 1
    assert "deep_file.mp4" in files[0]


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