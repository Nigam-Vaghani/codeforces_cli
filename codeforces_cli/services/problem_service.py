import cloudscraper
from bs4 import BeautifulSoup


def get_problem_statement(contest_id: int, index: str):
    url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"

    scraper = cloudscraper.create_scraper()

    response = scraper.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch problem (Status {response.status_code})")

    soup = BeautifulSoup(response.text, "html.parser")

    problem_div = soup.find("div", class_="problem-statement")

    if not problem_div:
        raise Exception("Problem statement not found")

    return problem_div
