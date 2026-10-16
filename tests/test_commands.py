from pathlib import Path
from devsnap.commands import suggest_commands


def test_node_suggestions_from_scripts(tmp_path: Path):
    (tmp_path / "package.json").write_text('{"scripts":{"dev":"vite","test":"vitest"}}', encoding="utf-8")
    commands = [command for _, command in suggest_commands(tmp_path)]
    assert "npm install" in commands
    assert "npm run dev" in commands
    assert "npm run test" in commands


def test_python_suggestions(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    assert ("Install project", "python -m pip install -e .") in suggest_commands(tmp_path)
    assert ("Run tests", "python -m pytest") in suggest_commands(tmp_path)


def test_invalid_package_json_is_handled(tmp_path: Path):
    (tmp_path / "package.json").write_text("{invalid", encoding="utf-8")
    assert suggest_commands(tmp_path) == [("Inspect package manifest", "Open package.json and validate its JSON")]
