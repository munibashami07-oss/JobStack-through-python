"""Tests for Step 1 data cleaning and standardization (Person 2).

These simple tests verify each cleaning function using ordinary pytest assertions.
"""

import pandas as pd
import pytest

from src.transformation.clean_data import (
    clean_dataset,
    clean_html_and_whitespace,
    handle_missing_values,
    standardize_employment_type,
    standardize_job_title,
    standardize_location,
    standardize_work_mode,
)


# ==============================================================================
# 1. HTML & Whitespace Cleaning Tests
# ==============================================================================

def test_clean_html_tags_removed():
    raw = "<p>Join our team as a <strong>Python Developer</strong>.<br>Apply now!</p>"
    expected = "Join our team as a Python Developer . Apply now!"
    assert clean_html_and_whitespace(raw) == expected


def test_clean_html_entities_decoded():
    raw = "Skills needed: Python &amp; SQL &nbsp; (FastAPI &lt; 1.0)"
    expected = "Skills needed: Python & SQL (FastAPI < 1.0)"
    assert clean_html_and_whitespace(raw) == expected


def test_clean_whitespace_collapsed():
    raw = "   Senior    Software   \n\n   Engineer   \t\t "
    expected = "Senior Software Engineer"
    assert clean_html_and_whitespace(raw) == expected


def test_clean_html_none_and_empty():
    assert clean_html_and_whitespace(None) is None
    assert clean_html_and_whitespace("   ") is None
    assert clean_html_and_whitespace("") is None


# ==============================================================================
# 2. Job Title Standardization Tests
# ==============================================================================

def test_standardize_job_title_known_mapping():
    assert standardize_job_title("software developer") == "Software Engineer"
    assert standardize_job_title("Senior .NET Full-stack Developer") == "Full Stack Developer"
    assert standardize_job_title("qa engineer") == "QA Engineer"
    assert standardize_job_title("data scientist") == "Data Scientist"


def test_standardize_job_title_gender_noise_removed():
    assert standardize_job_title("Marketing Manager (m/w/d)") == "Marketing Manager"
    assert standardize_job_title("Senior Key Account Manager (m|w|d)") == "Senior Key Account Manager"


def test_standardize_job_title_unmapped_preserved():
    # If the title is not in the dictionary, it should preserve the cleaned title
    assert standardize_job_title("Autocad Draftsman") == "Autocad Draftsman"
    assert standardize_job_title(None) is None


# ==============================================================================
# 3. Location Standardization Tests
# ==============================================================================

def test_standardize_location_pakistan_cities():
    assert standardize_location("Lahore, Pakistan") == "Lahore"
    assert standardize_location("karachi, pakistan") == "Karachi"
    assert standardize_location("Islamabad") == "Islamabad"


def test_standardize_location_international_cities():
    assert standardize_location("Berlin, Berlin, Germany") == "Berlin"
    assert standardize_location("Munich (DEU)") == "Munich"
    assert standardize_location("Hybrid London") == "London"


def test_standardize_location_missing_not_invented():
    # Crucial rule: Missing location remains None, never fabricated
    assert standardize_location(None) is None
    assert standardize_location("   ") is None


# ==============================================================================
# 4. Employment Type Standardization Tests
# ==============================================================================

def test_standardize_employment_type_fulltime():
    assert standardize_employment_type("full_time") == "Full-time"
    assert standardize_employment_type("Experienced, Permanent, Full time") == "Full-time"
    assert standardize_employment_type("unbefristeter arbeitsvertrag") == "Full-time"


def test_standardize_employment_type_parttime():
    assert standardize_employment_type("Part Time") == "Part-time"
    assert standardize_employment_type("werkstudent") == "Part-time"


def test_standardize_employment_type_contract_and_internship():
    assert standardize_employment_type("freelance") == "Contract"
    assert standardize_employment_type("FR Intern") == "Internship"


# ==============================================================================
# 5. Work Mode Standardization Tests
# ==============================================================================

def test_standardize_work_mode_remote_variations():
    assert standardize_work_mode("remote") == "remote"
    assert standardize_work_mode("100 % remote") == "remote"
    assert standardize_work_mode("WFH") == "remote"


def test_standardize_work_mode_onsite_and_hybrid():
    assert standardize_work_mode("in-office") == "onsite"
    assert standardize_work_mode("Hybrid") == "hybrid"


def test_standardize_work_mode_unknown():
    assert standardize_work_mode(None) == "unknown"
    assert standardize_work_mode("Not specified") == "unknown"


# ==============================================================================
# 6. Missing Values & Preservation of Originals
# ==============================================================================

def test_missing_salary_is_not_zero():
    # As per data contract: "Missing salary is null, never 0"
    df = pd.DataFrame([
        {"salary_min": None, "salary_max": None, "city": "   ", "tags": None}
    ])
    cleaned = handle_missing_values(df)

    assert cleaned["salary_min"].iloc[0] is None
    assert cleaned["salary_max"].iloc[0] is None
    assert cleaned["city"].iloc[0] is None
    assert cleaned["tags"].iloc[0] == []


def test_clean_dataset_preserves_original_columns():
    df = pd.DataFrame([
        {
            "posting_id": "1",
            "source": "kaggle_pk",
            "title": "software developer",
            "city": "Lahore, Pakistan",
            "employment_type": "full_time",
            "work_mode": "100 % remote",
            "description": "<p>Build great software with Python &amp; SQL.</p>",
            "salary_min": None,
        }
    ])
    result = clean_dataset(df)

    # Originals preserved
    assert result["title"].iloc[0] == "software developer"
    assert result["city"].iloc[0] == "Lahore, Pakistan"
    assert result["employment_type"].iloc[0] == "full_time"
    assert result["work_mode"].iloc[0] == "100 % remote"
    assert "<p>" in result["description"].iloc[0]

    # Standardized columns added
    assert result["standardized_title"].iloc[0] == "Software Engineer"
    assert result["standardized_city"].iloc[0] == "Lahore"
    assert result["standardized_employment_type"].iloc[0] == "Full-time"
    assert result["standardized_work_mode"].iloc[0] == "remote"
    assert result["cleaned_description"].iloc[0] == "Build great software with Python & SQL."
