import typer
from codeforces_cli.commands.hello import hello
from codeforces_cli.commands.contest import contest
from codeforces_cli.commands.problems import problems
from codeforces_cli.commands.open_problem import open as open_problem
from codeforces_cli.commands.create_file import create
from codeforces_cli.commands.open_file import open_file
from codeforces_cli.commands.login import login
from codeforces_cli.commands.submit import submit
from codeforces_cli.commands.standing import standing
from codeforces_cli.commands.login import login

app = typer.Typer(
    help="Codeforces CLI - Manage contests from terminal 🚀",
    no_args_is_help=True,
)

app.command()(hello)
app.command()(contest)
app.command()(problems)
app.command()(open_problem)
app.command(name="create")(create)
app.command(name="open-file")(open_file)
# app.command(name="login")(login)
app.command(name="submit")(submit)
app.command(name="standing")(standing)
app.command()(login)

@app.callback()
def main():
    """Codeforces CLI entrypoint."""


if __name__ == "__main__":
    app()