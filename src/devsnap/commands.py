import json
from pathlib import Path


def suggest_commands(root: Path) -> list[tuple[str, str]]:
    """Return conservative command suggestions; never execute them."""
    suggestions: list[tuple[str, str]] = []
    package_json = root / "package.json"
    if package_json.is_file():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            scripts = data.get("scripts", {})
            if (root / "pnpm-lock.yaml").exists():
                installer = "pnpm install"
            elif (root / "yarn.lock").exists():
                installer = "yarn install"
            else:
                installer = "npm install"
            suggestions.append(("Install dependencies", installer))
            runner = _package_runner(root)
            if "dev" in scripts:
                suggestions.append(("Start development server", f"{runner} run dev"))
            elif "start" in scripts:
                suggestions.append(("Start application", f"{runner} run start"))
            if "test" in scripts:
                suggestions.append(("Run tests", f"{runner} run test"))
        except (OSError, json.JSONDecodeError):
            suggestions.append(("Inspect package manifest", "Open package.json and validate its JSON"))
    elif (root / "pyproject.toml").is_file():
        suggestions.append(("Install project", "python -m pip install -e ."))
        if (root / "tests").is_dir():
            suggestions.append(("Run tests", "python -m pytest"))
    elif (root / "requirements.txt").is_file():
        suggestions.append(("Install dependencies", "python -m pip install -r requirements.txt"))
        if (root / "tests").is_dir():
            suggestions.append(("Run tests", "python -m pytest"))
    elif (root / "Cargo.toml").is_file():
        suggestions.extend([("Build", "cargo build"), ("Run tests", "cargo test")])
    elif (root / "go.mod").is_file():
        suggestions.extend([("Build", "go build ./..."), ("Run tests", "go test ./...")])
    elif (root / "pom.xml").is_file():
        suggestions.extend([("Build", "mvn package"), ("Run tests", "mvn test")])
    elif any(root.glob("*.csproj")) or any(root.glob("*.sln")):
        suggestions.extend([("Build", "dotnet build"), ("Run tests", "dotnet test")])
    return suggestions


def _package_runner(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    return "npm"
