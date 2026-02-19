from codeforces_cli.api.standings_client import fetch_contest_standings


def get_top_standings(contest_id: int, count: int = 20) -> list[dict]:
    data = fetch_contest_standings(contest_id=contest_id, start_from=1, count=count)

    rows = data.get("rows", [])
    standing_rows: list[dict] = []

    for row in rows:
        members = row.get("party", {}).get("members", [])
        handle = members[0].get("handle") if members else "N/A"

        standing_rows.append(
            {
                "rank": row.get("rank", "N/A"),
                "handle": handle,
                "points": row.get("points", 0),
                "penalty": row.get("penalty", 0),
            }
        )

    return standing_rows
