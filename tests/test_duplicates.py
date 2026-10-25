"""Tests for Step 3: Duplicate Job Detection and Removal (Person 2).

These simple tests verify that duplicate postings are properly detected and removed,
unique postings are preserved, and row counts match expectations.
"""

import pandas as pd
import pytest

from src.transformation.detect_duplicates import (
    deduplicate_dataset,
    find_duplicates,
    remove_duplicates,
    resolve_dedup_subset,
)


@pytest.fixture
def sample_jobs_with_duplicates():
    """Sample DataFrame with 2 duplicate jobs and 2 unique jobs (4 total)."""
    return pd.DataFrame([
        {
            "posting_id": "job_1",
            "title": "Software Engineer",
            "company_name": "Tech Corp",
            "city": "Lahore",
            "posted_at": "2026-01-01",
        },
        {
            "posting_id": "job_2",  # Duplicate of job_1 (same title, company, city)
            "title": "Software Engineer",
            "company_name": "Tech Corp",
            "city": "Lahore",
            "posted_at": "2026-01-05",  # Reposted later
        },
        {
            "posting_id": "job_3",  # Same title and company, but different city
            "title": "Software Engineer",
            "company_name": "Tech Corp",
            "city": "Karachi",
            "posted_at": "2026-01-02",
        },
        {
            "posting_id": "job_4",  # Completely different job
            "title": "Data Analyst",
            "company_name": "Analytics Ltd",
            "city": "Islamabad",
            "posted_at": "2026-01-03",
        },
    ])


def test_find_duplicates_identifies_matching_posting(sample_jobs_with_duplicates):
    """Verify that find_duplicates correctly identifies duplicate rows."""
    df = sample_jobs_with_duplicates
    duplicates = find_duplicates(df, subset=["title", "company_name", "city"])

    assert len(duplicates) == 1
    assert duplicates["posting_id"].iloc[0] == "job_2"


def test_remove_duplicates_reduces_to_expected_rows(sample_jobs_with_duplicates):
    """Verify that removing duplicates produces the exact expected row count (4 -> 3)."""
    df = sample_jobs_with_duplicates
    deduped = remove_duplicates(df, subset=["title", "company_name", "city"])

    # 4 rows originally - 1 duplicate = 3 rows remaining
    assert len(deduped) == 3


def test_remove_duplicates_keeps_first_occurrence(sample_jobs_with_duplicates):
    """Verify that keep='first' preserves the earliest record and drops the second."""
    df = sample_jobs_with_duplicates
    deduped = remove_duplicates(df, subset=["title", "company_name", "city"], keep="first")

    # job_1 should be kept, job_2 should be dropped
    retained_ids = list(deduped["posting_id"])
    assert "job_1" in retained_ids
    assert "job_2" not in retained_ids
    assert "job_3" in retained_ids
    assert "job_4" in retained_ids


def test_unique_postings_all_preserved():
    """Verify that a dataset with no duplicates retains all original rows."""
    df_unique = pd.DataFrame([
        {"posting_id": "u1", "title": "DevOps Engineer", "company_name": "CloudTech", "city": "Lahore"},
        {"posting_id": "u2", "title": "QA Engineer", "company_name": "QualityFirst", "city": "Karachi"},
        {"posting_id": "u3", "title": "UI Designer", "company_name": "CreativeStudio", "city": "Islamabad"},
    ])

    duplicates = find_duplicates(df_unique, subset=["title", "company_name", "city"])
    deduped = remove_duplicates(df_unique, subset=["title", "company_name", "city"])

    assert len(duplicates) == 0
    assert len(deduped) == 3


def test_missing_values_handled_without_inventing_data():
    """Verify missing values (None / NaN) are preserved without inventing fake text or values."""
    df_with_nulls = pd.DataFrame([
        {
            "posting_id": "n1",
            "title": "Software Engineer",
            "company_name": None,  # Missing company
            "city": "Lahore",
            "salary_min": None,
        },
        {
            "posting_id": "n2",  # Duplicate of n1
            "title": "Software Engineer",
            "company_name": None,
            "city": "Lahore",
            "salary_min": None,
        },
        {
            "posting_id": "n3",  # Unique row
            "title": "Data Scientist",
            "company_name": "AI Labs",
            "city": None,
            "salary_min": None,
        },
    ])

    deduped = remove_duplicates(df_with_nulls, subset=["title", "company_name", "city"])

    assert len(deduped) == 2
    # Verify missing values remain missing (pd.isna) and are not filled with fake data
    assert pd.isna(deduped["salary_min"].iloc[0])
    assert pd.isna(deduped["company_name"].iloc[0])


def test_resolve_dedup_subset_prefers_standardized():
    """Verify resolve_dedup_subset chooses standardized columns when available."""
    df_with_std = pd.DataFrame({
        "title": ["A"],
        "standardized_title": ["A"],
        "company_name": ["C"],
        "city": ["L"],
        "standardized_city": ["L"],
    })
    cols = resolve_dedup_subset(df_with_std)
    assert cols == ["standardized_title", "company_name", "standardized_city"]


def test_deduplicate_dataset_helper(sample_jobs_with_duplicates):
    """Verify high-level deduplicate_dataset function returns both clean df and duplicates df."""
    df = sample_jobs_with_duplicates
    deduped_df, duplicates_df = deduplicate_dataset(df, subset=["title", "company_name", "city"])

    assert len(deduped_df) == 3
    assert len(duplicates_df) == 1
    assert duplicates_df["posting_id"].iloc[0] == "job_2"
