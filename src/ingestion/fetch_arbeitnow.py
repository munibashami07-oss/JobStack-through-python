import datetime
import json
import pathlib
import time

import requests

URL = "https://www.arbeitnow.com/api/job-board-api"
MAX_PAGES = 10


def main():
    jobs = []
    for page in range(1, MAX_PAGES + 1):
        r = requests.get(URL, params={"page": page}, timeout=30,
                         headers={"User-Agent": "JobStack-student-project"})
        r.raise_for_status()
        batch = r.json().get("data", [])
        if not batch:
            break
        jobs.extend(batch)
        print(f"page {page}: {len(batch)} jobs")
        time.sleep(1.5)

    out = pathlib.Path("data/raw")
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    path = out / f"arbeitnow_{stamp}.json"
    path.write_text(json.dumps({"data": jobs}), encoding="utf-8")
    print(f"Saved {len(jobs)} jobs to {path}")
    if jobs:
        print(json.dumps(jobs[0], indent=2)[:1200])


if __name__ == "__main__":
    main()