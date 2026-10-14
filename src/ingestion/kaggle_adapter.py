import hashlib
import re
from datetime import datetime

import pandas as pd

from src.ingestion.arbeitnow_adapter import detect_language

PREFIXES = ("Full Time", "Part Time", "Contract", "Internship", "Freelance", "Temporary", "Work From Home")


def clean_title(t: str) -> str:
    t = re.sub(r"\s+Jobs?\s+in\s+Pakistan\s*$", "", t.strip(), flags=re.I)
    for p in PREFIXES:
        if t.lower().startswith(p.lower() + " "):
            t = t[len(p):].strip()
            break
    return t


def _strip_jobs(value: str) -> str:
    """Drop a trailing 'Job' or 'Jobs' label that the source adds to categories and job types."""
    return re.sub(r"\s+Jobs?\s*$", "", (value or "").strip(), flags=re.I)


def _strip(value: str, suffix: str) -> str:
    value = (value or "").strip()
    if value.lower().endswith(suffix.lower()):
        value = value[: -len(suffix)].strip()
    return value


def load_rows(path) -> list[dict]:
    """Read the CSV as text and attach a stable hash-based id to each row."""
    df = None
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            df = pd.read_csv(path, encoding=enc, dtype=str)
            break
        except UnicodeDecodeError:
            continue
    df = df.fillna("")
    rows = df.to_dict("records")
    for r in rows:
        key = "|".join([r["Job Name"], r["Company Name"], r["City"], r["Date Posted"], r["JD"][:200]])
        r["_id"] = hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]
    return rows


def to_record(raw: dict) -> dict:
    """Map one Kaggle Pakistan row into the JobPosting schema."""
    desc = raw.get("JD", "")
    company = _strip(raw.get("Company Name", ""), ", Pakistan") or None
    date = raw.get("Date Posted", "").strip()
    posted = datetime.strptime(date, "%d-%b-%y").isoformat() if date else None
    return {
        "posting_id": raw["_id"],
        "source": "kaggle_pk",
        "title": clean_title(raw.get("Job Name", "")),
        "description": desc,
        "company_name": company,
        "category": _strip_jobs(raw.get("Department", "")) or None,
        "city": raw.get("City", "").strip() or None,
        "country": "Pakistan",
        "work_mode": "unknown",
        "employment_type": _strip_jobs(raw.get("Job Type", "")) or None,
        "experience": raw.get("Experience Required", "").strip() or None,
        "posted_at": posted,
        "language": detect_language(desc[:1500]),
    }