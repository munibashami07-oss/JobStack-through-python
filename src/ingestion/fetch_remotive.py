import datetime
import json
import pathlib

import requests

URL = "https://remotive.com/api/remote-jobs"


def main():
    r = requests.get(URL, timeout=30, headers={"User-Agent": "JobStack-student-project"})
    r.raise_for_status()
    out = pathlib.Path("data/raw")
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    path = out / f"remotive_{stamp}.json"
    path.write_text(r.text, encoding="utf-8")
    jobs = r.json().get("jobs", [])
    print(f"Saved {len(jobs)} jobs to {path}")
    if jobs:
        print(json.dumps(jobs[0], indent=2)[:1500])


if __name__ == "__main__":
    main()