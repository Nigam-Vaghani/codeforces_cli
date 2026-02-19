from datetime import datetime
from codeforces_cli.api.client import fetch

def get_current_month_contests():
    contests = fetch("contest.list")
    now = datetime.now()
    curr_month = now.month
    curr_year = now.year
    filtered_contest = []
    for c in contests:
        if "startTimeSeconds" not in c:
            continue
        start_time = datetime.fromtimestamp(c["startTimeSeconds"])
        if(
            start_time.month == curr_month
            and start_time.year == curr_year
        ):
            filtered_contest.append(c)
    return filtered_contest

def get_contest_problems(contest_id : int):
    data = fetch(
        "contest.standings",
        {
            "contestId" : contest_id,
            "from" : 1,
            "count": 1,
        },
    )
    
    return data["problems"]