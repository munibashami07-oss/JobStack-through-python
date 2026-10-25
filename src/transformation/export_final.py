"""Step 4: Final Dataset Export and Pipeline Verification.

JobStack - Person 2 (Data Transformation and Skill Intelligence).
This module performs the final export and verification:
1. Loads the transformed dataset from previous steps.
2. Verifies that all required columns are present (cleaned info, standardized columns, and extracted_skills).
3. Applies / confirms duplicate detection (matching title, company, location; keeping first).
4. Exports the final production-ready dataset as:
   - data/transformed/jobs_final.csv
   - data/transformed/jobs_final.json
5. Reports row counts before and after deduplication and summarizes column integrity.
"""

import json
import pathlib
import sys
from typing import Optional

import pandas as pd

from src.transformation.detect_duplicates import (
    deduplicate_dataset,
    resolve_dedup_subset,
)

# Essential required columns for downstream consumers (Person 3, Person 4, Database, API)
REQUIRED_COLUMNS = [
    "posting_id",
    "source",
    "title",
    "standardized_title",
    "description",
    "cleaned_description",
    "company_name",
    "city",
    "standardized_city",
    "work_mode",
    "standardized_work_mode",
    "employment_type",
    "standardized_employment_type",
    "extracted_skills",
    "posted_at",
]


def verify_columns(df: pd.DataFrame, required: list[str] = REQUIRED_COLUMNS) -> tuple[bool, list[str]]:
    """Check that all required transformed columns exist in the DataFrame.

    Returns:
        tuple of (is_valid: bool, missing_columns: list[str])
    """
    missing = [col for col in required if col not in df.columns]
    is_valid = len(missing) == 0
    return is_valid, missing


def export_final_dataset(
    input_path: Optional[str] = None,
    output_dir: str = "data/transformed",
) -> tuple[pd.DataFrame, dict]:
    """Load transformed data, apply final deduplication, verify schema, and export jobs_final.csv / .json.

    Returns:
        tuple of (final_df: pd.DataFrame, report_stats: dict)
    """
    out_dir = pathlib.Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Determine input path
    if input_path is not None:
        src = pathlib.Path(input_path)
    else:
        src = out_dir / "jobs_cleaned.json"

    if not src.exists():
        raise FileNotFoundError(
            f"Transformed dataset not found at '{src}'. "
            "Please ensure Steps 1 to 3 have run."
        )

    print(f"Loading data from: {src}")
    data = json.loads(src.read_text(encoding="utf-8"))
    df = pd.DataFrame(data)
    initial_rows = len(df)
    print(f"Initial row count: {initial_rows}")

    # 2. Verify required columns
    is_valid, missing_cols = verify_columns(df)
    if not is_valid:
        raise ValueError(
            f"Dataset is missing required columns from earlier steps: {missing_cols}"
        )
    print("All required columns verified successfully.")

    # 3. Apply / confirm duplicate removal (title + company + city, keep='first')
    dedup_subset = resolve_dedup_subset(df)
    deduped_df, duplicates_df = deduplicate_dataset(df, subset=dedup_subset, keep="first")
    final_rows = len(deduped_df)
    duplicates_removed = len(duplicates_df)

    # 4. Save final output files
    final_csv = out_dir / "jobs_final.csv"
    final_json = out_dir / "jobs_final.json"

    # Export CSV
    deduped_df.to_csv(final_csv, index=False, encoding="utf-8")
    print(f"Exported final CSV: {final_csv}")

    # Export JSON (ensure_ascii=False for proper unicode handling)
    records = deduped_df.to_dict(orient="records")
    final_json.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported final JSON: {final_json}")

    # 5. Compile stats dictionary
    stats = {
        "initial_rows": initial_rows,
        "final_rows": final_rows,
        "duplicates_removed": duplicates_removed,
        "dedup_columns": dedup_subset,
        "total_columns": len(deduped_df.columns),
        "postings_with_skills": int((deduped_df["extracted_skills"].apply(len) > 0).sum()),
        "postings_without_skills": int((deduped_df["extracted_skills"].apply(len) == 0).sum()),
    }

    return deduped_df, stats


def main():
    """Run Step 4 final export and display summary."""
    print("=" * 60)
    print("JobStack - Person 2: Step 4 Final Dataset Export")
    print("=" * 60)

    try:
        final_df, stats = export_final_dataset()
    except Exception as e:
        print(f"Error during export: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Final Export Summary:")
    print("=" * 60)
    print(f"Initial Rows:             {stats['initial_rows']}")
    print(f"Duplicate Rows Removed:   {stats['duplicates_removed']}")
    print(f"Final Retained Rows:      {stats['final_rows']}")
    print(f"Total Columns:            {stats['total_columns']}")
    print(f"Deduplication Match Keys: {stats['dedup_columns']}")
    print(f"Postings with Skills:     {stats['postings_with_skills']} ({stats['postings_with_skills'] / stats['final_rows'] * 100:.1f}%)")
    print(f"Postings without Skills:  {stats['postings_without_skills']} ({stats['postings_without_skills'] / stats['final_rows'] * 100:.1f}%)")

    print("\nOutput Files Created:")
    print("  - data/transformed/jobs_final.csv")
    print("  - data/transformed/jobs_final.json")
    print("\nStep 4 completed successfully.")


if __name__ == "__main__":
    main()
