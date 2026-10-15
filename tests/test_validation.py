import pytest
from pydantic import ValidationError

from src.ingestion.arbeitnow_adapter import detect_language, to_record
from src.ingestion.kaggle_adapter import clean_title
from src.ingestion.kaggle_adapter import to_record as kaggle_record
from src.validation.models import JobPosting


def make(**kw):
    base = dict(posting_id="1", source="remotive", title="Data Analyst", description="Work with data")
    base.update(kw)
    return JobPosting(**base)


def test_valid_record():
    assert make().title == "Data Analyst"


def test_blank_title_rejected():
    with pytest.raises(ValidationError):
        make(title="   ")


def test_bad_salary_range_rejected():
    with pytest.raises(ValidationError):
        make(salary_min=100, salary_max=50)


def test_negative_salary_rejected():
    with pytest.raises(ValidationError):
        make(salary_min=-5)


def test_future_date_rejected():
    with pytest.raises(ValidationError):
        make(posted_at="2999-01-01T00:00:00")


def test_german_detected():
    assert detect_language("Wir suchen dich und deine Hilfe für die Arbeit mit der Kasse") == "de"


def test_arbeitnow_record_validates():
    raw = {"slug": "x-1", "title": "Dev", "description": "Build things for the team and ship them",
           "remote": True, "created_at": 1791982885, "tags": ["Web Development"],
           "job_types": ["Full-time"], "location": "Berlin"}
    assert JobPosting(**to_record(raw)).work_mode == "remote"


def test_clean_title():
    assert clean_title("Full Time Senior Web Developer Jobs in Pakistan") == "Senior Web Developer"


def test_kaggle_record_validates():
    raw = {"_id": "abc123", "Job Name": "Full Time Senior Web Developer Jobs in Pakistan",
           "Company Name": "Eurosoft Tech Private Limited, Pakistan", "Job Type": "Full Time Jobs",
           "Experience Required": "2 Years Job Exp.", "Department": "IT Jobs",
           "JD": "We are looking for an experienced Web Developer.", "City": "Karachi",
           "Date Posted": "12-Mar-21"}
    job = JobPosting(**kaggle_record(raw))
    assert job.company_name == "Eurosoft Tech Private Limited"
    assert job.country == "Pakistan"
    assert job.posted_at.year == 2021


def test_arbeitnow_remote_location_becomes_work_mode():
    raw = {"slug": "x-2", "title": "Dev", "description": "Build things", "remote": False,
           "location": "Remote", "created_at": 1791982885}
    rec = to_record(raw)
    assert rec["city"] is None
    assert rec["work_mode"] == "remote"


def test_clean_title_singular_job():
    assert clean_title("Accounts Officer Job in Pakistan") == "Accounts Officer"


def test_kaggle_category_and_type_strip_singular_job():
    raw = {"_id": "z", "Job Name": "Tea Boy", "Company Name": "Acme", "Job Type": "Full Time Job",
           "Department": "IT Job", "JD": "Make tea", "City": "Lahore", "Date Posted": "01-Jan-21"}
    rec = kaggle_record(raw)
    assert rec["employment_type"] == "Full Time"
    assert rec["category"] == "IT"