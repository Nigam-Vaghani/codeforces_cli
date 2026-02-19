import typer
from rich.console import Console

from codeforces_cli.services.file_service import create_solution_file


def create(
    contest_id: int = typer.Argument(..., help="Codeforces contest ID. Example: 2197"),
    problem_index: str = typer.Argument(..., help="Problem index (A, B, C1, ...). Example: A"),
    language: str = typer.Argument(..., help="Language: cpp | c | java | python"),
):
    """
    Create local solution file with language template.

    Example:
      cf_cli create 2197 A cpp
    """
    console = Console()

    try:
        file_path = create_solution_file(contest_id, problem_index, language)
    except Exception as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Created:[/bold green] {file_path}")
