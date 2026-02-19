from playwright.sync_api import sync_playwright
from rich.console import Console
from codeforces_cli.auth.session_manager import save_session


def login_with_playwright(handle: str, password: str):
    console = Console()

    console.print("[bold cyan]Launching headless browser...[/bold cyan]")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://codeforces.com/enter")

        # Wait for login form to appear (Cloudflare may delay it)
        page.wait_for_selector('input[name="handleOrEmail"]', timeout=60000)

        page.fill('input[name="handleOrEmail"]', handle)
        page.fill('input[name="password"]', password)

        page.click('input[type="submit"]')

        page.wait_for_load_state("networkidle")

        if "enter" in page.url:
            browser.close()
            raise Exception("Login failed. Check credentials.")

        console.print("[green]Login successful![/green]")

        cookies = context.cookies()
        save_session(cookies)

        console.print("[bold green]Session saved successfully.[/bold green]")

        browser.close()
