from codeforces_cli.api.web_utils import extract_csrf_token, extract_ftaa_bfaa
from codeforces_cli.auth.session_manager import build_session


def login(handle: str, password: str):
    session = build_session()

    enter_url = "https://codeforces.com/enter"
    page_response = session.get(enter_url)
    if page_response.status_code != 200:
        raise Exception("Unable to open login page")

    csrf_token = extract_csrf_token(page_response.text)
    ftaa, bfaa = extract_ftaa_bfaa(page_response.text)

    payload = {
        "csrf_token": csrf_token,
        "action": "enter",
        "ftaa": ftaa,
        "bfaa": bfaa,
        "handleOrEmail": handle,
        "password": password,
        "remember": "on",
        "_tta": "176",
    }

    headers = {"Referer": enter_url}
    submit_response = session.post(enter_url, data=payload, headers=headers, allow_redirects=True)

    if submit_response.status_code not in (200, 302):
        raise Exception("Login failed")

    if "/enter" in submit_response.url and "password" in submit_response.text.lower():
        raise Exception("Invalid handle or password")

    return session
