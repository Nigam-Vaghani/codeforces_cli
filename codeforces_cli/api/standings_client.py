from codeforces_cli.api.client import fetch


def fetch_contest_standings(contest_id: int, start_from: int = 1, count: int = 20):
    return fetch(
        "contest.standings",
        {
            "contestId": contest_id,
            "from": start_from,
            "count": count,
        },
    )
