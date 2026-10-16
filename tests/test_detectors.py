from pathlib import Path
from devsnap.detectors import detect_ecosystems, find_key_files


def test_detect_python_and_node(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / "package.json").write_text('{"scripts": {}}', encoding="utf-8")
    assert detect_ecosystems(tmp_path) == ["Python", "JavaScript / TypeScript"]


def test_detect_dotnet(tmp_path: Path):
    (tmp_path / "Demo.csproj").write_text("<Project />", encoding="utf-8")
    assert ".NET" in detect_ecosystems(tmp_path)


def test_find_key_files(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo", encoding="utf-8")
    assert find_key_files(tmp_path) == ["README.md"]
