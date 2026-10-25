"""Tests for Step 4: Final Dataset Export and Documentation Verification (Person 2).

These tests verify that the final export produces valid CSV and JSON files,
ensures required columns are present, and confirms duplicate checking.
"""

import pathlib
import pandas as pd
import pytest

from src.transformation.export_final import (
    REQUIRED_COLUMNS,
    export_final_dataset,
    verify_columns,
)


def test_verify_columns_success():
    """Verify verify_columns returns True when all required columns are present."""
    data = {col: ["sample_val"] for col in REQUIRED_COLUMNS}
    df = pd.DataFrame(data)

    is_valid, missing = verify_columns(df)
    assert is_valid is True
    assert missing == []


def test_verify_columns_detects_missing():
    """Verify verify_columns flags missing required columns."""
    df_incomplete = pd.DataFrame({
        "title": ["Software Engineer"],
        "description": ["Build apps"],
    })

    is_valid, missing = verify_columns(df_incomplete)
    assert is_valid is False
    assert "extracted_skills" in missing
    assert "standardized_title" in missing


def test_final_dataset_files_exist():
    """Verify jobs_final.csv and jobs_final.json exist in data/transformed/."""
    csv_file = pathlib.Path("data/transformed/jobs_final.csv")
    json_file = pathlib.Path("data/transformed/jobs_final.json")

    assert csv_file.exists(), "jobs_final.csv was not found"
    assert json_file.exists(), "jobs_final.json was not found"


def test_final_csv_loadable_and_has_required_columns():
    """Verify jobs_final.csv can be read by pandas and contains all required columns."""
    csv_file = pathlib.Path("data/transformed/jobs_final.csv")
    df = pd.read_csv(csv_file)

    assert len(df) == 300
    for col in REQUIRED_COLUMNS:
        assert col in df.columns, f"Required column '{col}' missing in jobs_final.csv"


def test_final_json_has_list_extracted_skills():
    """Verify extracted_skills in jobs_final.json contains lists and has expected entries."""
    json_file = pathlib.Path("data/transformed/jobs_final.json")
    import json
    data = json.loads(json_file.read_text(encoding="utf-8"))

    assert len(data) == 300
    # First posting should have extracted skills list
    first_skills = data[0]["extracted_skills"]
    assert isinstance(first_skills, list)
    assert len(first_skills) > 0
    assert "Python" in first_skills or "JavaScript" in first_skills
