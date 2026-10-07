"""Pull live GitHub numbers into data/github.json (run by the workflow).

Needs GITHUB_TOKEN (the Actions token is enough for public data). Set a
PROFILE_TOKEN secret with read:user to count private contributions too, if
"Private contributions" is switched on for the profile.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from . import profile as P

OUT = Path(__file__).resolve().parent.parent / "data" / "github.json"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        name stargazerCount pushedAt
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}
"""

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
# Markup and notebooks inflate byte counts without saying much about what was built.
SKIP_LANGS = {"Jupyter Notebook", "HTML"}


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set; keeping the existing snapshot.")
        return 0
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": P.HANDLE}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": f"{P.HANDLE}-profile"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if payload.get("errors"):
        print(json.dumps(payload["errors"], indent=2))
        return 1
    u = payload["data"]["user"]
    cc = u["contributionsCollection"]
    days = [{"date": d["date"], "count": d["contributionCount"], "level": LEVELS[d["contributionLevel"]]}
            for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    langs: dict[str, int] = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            if e["node"]["name"] not in SKIP_LANGS:
                langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    data = {
        "synced": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "total": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "private": cc["restrictedContributionsCount"],
        "repos": u["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "languages": sorted(({"name": k, "bytes": v} for k, v in langs.items()), key=lambda x: -x["bytes"]),
        "days": days,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1) + "\n")
    print(f"synced {len(days)} days, {data['total']} contributions, {data['repos']} public repos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
