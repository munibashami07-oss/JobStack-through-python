from src.ingestion.arbeitnow_adapter import detect_language


def to_record(raw: dict) -> dict:
    """Map one Remotive job into the JobPosting schema."""
    desc = raw.get("description") or ""
    return {
        "posting_id": str(raw["id"]),
        "source": "remotive",
        "source_url": raw.get("url"),
        "title": raw.get("title") or "",
        "description": desc,
        "company_name": raw.get("company_name"),
        "category": raw.get("category"),
        "tags": raw.get("tags") or [],
        "candidate_location": raw.get("candidate_required_location"),
        "work_mode": "remote",
        "employment_type": raw.get("job_type"),
        "salary_text": raw.get("salary") or None,
        "posted_at": raw.get("publication_date"),
        "language": detect_language(desc[:1500]),
    }