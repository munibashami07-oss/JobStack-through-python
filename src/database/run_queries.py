"""Run every query in sql/04_queries.sql and print the results (handy for screenshots and the demo).

Run from the repository root:
    python -m src.database.run_queries
"""

import argparse
import pathlib
import sqlite3

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUERY_FILE = ROOT / "sql" / "04_queries.sql"
DEFAULT_DB = ROOT / "data" / "jobstack_final.db"


def load_queries(path=QUERY_FILE):
    """Split the .sql file on '-- name:' marker lines -> list of (name, sql_text)."""
    queries, name, lines = [], None, []
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("-- name:"):
            if name:
                queries.append((name, "\n".join(lines).strip()))
            name, lines = line[len("-- name:"):].strip(), []
        elif name:
            lines.append(line)
    if name:
        queries.append((name, "\n".join(lines).strip()))
    return queries


def main():
    parser = argparse.ArgumentParser(description="Run the JobStack analytical SQL queries.")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    args = parser.parse_args()

    con = sqlite3.connect(args.db)
    try:
        for name, sql in load_queries():
            print(f"\n=== {name} ===")
            print(pd.read_sql_query(sql, con).to_string(index=False))
    finally:
        con.close()


if __name__ == "__main__":
    main()
