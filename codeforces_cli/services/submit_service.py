import os
import time
from bs4 import BeautifulSoup

from codeforces_cli.auth.session_manager import build_session


def detect_file(contest_id, problem_index):
    extensions = [".cpp", ".py", ".java", ".c"]

    # Case 1: running from root (2197/A.java)
    for ext in extensions:
        path = f"{contest_id}/{problem_index}{ext}"
        if os.path.exists(path):
            return path, ext

    # Case 2: running inside contest folder (A.java)
    for ext in extensions:
        path = f"{problem_index}{ext}"
        if os.path.exists(path):
            return path, ext

    raise Exception("Solution file not found.")


def get_language_id(ext):
    mapping = {
        ".cpp": "54",   # GNU++17
        ".py": "31",    # Python 3
        ".java": "36",  # Java 11
        ".c": "43",     # GNU C11
    }

    if ext not in mapping:
        raise Exception("Unsupported language.")

    return mapping[ext]


def get_handle(session):
    resp = session.get("https://codeforces.com/")
    soup = BeautifulSoup(resp.text, "html.parser")

    user = soup.find("a", class_="rated-user")

    if not user:
        raise Exception("Unable to detect logged-in user.")

    return user.text.strip()


def get_csrf_token(session, contest_id):
    url = f"https://codeforces.com/contest/{contest_id}/submit"
    resp = session.get(url)

    # If redirected to login page
    if "enter" in resp.url:
        raise Exception("Session expired. Please run cf_cli login again.")

    soup = BeautifulSoup(resp.text, "html.parser")

    csrf = soup.find("input", {"name": "csrf_token"})

    if not csrf:
        raise Exception("CSRF token not found.")

    return csrf["value"]



def submit_solution(contest_id, problem_index):
    session = build_session()

    if not session:
        raise Exception("Not logged in. Run cf_cli login first.")

    file_path, ext = detect_file(contest_id, problem_index)
    language_id = get_language_id(ext)

    csrf_token = get_csrf_token(session, contest_id)

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    submit_url = f"https://codeforces.com/contest/{contest_id}/submit"

    data = {
        "csrf_token": csrf_token,
        "action": "submitSolutionFormSubmitted",
        "submittedProblemIndex": problem_index,
        "programTypeId": language_id,
        "source": source_code,
        "tabSize": "4",
        "_tta": "176",
    }

    session.post(submit_url, data=data)

    handle = get_handle(session)

    # Fetch latest submission
    resp = session.get(f"https://codeforces.com/contest/{contest_id}/my")
    soup = BeautifulSoup(resp.text, "html.parser")

    row = soup.find("tr", attrs={"data-submission-id": True})

    if not row:
        raise Exception("Unable to retrieve submission ID.")

    submission_id = row["data-submission-id"]

    return {
        "submission_id": submission_id,
        "handle": handle,
        "file_path": file_path,
    }


def poll_submission_verdict(contest_id, handle, submission_id):
    session = build_session()

    while True:
        resp = session.get(f"https://codeforces.com/contest/{contest_id}/my")
        soup = BeautifulSoup(resp.text, "html.parser")

        row = soup.find("tr", {"data-submission-id": submission_id})

        if not row:
            time.sleep(2)
            continue

        verdict_cell = row.find("span", class_="submissionVerdictWrapper")
        passed_cell = row.find("td", class_="passedTestCount")

        verdict = verdict_cell.text.strip() if verdict_cell else "UNKNOWN"
        passed = passed_cell.text.strip() if passed_cell else "0"

        yield {
            "verdict": verdict,
            "passed_test_count": passed,
        }

        if verdict not in ["In queue", "Running", "TESTING"]:
            break

        time.sleep(2)
