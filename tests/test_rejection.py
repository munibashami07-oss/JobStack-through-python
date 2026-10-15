"""Rejection tests for the JobPosting validation model.

The real data produced 0 rejected records (0 of 8,011), so the rejection path
never ran on real data. These tests feed deliberately broken records to the
model and check that each one is refused WITH a readable reason, that a bad
record does not stop good records from passing, and that missing salary stays
missing (None) and is never turned into 0.
"""
import pytest
from pydantic import ValidationError

from src.validation.models import JobPosting

GOOD = dict(
    posting_id="1",
    source="remotive",
    title="Data Analyst",
    description="Work with data",
)


def make(**overrides):
    return JobPosting(**{**GOOD, **overrides})


def reasons(record: dict) -> list[str]:
    """Validate a record and return readable 'field: message' reasons.

    Returns an empty list when the record is valid.
    """
    try:
        JobPosting(**record)
    except ValidationError as exc:
        return [
            f"{'.'.join(str(p) for p in e['loc']) or 'record'}: {e['msg']}"
            for e in exc.errors()
        ]
    return []


# --- one bad record per rule: must be rejected, with the right reason -------

BAD_CASES = [
    pytest.param({"title": "   "}, "title", "must not be empty", id="blank-title"),
    pytest.param({"title": ""}, "title", "must not be empty", id="empty-title"),
    pytest.param({"description": "  "}, "description", "must not be empty", id="blank-description"),
    pytest.param({"salary_min": -1}, "salary_min", "must not be negative", id="negative-salary-min"),
    pytest.param({"salary_max": -1}, "salary_max", "must not be negative", id="negative-salary-max"),
    pytest.param({"salary_min": 100, "salary_max": 50}, "record", "greater than", id="min-above-max"),
    pytest.param({"salary_min": "abc"}, "salary_min", "", id="non-numeric-salary"),
    pytest.param({"posted_at": "2999-01-01T00:00:00"}, "posted_at", "in the future", id="future-date"),
    pytest.param({"posted_at": "not-a-date"}, "posted_at", "", id="invalid-date"),
    pytest.param({"work_mode": "office"}, "work_mode", "", id="bad-work-mode"),
    pytest.param({"source": "linkedin"}, "source", "", id="unknown-source"),
    pytest.param({"language": "fr"}, "language", "", id="unsupported-language"),
]


@pytest.mark.parametrize("overrides, field, message", BAD_CASES)
def test_bad_record_is_rejected_with_reason(overrides, field, message):
    found = reasons({**GOOD, **overrides})
    assert found, "record should have been rejected"
    assert any(r.startswith(field) and message in r for r in found), found


@pytest.mark.parametrize("missing", ["posting_id", "source", "title", "description"])
def test_missing_required_field_is_rejected(missing):
    record = {k: v for k, v in GOOD.items() if k != missing}
    found = reasons(record)
    assert any(r.startswith(missing) for r in found), found


def test_all_problems_are_reported_not_just_the_first():
    found = reasons({**GOOD, "title": " ", "salary_min": -5, "work_mode": "office"})
    assert len(found) >= 3, found


# --- valid records must still pass (rules are not too strict) ---------------

def test_good_record_passes_and_has_no_reasons():
    assert reasons(GOOD) == []


def test_equal_salary_min_and_max_is_allowed():
    assert make(salary_min=100, salary_max=100).salary_max == 100


def test_past_date_is_allowed():
    assert make(posted_at="2021-03-12T00:00:00").posted_at.year == 2021


def test_title_whitespace_is_stripped():
    assert make(title="  Data Analyst  ").title == "Data Analyst"


# --- missing salary must stay missing ----------------------------------------

def test_missing_salary_stays_none_not_zero():
    job = make()
    assert job.salary_min is None
    assert job.salary_max is None


def test_salary_text_alone_does_not_create_numeric_salary():
    job = make(salary_text="$60k - $80k")
    assert job.salary_text == "$60k - $80k"
    assert job.salary_min is None and job.salary_max is None


# --- a bad record must not stop the rest of the run --------------------------

def test_one_bad_record_does_not_stop_the_batch():
    batch = [
        {**GOOD, "posting_id": "a"},
        {**GOOD, "posting_id": "b", "title": ""},
        {**GOOD, "posting_id": "c"},
        {**GOOD, "posting_id": "d", "salary_min": 9, "salary_max": 1},
        {**GOOD, "posting_id": "e"},
    ]
    valid, rejected = [], []
    for rec in batch:
        found = reasons(rec)
        if found:
            rejected.append({"record": rec, "reasons": found})
        else:
            valid.append(rec)

    assert [r["posting_id"] for r in valid] == ["a", "c", "e"]
    assert [r["record"]["posting_id"] for r in rejected] == ["b", "d"]
    assert all(r["reasons"] for r in rejected)