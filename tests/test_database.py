"""Tests for the SQL database build and load (Person 3). Uses a tiny fake dataset and a temp file."""

import sqlite3

import pytest

from src.database.load_database import build_database

NAN = float("nan")


def make_record(posting_id, **overrides):
    record = {
        "posting_id": posting_id, "source": "kaggle_pk", "source_url": None,
        "title": "Data Engineer", "standardized_title": "Data Engineer",
        "cleaned_description": "Some text", "company_name": "Acme", "category": "IT",
        "standardized_city": "Lahore", "country": "Pakistan", "experience": None,
        "standardized_employment_type": "Full-time", "standardized_work_mode": "unknown",
        "posted_at": "2026-01-01T00:00:00", "language": "en",
        "salary_min": NAN, "salary_max": NAN, "currency": NAN, "salary_text": NAN,
        "extracted_skills": [],
    }
    record.update(overrides)
    return record


def test_counts_links_and_nulls(tmp_path):
    records = [
        make_record("1", extracted_skills=["Python", "SQL"]),
        make_record("2", extracted_skills=["Python"]),
        make_record("3", company_name=NAN, standardized_city=NAN, country=NAN,
                    salary_text="OTE $25k - $35k"),
    ]
    db = tmp_path / "t.db"
    result = build_database(records, db)
    assert result["counts"] == {
        "companies": 1, "locations": 1, "skills": 2,
        "postings": 3, "posting_skills": 3, "salary_observations": 1,
    }
    assert all(ok for _, ok, _ in result["qa"])

    con = sqlite3.connect(db)
    row = con.execute(
        "SELECT company_id, location_id FROM postings WHERE source_posting_id = '3'"
    ).fetchone()
    assert row == (None, None)                       # unknown company/city stay NULL
    salary = con.execute("SELECT salary_min, salary_text FROM salary_observations").fetchone()
    assert salary == (None, "OTE $25k - $35k")       # missing salary is NULL, never 0
    con.close()


def test_null_country_does_not_create_duplicate_locations(tmp_path):
    records = [
        make_record("1", standardized_city="London", country=NAN, source="arbeitnow"),
        make_record("2", standardized_city="London", country=NAN, source="arbeitnow"),
    ]
    result = build_database(records, tmp_path / "t.db")
    assert result["counts"]["locations"] == 1


def test_same_posting_id_in_two_sources_is_allowed(tmp_path):
    records = [make_record("1", source="kaggle_pk"), make_record("1", source="arbeitnow")]
    assert build_database(records, tmp_path / "t.db")["counts"]["postings"] == 2


def test_same_source_and_posting_id_twice_is_rejected(tmp_path):
    records = [make_record("1"), make_record("1")]
    with pytest.raises(sqlite3.IntegrityError):
        build_database(records, tmp_path / "t.db")


def test_foreign_keys_and_checks_are_enforced(tmp_path):
    db = tmp_path / "t.db"
    build_database([make_record("1")], db)
    con = sqlite3.connect(db)
    con.execute("PRAGMA foreign_keys = ON")
    with pytest.raises(sqlite3.IntegrityError):      # skill_id 999 does not exist
        con.execute("INSERT INTO posting_skills (posting_pk, skill_id) VALUES (1, 999)")
    with pytest.raises(sqlite3.IntegrityError):      # invalid work_mode
        con.execute(
            "INSERT INTO postings (source, source_posting_id, title, description, work_mode) "
            "VALUES ('x', 'y', 't', 'd', 'sometimes')"
        )
    con.close()


def test_missing_required_column_gives_clear_error(tmp_path):
    bad = make_record("1")
    del bad["extracted_skills"]
    with pytest.raises(ValueError):
        build_database([bad], tmp_path / "t.db")
