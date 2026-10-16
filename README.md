# DevSnap

**Know your project before you run it.**

DevSnap is a lightweight, local-first CLI that scans a coding project, detects common project types, suggests likely setup/test commands, and reports basic health warnings. No cloud account or API key required.

> MVP note: suggestions are heuristic and may not fit every project. DevSnap never executes commands automatically.

## Features
- Detect Python, JavaScript/TypeScript, Rust, Go, Java, and .NET markers.
- Summarize key files and Git status.
- Suggest likely install, run, and test commands.
- Report basic setup warnings.
- Read-only, local operation. Project files are not uploaded.

## Install
Requires Python 3.11+.

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Usage
```bash
devsnap inspect .
devsnap check .
devsnap commands .
```

## Safety
This release reads project metadata only. It does not run detected commands, install dependencies, or modify the scanned project. Review suggestions before running them yourself.

## Detection markers
| Ecosystem | Example markers |
|---|---|
| Python | `pyproject.toml`, `requirements.txt`, `setup.py` |
| JavaScript/TypeScript | `package.json`, `pnpm-lock.yaml`, `yarn.lock` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |
| Java | `pom.xml`, `build.gradle` |
| .NET | `*.sln`, `*.csproj`, `*.fsproj` |

Monorepos may be detected as multiple ecosystems.

## Development
```bash
python -m pip install -e ".[dev]"
pytest
```

## Roadmap
- [x] Initial scanner and CLI
- [x] Command suggestions
- [x] Basic health checks
- [x] Tests and cross-platform CI
- [ ] JSON output
- [ ] Configurable rules
- [ ] More ecosystem diagnostics
- [ ] Optional desktop UI

## Contributing
Pull requests welcome. Include tests for new detectors and command rules. Do not print or upload secrets found in scanned projects.

## License
MIT. See [LICENSE](LICENSE).
