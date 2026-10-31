"""Build the normalized JobStack SQLite database and load Person 2's final data.

JobStack - Person 3 (SQL Database Engineering).

What this script does (the "L" = Load in ETL):
1. Reads data/transformed/jobs_final.json  (Person 2's output).
2. Deletes any old database file and runs the SQL scripts in sql/ (schema, indexes, views).
3. Inserts companies, locations, skills, postings, posting_skills, salary_observations.
4. Runs QA checks (row counts + referential integrity) and exits with code 1 if one fails.

Run from the repository root:
    python -m src.database.load_database
"""

import argparse
import json
import pathlib
import sqlite3
import sys

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]
SQL_DIR = ROOT / "sql"
DEFAULT_SRC = ROOT / "data" / "transformed" / "jobs_final.json"
DEFAULT_DB = ROOT / "data" / "jobstack_final.db"
SQL_SETUP_FILES = ["01_schema.sql", "02_indexes.sql", "03_views.sql"]
EXTRACTION_METHOD = "dictionary_match"   # how Person 2 extracted skills (see transformation report)

REQUIRED_COLUMNS = [
    "posting_id", "source", "source_url", "title", "standardized_title", "cleaned_description",
    "company_name", "category", "standardized_city", "country", "experience",
    "standardized_employment_type", "standardized_work_mode", "posted_at", "language",
    "salary_min", "salary_max", "currency", "salary_text", "extracted_skills",
]


def get_or_create(cur, table, id_col, match, extra=None):
    """Return the id of the row matching `match`; insert it first if it does not exist.

    `match` is a dict like {"city": "London", "country": None}.
    We compare with `IS ?` (not `= ?`) because in SQL NULL = NULL is never true,
    so `=` would create duplicate rows for NULL values.
    Table/column names come from our own code (never from user data), so f-strings are safe here.
    Values always go through `?` placeholders.
    """
    cols = list(match)
    where = " AND ".join(f"{c} IS ?" for c in cols)
    row = cur.execute(
        f"SELECT {id_col} FROM {table} WHERE {where}", tuple(match[c] for c in cols)
    ).fetchone()
    if row:
        return row[0]
    data = {**match, **(extra or {})}
    placeholders = ",".join("?" * len(data))
    cur.execute(
        f"INSERT INTO {table} ({','.join(data)}) VALUES ({placeholders})", tuple(data.values())
    )
    return cur.lastrowid   # id of the row we just inserted


def prepare_dataframe(records):
    """List of dicts -> DataFrame where every missing value is None (what SQL calls NULL)."""
    df = pd.DataFrame(records)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Input data is missing required columns: {missing}")
    # pandas/JSON use NaN for "missing"; SQLite needs None. Converting avoids storing garbage.
    return df.astype(object).where(df.notna(), None)


def run_qa(con, df):
    """Compare what is in the database with what was in the input. Returns [(name, ok, detail)]."""
    cur = con.cursor()

    def count(table):
        return cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    skill_lists = [list(dict.fromkeys(s.strip() for s in (v or []))) for v in df["extracted_skills"]]
    expected = {
        "postings": len(df),
        "companies": df["company_name"].dropna().nunique(),
        "locations": len(df.dropna(subset=["standardized_city"])[["standardized_city", "country"]].drop_duplicates()),
        "skills": len({s for lst in skill_lists for s in lst}),
        "posting_skills": sum(len(lst) for lst in skill_lists),
    }
    results = [
        (f"{t} row count = {n}", count(t) == n, f"db has {count(t)}") for t, n in expected.items()
    ]
    fk_problems = cur.execute("PRAGMA foreign_key_check").fetchall()
    results.append(("no foreign key violations", not fk_problems, f"{len(fk_problems)} found"))
    zero = cur.execute(
        "SELECT COUNT(*) FROM salary_observations WHERE salary_min = 0 OR salary_max = 0"
    ).fetchone()[0]
    results.append(("no salary stored as 0", zero == 0, f"{zero} found"))
    return results


def build_database(records, db_path, sql_dir=SQL_DIR):
    """Create db_path from scratch and load `records`. Returns {"counts": {...}, "qa": [...]}."""
    db_path = pathlib.Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()   # rebuild from scratch = reproducible

    df = prepare_dataframe(records)
    con = sqlite3.connect(db_path)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()
        for name in SQL_SETUP_FILES:
            cur.executescript((pathlib.Path(sql_dir) / name).read_text(encoding="utf-8"))

        for r in df.itertuples(index=False):
            company_id = None
            if r.company_name:
                company_id = get_or_create(cur, "companies", "company_id", {"company_name": r.company_name})

            location_id = None
            if r.standardized_city:
                location_id = get_or_create(
                    cur, "locations", "location_id", {"city": r.standardized_city, "country": r.country}
                )

            cur.execute(
                """INSERT INTO postings (source, source_posting_id, source_url, title, standardized_title,
                       description, company_id, location_id, category, experience, employment_type,
                       work_mode, posted_at, language)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (r.source, r.posting_id, r.source_url, r.title, r.standardized_title,
                 r.cleaned_description, company_id, location_id, r.category, r.experience,
                 r.standardized_employment_type, r.standardized_work_mode, r.posted_at, r.language),
            )
            posting_pk = cur.lastrowid

            for skill in (r.extracted_skills or []):
                skill_id = get_or_create(cur, "skills", "skill_id", {"canonical_name": skill.strip()})
                cur.execute(
                    "INSERT OR IGNORE INTO posting_skills (posting_pk, skill_id, extraction_method) VALUES (?,?,?)",
                    (posting_pk, skill_id, EXTRACTION_METHOD),
                )

            if r.salary_text is not None or r.salary_min is not None or r.salary_max is not None:
                cur.execute(
                    """INSERT INTO salary_observations (posting_pk, salary_min, salary_max, currency, salary_text)
                       VALUES (?,?,?,?,?)""",
                    (posting_pk, r.salary_min, r.salary_max, r.currency, r.salary_text),
                )

        con.commit()   # without commit, nothing is saved
        counts = {
            t: cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in ["companies", "locations", "skills", "postings", "posting_skills", "salary_observations"]
        }
        return {"counts": counts, "qa": run_qa(con, df)}
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build and load the JobStack SQL database.")
    parser.add_argument("--src", default=str(DEFAULT_SRC), help="transformed JSON file")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="output SQLite file")
    args = parser.parse_args(argv)

    records = json.loads(pathlib.Path(args.src).read_text(encoding="utf-8"))
    result = build_database(records, args.db)

    print(f"Database built: {args.db}\n")
    print("Row counts:")
    for table, n in result["counts"].items():
        print(f"  {table:22s} {n}")
    print("\nQA checks:")
    all_ok = True
    for name, ok, detail in result["qa"]:
        all_ok &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}  ({detail})")
    print("\nALL CHECKS PASSED" if all_ok else "\nSOME CHECKS FAILED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
