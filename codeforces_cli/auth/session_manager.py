import os
import json
from pathlib import Path
import requests


SESSION_DIR = Path.home() / ".cf_cli"
SESSION_FILE = SESSION_DIR / "session.json"


def save_session(jsessionid: str, rcpc: str):
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "JSESSIONID": jsessionid,
        "39ce7": rcpc
    }

    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)


def load_session():
    if not SESSION_FILE.exists():
        return None

    with open(SESSION_FILE, "r") as f:
        return json.load(f)


def build_session():
    """
    Build authenticated requests session using stored cookies.
    """
    cookies = load_session()
    if not cookies:
        return None

    session = requests.Session()

    session.cookies.set("JSESSIONID", cookies["JSESSIONID"])
    session.cookies.set("39ce7", cookies["39ce7"])

    return session


def session_exists():
    return SESSION_FILE.exists()
