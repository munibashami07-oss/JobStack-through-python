"""Step 1: Basic Data Cleaning and Standardization.

JobStack - Person 2 (Data Transformation and Skill Intelligence).
This module performs beginner-friendly data cleaning using Python and Pandas:
1. Strips unnecessary whitespace and HTML tags from descriptions.
2. Handles missing values without inventing or faking data.
3. Standardizes job titles, locations, employment types, and work modes using simple dictionaries.
4. Preserves original values in separate columns for comparison.
5. Saves the cleaned data under data/transformed/.
"""

import html
import json
import pathlib
import re
from typing import Optional

import pandas as pd


# ==============================================================================
# 1. Simple Standardization Dictionaries
# ==============================================================================

# Dictionary to map title variations to a canonical job title
TITLE_MAP = {
    "software engineer": "Software Engineer",
    "software developer": "Software Engineer",
    "sr. software engineer": "Senior Software Engineer",
    "sr software engineer": "Senior Software Engineer",
    "senior software engineer": "Senior Software Engineer",
    "frontend developer": "Frontend Developer",
    "front end developer": "Frontend Developer",
    "front-end developer": "Frontend Developer",
    "backend developer": "Backend Developer",
    "back end developer": "Backend Developer",
    "back-end developer": "Backend Developer",
    "full stack developer": "Full Stack Developer",
    "fullstack developer": "Full Stack Developer",
    "full-stack developer": "Full Stack Developer",
    "senior .net full-stack developer": "Full Stack Developer",
    "web developer": "Web Developer",
    "data scientist": "Data Scientist",
    "senior data scientist": "Data Scientist",
    "data analyst": "Data Analyst",
    "senior data analyst": "Data Analyst",
    "devops engineer": "DevOps Engineer",
    "qa engineer": "QA Engineer",
    "quality assurance engineer": "QA Engineer",
    "ui/ux designer": "UI/UX Designer",
    "ui ux designer": "UI/UX Designer",
}

# Dictionary to map location / city variations to a standard clean city name
LOCATION_MAP = {
    # Major Pakistani tech cities
    "lahore": "Lahore",
    "lahore, pakistan": "Lahore",
    "karachi": "Karachi",
    "karachi, pakistan": "Karachi",
    "islamabad": "Islamabad",
    "islamabad, pakistan": "Islamabad",
    "rawalpindi": "Rawalpindi",
    "rawalpindi, pakistan": "Rawalpindi",
    "faisalabad": "Faisalabad",
    "peshawar": "Peshawar",
    "multan": "Multan",
    # Common international cities from Arbeitnow
    "berlin": "Berlin",
    "berlin, germany": "Berlin",
    "berlin, berlin, germany": "Berlin",
    "munich": "Munich",
    "münchen": "Munich",
    "munich (deu)": "Munich",
    "london": "London",
    "london, greater london": "London",
    "london, united kingdom": "London",
    "hybrid london": "London",
    "paris": "Paris",
    "amsterdam": "Amsterdam",
}

# Dictionary to map employment types to standard categories
EMPLOYMENT_TYPE_MAP = {
    "full time": "Full-time",
    "full-time": "Full-time",
    "full_time": "Full-time",
    "permanent": "Full-time",
    "cdi": "Full-time",
    "unbefristeter arbeitsvertrag": "Full-time",
    "part time": "Part-time",
    "part-time": "Part-time",
    "werkstudent": "Part-time",
    "contract": "Contract",
    "freelance": "Contract",
    "freelancer": "Contract",
    "intern": "Internship",
    "internship": "Internship",
    "fr intern": "Internship",
    "temporary": "Temporary",
}

# Dictionary to map work mode variations
WORK_MODE_MAP = {
    "remote": "remote",
    "wfh": "remote",
    "work from home": "remote",
    "100 % remote": "remote",
    "onsite": "onsite",
    "on-site": "onsite",
    "in-office": "onsite",
    "office": "onsite",
    "hybrid": "hybrid",
    "unknown": "unknown",
}


# ==============================================================================
# 2. Individual Cleaning Functions
# ==============================================================================

