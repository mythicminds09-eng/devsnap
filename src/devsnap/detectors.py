from pathlib import Path

MARKERS: dict[str, tuple[str, ...]] = {
    "Python": ("pyproject.toml", "requirements.txt", "setup.py", "Pipfile"),
    "JavaScript / TypeScript": ("package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json", "tsconfig.json"),
    "Rust": ("Cargo.toml",),
    "Go": ("go.mod",),
    "Java": ("pom.xml", "build.gradle", "build.gradle.kts"),
}

IMPORTANT_FILES = (
    "README.md", "README.rst", "pyproject.toml", "requirements.txt",
    "package.json", "Cargo.toml", "go.mod", "pom.xml", "build.gradle",
    "Makefile", "Dockerfile", ".env.example",
)


def detect_ecosystems(root: Path) -> list[str]:
    found = [name for name, markers in MARKERS.items()
             if any((root / marker).is_file() for marker in markers)]
    if any(root.glob("*.sln")) or any(root.glob("*.csproj")) or any(root.glob("*.fsproj")):
        found.append(".NET")
    return found


def find_key_files(root: Path) -> list[str]:
    found = [name for name in IMPORTANT_FILES if (root / name).is_file()]
    found.extend(sorted(p.name for pattern in ("*.sln", "*.csproj", "*.fsproj")
                        for p in root.glob(pattern) if p.is_file()))
    return list(dict.fromkeys(found))
