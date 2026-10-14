import pytest
from pydantic import ValidationError

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