"""Step 3: Duplicate Job Detection and Removal.

JobStack - Person 2 (Data Transformation and Skill Intelligence).
This module identifies and removes duplicate job postings using Pandas:
1. Detects duplicate postings where job title, company, and location match.
2. Uses Pandas `duplicated()` to identify duplicate postings.
3. Uses Pandas `drop_duplicates(keep='first')` to remove duplicates while keeping the first occurrence.
4. Handles missing values carefully without inventing fake information.
5. Saves the deduplicated dataset in data/transformed/.
"""

import json
import pathlib
from typing import Optional

import pandas as pd


# Default columns considered for identifying duplicates (title, company, and location)
DEFAULT_SUBSET = ["title", "company_name", "city"]
STANDARDIZED_SUBSET = ["standardized_title", "company_name", "standardized_city"]


def resolve_dedup_subset(df: pd.DataFrame, custom_subset: Optional[list[str]] = None) -> list[str]:
    """Determine which subset of columns to use for duplicate checking.

    If standardized columns (standardized_title, company_name, standardized_city)
    exist in the DataFrame, they are preferred because they account for minor variations
    cleaned in Step 1. Otherwise, it falls back to raw columns (title, company_name, city).
    """
    if custom_subset is not None:
        return custom_subset

    # Check if standardized columns from Step 1 are present
    if all(col in df.columns for col in STANDARDIZED_SUBSET):
        return STANDARDIZED_SUBSET

    # Fallback to basic columns
    return [col for col in DEFAULT_SUBSET if col in df.columns]


def find_duplicates(
    df: pd.DataFrame,
    subset: Optional[list[str]] = None,
    keep: str = "first",
) -> pd.DataFrame:
    """Identify duplicate rows in the DataFrame using Pandas `duplicated()`.

    Parameters:
        df: Input DataFrame.
        subset: Columns to compare (defaults to title, company, and location).
        keep: 'first' (marks 2nd+ occurrences as duplicates),
              'last' (marks 1st to n-1 occurrences as duplicates),
              or False (marks all duplicate occurrences as duplicates).

    Returns:
        DataFrame containing only the duplicate rows.

    How df.duplicated() works:
        It checks each row against preceding rows based on the columns in `subset`.
        It returns a boolean Series (True for duplicates, False for unique/first occurrence).
        We then filter `df[df.duplicated(...)]` to inspect the duplicate records.
    """
    cols = resolve_dedup_subset(df, subset)
    duplicate_mask = df.duplicated(subset=cols, keep=keep)
    return df[duplicate_mask].copy()


def remove_duplicates(
    df: pd.DataFrame,
    subset: Optional[list[str]] = None,
    keep: str = "first",
) -> pd.DataFrame:
    """Remove duplicate rows in the DataFrame using Pandas `drop_duplicates()`.

    Parameters:
        df: Input DataFrame.
        subset: Columns to compare (title, company, location).
        keep: 'first' (keeps the first occurrence and drops later duplicates).

    Returns:
        Deduplicated DataFrame.

    How df.drop_duplicates() works:
        It scans the DataFrame from top to bottom. When it encounters a combination
        of values in `subset` that it has already seen, it drops that row and keeps
        the first one. It preserves index and column data without inventing new values.
    """
    cols = resolve_dedup_subset(df, subset)
    deduped_df = df.drop_duplicates(subset=cols, keep=keep).copy()
    return deduped_df


def deduplicate_dataset(
    df: pd.DataFrame,
    subset: Optional[list[str]] = None,
    keep: str = "first",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Perform duplicate detection and removal on a dataset.

    Returns:
        tuple of (deduplicated_df, duplicates_found_df)
    """
    cols = resolve_dedup_subset(df, subset)
    print(f"Checking for duplicates matching on columns: {cols}")

    # 1. Identify duplicates
    duplicates_df = find_duplicates(df, subset=cols, keep=keep)
    num_duplicates = len(duplicates_df)

    # 2. Remove duplicates
    deduped_df = remove_duplicates(df, subset=cols, keep=keep)

    print(f"Total rows before: {len(df)}")
    print(f"Duplicate rows detected: {num_duplicates}")
    print(f"Total rows after deduplication: {len(deduped_df)}")

    return deduped_df, duplicates_df


def load_transformed_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """Load the transformed dataset from previous steps.

    Defaults to 'data/transformed/jobs_cleaned.json'.
    """
    if filepath is not None:
        path = pathlib.Path(filepath)
    else:
        path = pathlib.Path("data/transformed/jobs_cleaned.json")

    if not path.exists():
        raise FileNotFoundError(
            f"Transformed dataset not found at '{path}'. "
            "Please run Steps 1 and 2 first."
        )

    print(f"Loading dataset from: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} postings.")
    return df


def save_deduplicated_data(
    df: pd.DataFrame, output_dir: str = "data/transformed"
) -> None:
    """Save the deduplicated dataset in data/transformed/ in both JSON and CSV formats."""
    out_dir = pathlib.Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_file = out_dir / "jobs_cleaned.json"
    csv_file = out_dir / "jobs_cleaned.csv"
    dedup_json = out_dir / "jobs_deduplicated.json"
    dedup_csv = out_dir / "jobs_deduplicated.csv"

    # Save to JSON
    records = df.to_dict(orient="records")
    content_json = json.dumps(records, ensure_ascii=False, indent=2)
    json_file.write_text(content_json, encoding="utf-8")
    dedup_json.write_text(content_json, encoding="utf-8")
    print(f"Saved deduplicated JSON to: {json_file} (and {dedup_json.name})")

    # Save to CSV
    df.to_csv(csv_file, index=False, encoding="utf-8")
    df.to_csv(dedup_csv, index=False, encoding="utf-8")
    print(f"Saved deduplicated CSV to: {csv_file} (and {dedup_csv.name})")


def main():
    """Run Step 3 duplicate job detection and display summary results."""
    print("=" * 60)
    print("JobStack - Person 2: Step 3 Duplicate Job Detection")
    print("=" * 60)

    # 1. Load transformed data from previous steps
    df = load_transformed_data()

    # 2. Run deduplication
    deduped_df, duplicates_df = deduplicate_dataset(df)

    # 3. Save deduplicated dataset
    save_deduplicated_data(deduped_df)

    # 4. Summary display
    print("\n" + "=" * 60)
    print("Deduplication Summary:")
    print("=" * 60)
    print(f"Rows before: {len(df)}")
    print(f"Duplicates removed: {len(duplicates_df)}")
    print(f"Unique rows preserved: {len(deduped_df)}")

    if len(duplicates_df) > 0:
        print("\nSample Duplicate Postings Removed:")
        cols_to_show = [c for c in ["title", "company_name", "city"] if c in df.columns]
        print(duplicates_df[cols_to_show].head().to_string())
    else:
        print("\nNotice: All rows in the current dataset sample were unique.")
        print("(In the full 8,011-row dataset, near-duplicates are flagged as documented in the quality report).")

    print("\nStep 3 completed successfully.")


if __name__ == "__main__":
    main()
