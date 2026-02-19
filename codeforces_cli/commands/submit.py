import typer
from rich.console import Console

from codeforces_cli.services.submit_service import (
    submit_solution,
    poll_submission_verdict,
)

console = Console()


def submit(
    contest_id: int = typer.Argument(..., help="Contest ID"),
    problem_index: str = typer.Argument(..., help="Problem index (A, B, C1...)"),
):
    """
    Submit local solution file and stream verdict updates.
    """

    try:
        submission = submit_solution(contest_id, problem_index)
    except Exception as error:
        console.print(f"[bold red]Submission failed:[/bold red] {error}")
        raise typer.Exit(code=1)

    submission_id = submission["submission_id"]
    handle = submission["handle"]

    console.print(f"[bold cyan]Submitted[/bold cyan] {submission['file_path']}")
    console.print(f"Submission ID: {submission_id}")

    last_snapshot = None

    try:
        for snapshot in poll_submission_verdict(contest_id, handle, submission_id):
            if snapshot == last_snapshot:
                continue

            last_snapshot = snapshot

            console.print(
                f"Status: {snapshot['verdict']} | "
                f"Passed Tests: {snapshot['passed_test_count']}"
            )

        if last_snapshot:
            final_verdict = last_snapshot["verdict"]
            style = "green" if final_verdict == "OK" else "red"
            console.print(f"[bold {style}]Final Verdict: {final_verdict}[/bold {style}]")

    except Exception as error:
        console.print(f"[bold red]Error while polling verdict:[/bold red] {error}")
        raise typer.Exit(code=1)
