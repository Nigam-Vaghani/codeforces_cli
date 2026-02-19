import typer
from rich.console import Console
from rich.table import Table

from codeforces_cli.services.standing_service import get_top_standings


def standing(
    contest_id: int = typer.Argument(..., help="Codeforces contest ID. Example: 2197"),
):
    """
    Show top 20 standings for a contest.

    Example:
      cf_cli standing 2197
    """
    console = Console()

    try:
        rows = get_top_standings(contest_id, count=20)
    except Exception as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    if not rows:
        console.print("[bold red]No standings found.[/bold red]")
        raise typer.Exit(code=1)

    table = Table(title=f"Top 20 Standings - Contest {contest_id}")
    table.add_column("Rank", style="cyan", justify="right")
    table.add_column("Handle", style="green")
    table.add_column("Points", justify="right")
    table.add_column("Penalty", justify="right")

    for row in rows:
        table.add_row(
            str(row["rank"]),
            row["handle"],
            str(row["points"]),
            str(row["penalty"]),
        )

    console.print(table)
