import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime

from codeforces_cli.services.contest_services import get_current_month_contests


def contest():
    """
    List current month contests.

    Example:
      cf_cli contest
    """
    console = Console()
    contests = get_current_month_contests()
    if not contests:
        console.print("[bold red]No contests found for this month.[/bold red]")
        return
    table = Table(title="Current month contests")
    
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Name", style="green")
    table.add_column("Type", justify="center")
    table.add_column("Phase", justify="center")
    table.add_column("Start Time", justify="center")
    table.add_column("Duration (hrs)", justify="center")

    for c in contests:
        start_time = datetime.fromtimestamp(c["startTimeSeconds"])
        duration_hours = round(c["durationSeconds"] / 3600, 2)

        table.add_row(
            str(c["id"]),
            c["name"],
            c.get("type", "N/A"),
            c.get("phase", "N/A"),
            start_time.strftime("%Y-%m-%d %H:%M"),
            str(duration_hours),
        )

    console.print(table)