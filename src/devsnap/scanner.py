from pathlib import Path

from devsnap.commands import suggest_commands
from devsnap.detectors import detect_ecosystems, find_key_files
from devsnap.models import ProjectReport


def scan_project(path: str | Path) -> ProjectReport:
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root}")
    ecosystems = detect_ecosystems(root)
    key_files = find_key_files(root)
    warnings: list[str] = []
    if not ecosystems:
        warnings.append("No supported project manifest detected.")
    if not (root / ".git").exists():
        warnings.append("No .git directory detected.")
    if (root / "package.json").exists() and not any(
        (root / lock).exists() for lock in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock")
    ):
        warnings.append("package.json found without a recognized JavaScript lockfile.")
    return ProjectReport(root=root, ecosystems=ecosystems, key_files=key_files,
                         is_git_repo=(root / ".git").exists(), warnings=warnings,
                         suggestions=suggest_commands(root))
