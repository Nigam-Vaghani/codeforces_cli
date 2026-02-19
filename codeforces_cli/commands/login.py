import typer
from rich.console import Console
from codeforces_cli.auth.session_manager import save_session


def login():
    """
    Login by manually pasting Codeforces session cookies.
    """

    console = Console()

    console.print("[bold cyan]Login to Codeforces[/bold cyan]")
    console.print("Open Codeforces in your browser and login.")
    console.print("Then open DevTools → Application → Cookies → codeforces.com\n")

    jsessionid = typer.prompt("Paste JSESSIONID")
    rcpc = typer.prompt("Paste 39ce7")

    save_session(jsessionid, rcpc)

    console.print("[bold green]Session saved successfully![/bold green]")
