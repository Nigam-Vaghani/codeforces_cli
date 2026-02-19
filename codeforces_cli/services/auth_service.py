from codeforces_cli.api.auth_client import login
from codeforces_cli.config.store import get_session, save_session


def login_and_persist(handle: str, password: str) -> str:
    session = login(handle, password)
    cookies = session.cookies.get_dict()
    save_session(handle=handle, cookies=cookies)
    return handle


def get_stored_session() -> tuple[str, dict[str, str]]:
    handle, cookies = get_session()
    if not handle or not cookies:
        raise Exception("Not logged in. Run 'cf_cli login' first.")
    return handle, cookies
