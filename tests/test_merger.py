import os
from pathlib import Path

from duplicate_filechecker.logger import Logger
from duplicate_filechecker.merger import Merger


def test_merger_creates_trash_dir_if_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    source_dir = tmp_path / "target_dir"
    source_dir.mkdir()
    (source_dir / "file1.mp4").write_text("file1")
    (source_dir / "file2.mp4").write_text("file2")

    trash_dir = source_dir.with_name(source_dir.name + ".dup_trash")
    assert not trash_dir.exists()

    merger = Merger()
    logger = Logger("merger_test.log")
    duplicates = {"hash1": [str(source_dir / "file1.mp4"), str(source_dir / "file2.mp4")]}

    moved = merger.merge(duplicates, str(trash_dir), str(source_dir), logger)

    assert moved == 1
    assert trash_dir.exists()
    assert (trash_dir / "file2.mp4").exists()
    assert not (source_dir / "file2.mp4").exists()


def test_merger_renames_conflicting_file(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    source_dir = tmp_path / "target_dir"
    branch_dir = source_dir / "foo"
    branch_dir.mkdir(parents=True)

    stem = branch_dir / "john.mp4"
    stem.write_text("stem")
    branch = branch_dir / "john_branch.mp4"
    branch.write_text("branch")

    trash_dir = source_dir.with_name(source_dir.name + ".dup_trash")
    existing_target_dir = trash_dir / "foo"
    existing_target_dir.mkdir(parents=True)
    (existing_target_dir / "john.mp4").write_text("existing")

    merger = Merger()
    logger = Logger("merger_conflict.log")
    duplicates = {"hash1": [str(stem), str(branch)]}

    moved = merger.merge(duplicates, str(trash_dir), str(source_dir), logger)

    assert moved == 1
    assert (existing_target_dir / "john_1.mp4").exists()
    assert not branch.exists()
    captured = capsys.readouterr()
    assert "Destination conflict" in captured.out
