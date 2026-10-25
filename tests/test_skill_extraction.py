"""Tests for Step 2: Skill Extraction (Person 2).

These tests verify simple string-matching skill extraction using ordinary pytest assertions.
"""

import pandas as pd
import pytest

from src.transformation.extract_skills import (
    SKILL_DICTIONARY,
    add_extracted_skills_column,
    extract_skills_from_text,
)


def test_extract_multiple_skills():
    """Verify that multiple skills can be extracted from a single description."""
    text = (
        "We are looking for a Software Engineer proficient in Python, SQL, and Pandas. "
        "The candidate must have strong communication skills and be a good team player."
    )
    result = extract_skills_from_text(text)
    assert result == ["Communication", "Pandas", "Python", "SQL", "Teamwork"]


def test_extract_no_recognized_skills():
    """Verify that a description with no matching skills returns an empty list []."""
    text = "We are seeking a commercial delivery driver with a clean driving record."
    result = extract_skills_from_text(text)
    assert result == []


def test_extract_skills_empty_or_none():
    """Verify that None, empty string, or whitespace returns an empty list without crashing."""
    assert extract_skills_from_text(None) == []
    assert extract_skills_from_text("") == []
    assert extract_skills_from_text("     ") == []


def test_word_boundary_prevents_false_positives():
    """Verify that 'Java' is NOT falsely matched when the text only mentions 'JavaScript'."""
    text = "Must have deep knowledge of JavaScript and React."
    result = extract_skills_from_text(text)

    # 'JavaScript' and 'React' should be detected, but 'Java' must NOT be detected
    assert "JavaScript" in result
    assert "React" in result
    assert "Java" not in result


def test_case_insensitivity():
    """Verify that skill matching works regardless of letter casing."""
    text = "Required experience: pYtHoN, SqL, ExCeL, and TeAmWoRk."
    result = extract_skills_from_text(text)
    assert result == ["Excel", "Python", "SQL", "Teamwork"]


def test_core_required_skills_in_dictionary():
    """Verify that all core required skills exist in SKILL_DICTIONARY."""
    required = [
        "Python",
        "SQL",
        "Java",
        "JavaScript",
        "React",
        "Excel",
        "Pandas",
        "Communication",
        "Teamwork",
    ]
    for skill in required:
        assert skill in SKILL_DICTIONARY
        # Verify that extracting text containing that skill works
        matched = extract_skills_from_text(f"Must have experience with {skill}.")
        assert skill in matched


def test_add_extracted_skills_column():
    """Verify adding the extracted_skills column to a pandas DataFrame."""
    df = pd.DataFrame([
        {
            "posting_id": "1",
            "title": "Backend Engineer",
            "cleaned_description": "We build scalable APIs using Python and Docker.",
        },
        {
            "posting_id": "2",
            "title": "Office Clerical Assistant",
            "cleaned_description": "General office duties and filing documents.",
        },
    ])

    df_out = add_extracted_skills_column(df)

    assert "extracted_skills" in df_out.columns
    assert df_out["extracted_skills"].iloc[0] == ["Docker", "Python"]
    assert df_out["extracted_skills"].iloc[1] == []
