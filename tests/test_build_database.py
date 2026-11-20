"""Test the one-command database build (deploy/build_database.py)."""
import importlib.util
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_database", ROOT / "deploy" / "build_database.py")
build_database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_database)


def test_build_creates_verified_database(tmp_path):
    db = tmp_path / "test.db"
    assert build_database.main(["--db", str(db)]) == 0
    con = sqlite3.connect(db)
    try:
        assert con.execute("SELECT COUNT(*) FROM postings").fetchone()[0] > 0
        names = {r[0] for r in con.execute("SELECT name FROM sqlite_master")}
        assert {"postings", "skills", "posting_skills", "v_skill_counts"} <= names
    finally:
        con.close()
