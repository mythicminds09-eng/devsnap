from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from devsnap import __version__
from devsnap.scanner import scan_project

app = typer.Typer(name="devsnap", help="Inspect coding projects and suggest safe next steps.",
                  no_args_is_help=True, add_completion=False)
console = Console()


def _report(path: Path):
    try:
        return scan_project(path)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=2) from exc


@app.command()
def inspect(path: Path = typer.Argument(Path("."), exists=True, file_okay=False, readable=True)):
    """Summarize a project's ecosystem, files, and Git status."""
    report = _report(path)
    console.print(Panel(f"[bold]DevSnap[/bold] v{__version__}\n[dim]Know your project before you run it.[/dim]", border_style="cyan"))
    console.print(f"[bold]Project:[/bold] {report.root.name or report.root}")
    console.print(f"[bold]Path:[/bold] {report.root}")
    console.print(f"[bold]Ecosystems:[/bold] {', '.join(report.ecosystems) if report.ecosystems else 'Unknown'}")
    console.print(f"[bold]Git repository:[/bold] {'Yes' if report.is_git_repo else 'No'}")
    table = Table(title="Key files")
    table.add_column("File")
    for item in report.key_files:
        table.add_row(item)
    if not report.key_files:
        table.add_row("No known key files found")
    console.print(table)
    if report.warnings:
        console.print(f"[yellow]Warnings: {len(report.warnings)}[/yellow]")
        for warning in report.warnings:
            console.print(f"  • {warning}")
    else:
        console.print("[green]No basic health warnings detected.[/green]")


@app.command()
def check(path: Path = typer.Argument(Path("."), exists=True, file_okay=False, readable=True)):
    """Show basic setup warnings without changing files."""
    report = _report(path)
    if report.warnings:
        for warning in report.warnings:
            console.print(f"[yellow]WARNING[/yellow] {warning}")
        raise typer.Exit(code=1)
    console.print("[green]No basic health warnings detected.[/green]")


@app.command()
def commands(path: Path = typer.Argument(Path("."), exists=True, file_okay=False, readable=True)):
    """Suggest likely commands; nothing is executed."""
    report = _report(path)
    if not report.suggestions:
        console.print("No command suggestions available for this project yet.")
        return
    table = Table(title="Suggested commands (not executed)")
    table.add_column("Purpose", style="cyan")
    table.add_column("Command", style="green")
    for purpose, command in report.suggestions:
        table.add_row(purpose, command)
    console.print(table)
    console.print("[dim]Review each command before running it yourself.[/dim]")


if __name__ == "__main__":
    app()
