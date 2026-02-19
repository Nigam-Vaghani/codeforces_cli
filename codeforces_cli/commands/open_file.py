import typer
from rich.console import Console

from codeforces_cli.services.file_service import find_solution_file, open_file_in_vscode


def open_file(
    contest_id: int = typer.Argument(..., help="Codeforces contest ID. Example: 2197"),
    problem_index: str = typer.Argument(..., help="Problem index (A, B, C1, ...). Example: A"),
):
    """
    Open existing local solution file in VS Code.

    Example:
      cf_cli open-file 2197 A
    """
    console = Console()

    try:
        file_path = find_solution_file(contest_id, problem_index)
        open_file_in_vscode(file_path)
    except Exception as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Opened:[/bold green] {file_path}")
