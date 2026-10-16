from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProjectReport:
    root: Path
    ecosystems: list[str] = field(default_factory=list)
    key_files: list[str] = field(default_factory=list)
    is_git_repo: bool = False
    warnings: list[str] = field(default_factory=list)
    suggestions: list[tuple[str, str]] = field(default_factory=list)
