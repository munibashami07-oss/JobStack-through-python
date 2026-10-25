"""Step 2: Simple Skill Extraction.

JobStack - Person 2 (Data Transformation and Skill Intelligence).
This module extracts skills from cleaned job descriptions:
1. Defines a beginner-friendly dictionary of common technical and soft skills.
2. Uses simple string matching with word boundaries so 'Java' does not match inside 'JavaScript'.
3. Adds an 'extracted_skills' column with a list of matched skills (or [] if none found).
4. Updates and saves the dataset in data/transformed/.
"""

import json
import pathlib
import re
from typing import Optional

import pandas as pd


# ==============================================================================
# 1. Simple Skill Dictionary
# ==============================================================================

# Dictionary mapping canonical skill name -> search keywords / variations
SKILL_DICTIONARY = {
    # Core programming languages
    "Python": ["python"],
    "SQL": ["sql"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "C++": ["c++"],
    "C#": ["c#"],
    "PHP": ["php"],

    # Frameworks & Libraries
    "React": ["react", "reactjs", "react.js"],
    "Pandas": ["pandas"],
    "Node.js": ["node.js", "nodejs"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],

    # Tools, Platforms & Data
    "Excel": ["excel", "ms excel", "microsoft excel"],
    "Git": ["git", "github", "gitlab"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
    "Linux": ["linux"],

    # Soft skills & Methodologies
    "Communication": ["communication", "communicating", "verbal communication"],
    "Teamwork": ["teamwork", "team player", "collaboration"],
    "Problem Solving": ["problem solving", "analytical skills"],
}


# ==============================================================================
# 2. Skill Extraction Function
# ==============================================================================

def extract_skills_from_text(text: Optional[str]) -> list[str]:
    """Search for skills from SKILL_DICTIONARY in a text string.

    Parameters:
        text: Job description string (e.g. 'Looking for Python and SQL developer').

    Returns:
        Sorted list of matched canonical skill names, or an empty list [] if none found.

    Design notes:
        - We lowercase both the text and keywords so search is case-insensitive.
        - We use regex word boundaries (?<!\\w) and (?!\\w) to ensure 'java' does
          not falsely match inside 'javascript'.
        - If no skills are found, it returns [], never inventing skills.

    Example:
        >>> extract_skills_from_text("We need a developer with Python, SQL, and teamwork skills.")
        ['Communication', 'Python', 'SQL', 'Teamwork']
    """
    if text is None or not isinstance(text, str):
        return []

    cleaned_text = text.strip()
    if not cleaned_text:
        return []

    text_lower = cleaned_text.lower()
    found_skills = []

    # Check each skill and its variations
    for canonical_name, aliases in SKILL_DICTIONARY.items():
        for alias in aliases:
            # Word boundary regex: ensures the keyword is a standalone word
            # (?<!\w) means "not preceded by an alphanumeric character"
            # (?!\w) means "not followed by an alphanumeric character"
            pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"

            if re.search(pattern, text_lower):
                found_skills.append(canonical_name)
                # Break to avoid adding the same canonical skill twice if multiple aliases match
                break

    return sorted(found_skills)


# ==============================================================================
# 3. DataFrame Pipeline
# ==============================================================================

def add_extracted_skills_column(
    df: pd.DataFrame, description_col: str = "cleaned_description"
) -> pd.DataFrame:
    """Add the 'extracted_skills' column to the DataFrame.

    Parameters:
        df: DataFrame containing job postings.
        description_col: Column to search (defaults to 'cleaned_description',
                         falls back to 'description' if cleaned is absent).

    Returns:
        DataFrame with the new 'extracted_skills' column.
    """
    df = df.copy()

    # Determine which description column to search
    target_col = description_col if description_col in df.columns else "description"
    if target_col not in df.columns:
        raise KeyError("Neither 'cleaned_description' nor 'description' found in DataFrame.")

    print(f"Extracting skills using column: '{target_col}'...")

    # Apply skill extraction row-by-row
    df["extracted_skills"] = df[target_col].apply(extract_skills_from_text)

    return df


# ==============================================================================
# 4. File I/O Helpers
# ==============================================================================

def load_cleaned_dataset(filepath: Optional[str] = None) -> pd.DataFrame:
    """Load the cleaned dataset produced in Step 1.

    Defaults to 'data/transformed/jobs_cleaned.json'.
    """
    if filepath is not None:
        path = pathlib.Path(filepath)
    else:
        path = pathlib.Path("data/transformed/jobs_cleaned.json")

    if not path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found at '{path}'. "
            "Please run Step 1 first: python -m src.transformation.clean_data"
        )

    print(f"Loading cleaned dataset from: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} postings.")
    return df


def save_transformed_with_skills(
    df: pd.DataFrame, output_dir: str = "data/transformed"
) -> None:
    """Save the updated dataset containing 'extracted_skills' into data/transformed/."""
    out_dir = pathlib.Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_file = out_dir / "jobs_cleaned.json"
    csv_file = out_dir / "jobs_cleaned.csv"
    with_skills_json = out_dir / "jobs_with_skills.json"
    with_skills_csv = out_dir / "jobs_with_skills.csv"

    # Convert to records dict for JSON
    records = df.to_dict(orient="records")

    # Update jobs_cleaned.json and jobs_with_skills.json
    content_json = json.dumps(records, ensure_ascii=False, indent=2)
    json_file.write_text(content_json, encoding="utf-8")
    with_skills_json.write_text(content_json, encoding="utf-8")
    print(f"Saved updated JSON to: {json_file} (and {with_skills_json.name})")

    # Save to CSV
    df.to_csv(csv_file, index=False, encoding="utf-8")
    df.to_csv(with_skills_csv, index=False, encoding="utf-8")
    print(f"Saved updated CSV to: {csv_file} (and {with_skills_csv.name})")


def main():
    """Run Step 2 skill extraction and display sample results."""
    print("=" * 60)
    print("JobStack - Person 2: Step 2 Skill Extraction")
    print("=" * 60)

    # 1. Load Step 1 cleaned data
    df = load_cleaned_dataset()

    # 2. Extract skills
    df_with_skills = add_extracted_skills_column(df)

    # 3. Save updated data
    save_transformed_with_skills(df_with_skills)

    # 4. Show summary statistics
    skills_series = df_with_skills["extracted_skills"]
    total_postings = len(df_with_skills)
    postings_with_skills = (skills_series.apply(len) > 0).sum()
    postings_without_skills = total_postings - postings_with_skills

    print("\n" + "=" * 60)
    print("Skill Extraction Summary:")
    print("=" * 60)
    print(f"Total postings: {total_postings}")
    print(f"Postings with at least 1 skill: {postings_with_skills} ({postings_with_skills / total_postings * 100:.1f}%)")
    print(f"Postings with 0 skills: {postings_without_skills} ({postings_without_skills / total_postings * 100:.1f}%)")

    # Count frequencies of each extracted skill
    all_extracted = [skill for sublist in skills_series for skill in sublist]
    skill_counts = pd.Series(all_extracted).value_counts().head(10)
    print("\nTop 10 Most Frequent Extracted Skills:")
    for skill, count in skill_counts.items():
        print(f"  - {skill:15} : {count} postings")

    # Show a few sample before-and-after records
    print("\nSample Before-and-After Extractions:")
    samples = df_with_skills[["title", "extracted_skills"]].head(6)
    for idx, row in samples.iterrows():
        print(f"  [{row['title']}] -> {row['extracted_skills']}")

    print("\nStep 2 completed successfully.")


if __name__ == "__main__":
    main()
