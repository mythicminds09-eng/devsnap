from pathlib import Path
import pytest
from devsnap.scanner import scan_project


def test_scan_project_is_read_only(tmp_path: Path):
    (tmp_path / "go.mod").write_text("module example.com/demo\n", encoding="utf-8")
    report = scan_project(tmp_path)
    assert report.ecosystems == ["Go"]
    assert ("Build", "go build ./...") in report.suggestions
    assert (tmp_path / "go.mod").read_text(encoding="utf-8").startswith("module")
    assert report.is_git_repo is False


def test_missing_path_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        scan_project(tmp_path / "missing")


def test_file_path_rejected(tmp_path: Path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("hello", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        scan_project(file_path)