def clean_html_and_whitespace(raw_text: Optional[str]) -> Optional[str]:
    """Clean HTML tags, decode HTML entities, and collapse extra whitespace.

    Parameters:
        raw_text: A string that may contain HTML tags (<p>, <br>) and entities (&amp;).

    Returns:
        A cleaned, plain-text string, or None if input is empty/null.

    Example:
        >>> clean_html_and_whitespace("<p>Python &amp; SQL\\n\\n Developer  </p>")
        'Python & SQL Developer'
    """
    if raw_text is None or not isinstance(raw_text, str):
        return None

    # Step 1: Decode HTML entities like &amp; -> &, &nbsp; -> space
    text = html.unescape(raw_text)

    # Step 2: Remove HTML tags like <p>, <a href="...">, <br>, <div>
    text = re.sub(r"<[^>]+>", " ", text)

    # Step 3: Replace multiple spaces, newlines, and tabs with a single space
    text = re.sub(r"\s+", " ", text).strip()

    # If the text becomes empty after stripping, return None
    return text if text else None


def standardize_job_title(raw_title: Optional[str]) -> Optional[str]:
    """Standardize common job title variations using TITLE_MAP.

    Parameters:
        raw_title: Job title string (e.g. 'Senior .NET Full-stack Developer').

    Returns:
        Standardized job title, or cleaned original title if no mapping matches.

    Example:
        >>> standardize_job_title("software developer")
        'Software Engineer'
    """
    if raw_title is None or not isinstance(raw_title, str):
        return None

    cleaned = raw_title.strip()
    if not cleaned:
        return None

    # Clean out common Arbeitnow gender noise: (m/w/d), (m|w|d), etc.
    cleaned = re.sub(r"\s*\([mwd\s/|]+\)", "", cleaned, flags=re.IGNORECASE).strip()

    # Check for exact match in lowercased dictionary
    lower_title = cleaned.lower()
    if lower_title in TITLE_MAP:
        return TITLE_MAP[lower_title]

    # Return cleaned title as-is if no rule matched
    return cleaned


def standardize_location(raw_city: Optional[str]) -> Optional[str]:
    """Standardize city/location strings using LOCATION_MAP without inventing locations.

    Parameters:
        raw_city: Raw location or city string (e.g. 'Lahore, Pakistan', 'Berlin, Germany').

    Returns:
        Standardized city name, cleaned original city, or None if missing.

    Example:
        >>> standardize_location("Lahore, Pakistan")
        'Lahore'
    """
    if raw_city is None or not isinstance(raw_city, str):
        return None

    cleaned = raw_city.strip()
    if not cleaned:
        return None

    lower_city = cleaned.lower()
    if lower_city in LOCATION_MAP:
        return LOCATION_MAP[lower_city]

    # If not in dictionary, return the cleaned string without inventing new data
    return cleaned


def standardize_employment_type(raw_emp_type: Optional[str]) -> Optional[str]:
    """Map raw employment type descriptions to standard categories using EMPLOYMENT_TYPE_MAP.

    Parameters:
        raw_emp_type: String like 'full_time', 'Experienced, Permanent, Full time'.

    Returns:
        Standardized type ('Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary'),
        or cleaned original if unknown, or None if missing.

    Example:
        >>> standardize_employment_type("full_time")
        'Full-time'
    """
    if raw_emp_type is None or not isinstance(raw_emp_type, str):
        return None

    cleaned = raw_emp_type.strip()
    if not cleaned:
        return None

    lower_emp = cleaned.lower()

    # 1. Exact match in dictionary
    if lower_emp in EMPLOYMENT_TYPE_MAP:
        return EMPLOYMENT_TYPE_MAP[lower_emp]

    # 2. Check keyword matches for compound strings (e.g. 'Experienced, Permanent, Full time')
    for keyword, standard_val in EMPLOYMENT_TYPE_MAP.items():
        if keyword in lower_emp:
            return standard_val

    return cleaned


def standardize_work_mode(raw_work_mode: Optional[str]) -> str:
    """Standardize work mode to 'remote', 'onsite', 'hybrid', or 'unknown'.

    Parameters:
        raw_work_mode: String indicating work mode (e.g. 'remote', '100 % Remote').

    Returns:
        'remote', 'onsite', 'hybrid', or 'unknown'.

    Example:
        >>> standardize_work_mode("100 % remote")
        'remote'
    """
    if raw_work_mode is None or not isinstance(raw_work_mode, str):
        return "unknown"

    cleaned = raw_work_mode.strip().lower()
    if cleaned in WORK_MODE_MAP:
        return WORK_MODE_MAP[cleaned]

    # Keyword check
    if "remote" in cleaned or "wfh" in cleaned:
        return "remote"
    if "hybrid" in cleaned:
        return "hybrid"
    if "onsite" in cleaned or "office" in cleaned:
        return "onsite"

    return "unknown"


