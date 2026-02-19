import re
from bs4 import BeautifulSoup


def extract_csrf_token(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    token_input = soup.find("input", {"name": "csrf_token"})
    if not token_input or not token_input.get("value"):
        raise Exception("Unable to extract csrf token")
    return token_input["value"]


def extract_ftaa_bfaa(html: str) -> tuple[str, str]:
    ftaa_match = re.search(r'"ftaa"\s*:\s*"([^"]+)"', html)
    bfaa_match = re.search(r'"bfaa"\s*:\s*"([^"]+)"', html)

    if ftaa_match and bfaa_match:
        return ftaa_match.group(1), bfaa_match.group(1)

    soup = BeautifulSoup(html, "html.parser")
    ftaa_input = soup.find("input", {"name": "ftaa"})
    bfaa_input = soup.find("input", {"name": "bfaa"})

    return (
        ftaa_input["value"] if ftaa_input and ftaa_input.get("value") else "",
        bfaa_input["value"] if bfaa_input and bfaa_input.get("value") else "",
    )
