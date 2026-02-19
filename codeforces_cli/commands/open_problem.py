import typer
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from codeforces_cli.services.problem_service import get_problem_statement


def open(
    contest_id: int = typer.Argument(..., help="Codeforces contest ID. Example: 2197"),
    index: str = typer.Argument(..., help="Problem index (A, B, C1, ...). Example: A"),
):
    """
    Open full problem statement in terminal.

    Example:
      cf_cli open 2197 A
    """

    console = Console()

    try:
        problem_div = get_problem_statement(contest_id, index)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return

    # ---------------- TITLE ----------------
    title_div = problem_div.find("div", class_="title")
    title = title_div.text.strip() if title_div else "Unknown Title"

    time_limit = problem_div.find("div", class_="time-limit")
    memory_limit = problem_div.find("div", class_="memory-limit")

    time_text = time_limit.text.strip() if time_limit else "N/A"
    memory_text = memory_limit.text.strip() if memory_limit else "N/A"

    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", expand=False))
    console.print(f"[yellow]{time_text}[/yellow]")
    console.print(f"[yellow]{memory_text}[/yellow]")

    console.print(Rule())

    # ---------------- DESCRIPTION ----------------
    console.print("[bold white]Problem Description[/bold white]\n")

    for element in problem_div.find_all(recursive=False):
        if element.name == "p":
            console.print(element.get_text(strip=True))
            console.print()

        elif element.name == "pre":
            console.print(Panel(element.get_text(), title="Code", expand=False))
            console.print()

        elif element.get("class") in [
            ["input-specification"],
            ["output-specification"],
            ["sample-test"],
            ["title"],
            ["time-limit"],
            ["memory-limit"],
        ]:
            continue

    # ---------------- INPUT ----------------
    input_section = problem_div.find("div", class_="input-specification")
    if input_section:
        console.print(Rule("[bold green]Input[/bold green]"))

        for element in input_section.find_all(["p", "pre"]):
            if element.name == "p":
                console.print(element.get_text(strip=True))
                console.print()
            elif element.name == "pre":
                console.print(Panel(element.get_text(), title="Input Format", expand=False))
                console.print()

    # ---------------- OUTPUT ----------------
    output_section = problem_div.find("div", class_="output-specification")
    if output_section:
        console.print(Rule("[bold green]Output[/bold green]"))

        for element in output_section.find_all(["p", "pre"]):
            if element.name == "p":
                console.print(element.get_text(strip=True))
                console.print()
            elif element.name == "pre":
                console.print(Panel(element.get_text(), title="Output Format", expand=False))
                console.print()

    # ---------------- SAMPLE TESTS ----------------
    sample_section = problem_div.find("div", class_="sample-test")
    if sample_section:
        console.print(Rule("[bold magenta]Sample Tests[/bold magenta]"))

        inputs = sample_section.find_all("div", class_="input")
        outputs = sample_section.find_all("div", class_="output")

        for i in range(len(inputs)):
            input_text = inputs[i].find("pre").get_text()
            output_text = outputs[i].find("pre").get_text()

            console.print(
                Panel(input_text, title=f"Sample Input {i+1}", border_style="green")
            )
            console.print(
                Panel(output_text, title=f"Sample Output {i+1}", border_style="blue")
            )
            console.print()
