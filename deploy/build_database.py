"""One command to (re)build and verify the JobStack SQLite database.

Use this as the database *build step* on any host (Render, Railway, a classmate's laptop):

    python deploy/build_database.py
    python deploy/build_database.py --db /tmp/jobstack.db      # custom output path

What it does:
  1. Runs Person 3's loader  (python -m src.database.load_database)  -> creates the .db file
  2. Runs Person 3's verifier (python -m src.database.verify_database) -> integrity and QA checks
  3. Exits with code 1 if either step fails, so a deployment stops instead of serving a broken database.

The verifier's report is written to a temporary file, so running this never changes
the committed reports/database/database_verification_report.md.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "jobstack_final.db"


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=ROOT).returncode


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=str(DEFAULT_DB), help="output SQLite file (default: data/jobstack_final.db)")
    ap.add_argument("--skip-verify", action="store_true", help="only build, do not run the verifier")
    args = ap.parse_args(argv)

    py = sys.executable
    if run([py, "-m", "src.database.load_database", "--db", args.db]) != 0:
        print("\nBUILD FAILED: load_database reported an error.")
        return 1

    if not args.skip_verify:
        with tempfile.TemporaryDirectory() as tmp:
            report = str(Path(tmp) / "verification_report.md")
            if run([py, "-m", "src.database.verify_database", "--db", args.db, "--report", report]) != 0:
                print("\nBUILD FAILED: verify_database reported a failed check.")
                return 1

    size_kb = Path(args.db).stat().st_size / 1024
    print(f"\nOK: database ready at {args.db} ({size_kb:,.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
