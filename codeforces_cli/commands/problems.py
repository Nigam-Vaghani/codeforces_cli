import typer
from rich.console import Console
from rich.table import Table

from codeforces_cli.services.contest_services import get_contest_problems

def problems(
    contest_id: int = typer.Argument(..., help="Codeforces contest ID. Example: 2197"),
):
    """
    List problems for a contest.

    Example:
      cf_cli problems 2197
    """
    console = Console()

    try:
        problems = get_contest_problems(contest_id)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return

    if not problems:
        console.print("[bold red]No problems found.[/bold red]")
        return

    table = Table(title=f"Problems for Contest {contest_id}")

    table.add_column("Index", style="cyan", justify="center")
    table.add_column("Name", style="green")
    table.add_column("Type", justify="center")
    table.add_column("Points", justify="center")
    table.add_column("Rating", justify="center")

    for p in problems:
        table.add_row(
            p.get("index", "N/A"),
            p.get("name", "N/A"),
            p.get("type", "N/A"),
            str(p.get("points", "N/A")),
            str(p.get("rating", "N/A")),
        )

    console.print(table)