import re
from bs4 import BeautifulSoup

from codeforces_cli.api.web_utils import extract_csrf_token, extract_ftaa_bfaa
from codeforces_cli.submit.languages import LANGUAGES


def _extract_program_type_options(html: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    program_select = soup.find("select", {"name": "programTypeId"})
    if not program_select:
        return []

    options: list[tuple[str, str]] = []
    for option in program_select.find_all("option"):
        option_id = option.get("value")
        option_name = option.text.strip()
        if option_id:
            options.append((option_id, option_name))
    return options


def _pick_program_type_id(language: str, options: list[tuple[str, str]]) -> str:
    keywords = LANGUAGES[language]["cf_keywords"]

    for keyword in keywords:
        for option_id, option_name in options:
            if keyword.lower() in option_name.lower():
                return option_id

    if not options:
        raise Exception("No language options found on submit page")

    return options[0][0]


def submit_solution(session, contest_id: int, index: str, source_code: str, language: str) -> int | None:
    submit_page_url = f"https://codeforces.com/contest/{contest_id}/submit"

    page_response = session.get(submit_page_url)
    if page_response.status_code != 200:
        raise Exception("Unable to open submit page")

    csrf_token = extract_csrf_token(page_response.text)
    ftaa, bfaa = extract_ftaa_bfaa(page_response.text)
    options = _extract_program_type_options(page_response.text)
    program_type_id = _pick_program_type_id(language, options)

    payload = {
        "csrf_token": csrf_token,
        "ftaa": ftaa,
        "bfaa": bfaa,
        "action": "submitSolutionFormSubmitted",
        "submittedProblemIndex": index,
        "programTypeId": program_type_id,
        "source": source_code,
        "tabSize": "4",
        "sourceFile": "",
        "_tta": "176",
    }

    headers = {"Referer": submit_page_url}
    submit_response = session.post(
        submit_page_url,
        data=payload,
        headers=headers,
        allow_redirects=True,
    )

    if submit_response.status_code not in (200, 302):
        raise Exception("Submission request failed")

    submission_id_match = re.search(r"submission/(\d+)", submit_response.url)
    if submission_id_match:
        return int(submission_id_match.group(1))

    html_match = re.search(r"submission/(\d+)", submit_response.text)
    if html_match:
        return int(html_match.group(1))

    return None
