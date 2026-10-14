import json
import pathlib
import sqlite3

import pandas as pd

SRC = pathlib.Path("data/validated/jobs_valid.json")
DB = pathlib.Path("data/jobstack.db")

COLUMNS = [
    "posting_id", "source", "source_url", "title", "description", "company_name",
    "category", "tags", "city", "country", "candidate_location", "work_mode",
    "employment_type", "experience", "salary_min", "salary_max", "currency",
    "salary_text", "posted_at", "language",
]

SCHEMA = """
CREATE TABLE jobs (
    posting_id TEXT NOT NULL,
    source TEXT NOT NULL,
    source_url TEXT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    company_name TEXT,
    category TEXT,
    tags TEXT,
    city TEXT,
    country TEXT,
    candidate_location TEXT,
    work_mode TEXT,
    employment_type TEXT,
    experience TEXT,
    salary_min REAL,
    salary_max REAL,
    currency TEXT,
    salary_text TEXT,
    posted_at TEXT,
    language TEXT,
    PRIMARY KEY (source, posting_id)
)
"""


def main():
    jobs = json.loads(SRC.read_text(encoding="utf-8"))
    df = pd.DataFrame(jobs).reindex(columns=COLUMNS)
    df["tags"] = df["tags"].apply(lambda t: json.dumps(t, ensure_ascii=False) if isinstance(t, list) else "[]")

    with sqlite3.connect(DB) as con:
        con.execute("DROP TABLE IF EXISTS jobs")
        con.execute(SCHEMA)
        df.to_sql("jobs", con, if_exists="append", index=False)
        total = con.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        print(f"Loaded {total} rows into {DB}")
        for row in con.execute("SELECT source, language, COUNT(*) FROM jobs GROUP BY source, language"):
            print(row)


if __name__ == "__main__":
    main()