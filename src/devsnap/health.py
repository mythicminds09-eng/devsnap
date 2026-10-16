from pathlib import Path
from devsnap.scanner import scan_project


def check_project(path: str | Path) -> list[str]:
    """Return read-only health warnings for a project."""
    return scan_project(path).warnings