# ==============================================================================
# 3. Missing Value Handling
# ==============================================================================

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Clean missing values without inventing or filling fake data.

    Rules:
    - Empty strings or whitespace-only strings are replaced with None (null).
    - String representations of null like 'nan' or 'None' become None.
    - Missing salary stays None (salary is NOT filled with 0, as per data contract).
    - Tags column is preserved as an empty list [] if missing.
    """
    df = df.copy()

    # Replace whitespace-only strings and string 'nan'/'None' with None across text columns
    for col in df.columns:
        if df[col].dtype == object or str(df[col].dtype).startswith("str"):
            df[col] = df[col].apply(
                lambda val: None if (isinstance(val, str) and (val.strip() == "" or val.strip().lower() in {"nan", "none", "null"})) else val
            )

    # Ensure tags is a list
    if "tags" in df.columns:
        df["tags"] = df["tags"].apply(lambda t: t if isinstance(t, list) else [])

    return df


# ==============================================================================
# 4. Full Dataset Cleaning Pipeline
# ==============================================================================

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Run all cleaning steps on the DataFrame while preserving original values.

    Preserved original columns:
    - title -> standardized_title
    - city -> standardized_city
    - employment_type -> standardized_employment_type
    - work_mode -> standardized_work_mode
    - description -> cleaned_description
    """
    # 1. Handle missing values
    df = handle_missing_values(df)

    # 2. Clean HTML and whitespace from job descriptions
    df["cleaned_description"] = df["description"].apply(clean_html_and_whitespace)

    # 3. Standardize job titles
    df["standardized_title"] = df["title"].apply(standardize_job_title)

    # 4. Standardize locations / cities
    df["standardized_city"] = df["city"].apply(standardize_location)

    # 5. Standardize employment types
    df["standardized_employment_type"] = df["employment_type"].apply(standardize_employment_type)

    # 6. Standardize work modes
    df["standardized_work_mode"] = df["work_mode"].apply(standardize_work_mode)

    return df


# ==============================================================================
# 5. File I/O Helpers
# ==============================================================================

def load_validated_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """Load the validated job postings dataset.

    Checks:
    1. If filepath is explicitly passed, use it.
    2. Else check for full production data at 'data/validated/jobs_valid.json'.
    3. Else fallback to committed development sample at 'data/validated/sample_300.json'.
    """
    if filepath is not None:
        target_path = pathlib.Path(filepath)
    else:
        full_path = pathlib.Path("data/validated/jobs_valid.json")
        sample_path = pathlib.Path("data/validated/sample_300.json")

        if full_path.exists():
            target_path = full_path
        elif sample_path.exists():
            print(f"Notice: '{full_path}' not found. Using development sample '{sample_path}'.")
            target_path = sample_path
        else:
            raise FileNotFoundError("No validated dataset found in data/validated/")

    print(f"Loading validated data from: {target_path}")
    data = json.loads(target_path.read_text(encoding="utf-8"))
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} postings.")
    return df


def save_transformed_data(df: pd.DataFrame, output_dir: str = "data/transformed") -> None:
    """Save cleaned dataset in data/transformed/ in both JSON and CSV formats."""
    out_dir = pathlib.Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_file = out_dir / "jobs_cleaned.json"
    csv_file = out_dir / "jobs_cleaned.csv"

    # Save to JSON (orient='records' keeps JSON array structure)
    json_data = df.to_dict(orient="records")
    json_file.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved cleaned JSON to: {json_file}")

    # Save to CSV for tabular inspection
    df.to_csv(csv_file, index=False, encoding="utf-8")
    print(f"Saved cleaned CSV to: {csv_file}")


def main():
    """Run data cleaning step 1 and display sample results."""
    print("=" * 60)
    print("JobStack - Person 2: Step 1 Basic Data Cleaning")
    print("=" * 60)

    # 1. Load validated data
    df = load_validated_data()

    # 2. Clean and standardize
    cleaned_df = clean_dataset(df)

    # 3. Save output
    save_transformed_data(cleaned_df)

    # 4. Display a brief before-and-after summary
    print("\n" + "=" * 60)
    print("Transformation Summary:")
    print("=" * 60)
    print(f"Total rows processed: {len(cleaned_df)}")

    print("\n[Before vs After: Work Mode]")
    print(cleaned_df[["work_mode", "standardized_work_mode"]].value_counts().head(5))

    print("\n[Before vs After: Employment Type]")
    print(cleaned_df[["employment_type", "standardized_employment_type"]].value_counts().head(5))

    print("\n[Sample Cleaned Records]")
    sample_view = cleaned_df[
        ["title", "standardized_title", "city", "standardized_city", "standardized_employment_type"]
    ].head(5)
    print(sample_view.to_string())
    print("\nStep 1 completed successfully.")


if __name__ == "__main__":
    main()
