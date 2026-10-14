def to_record(raw: dict) -> dict:
    """Map one Remotive job into the JobPosting schema."""
    return {
        "posting_id": str(raw["id"]),
        "source": "remotive",
        "source_url": raw.get("url"),
        "title": raw.get("title") or "",
        "description": raw.get("description") or "",
        "company_name": raw.get("company_name"),
        "category": raw.get("category"),
        "tags": raw.get("tags") or [],
        "candidate_location": raw.get("candidate_required_location"),
        "work_mode": "remote",
        "employment_type": raw.get("job_type"),
        "salary_text": raw.get("salary") or None,
        "posted_at": raw.get("publication_date"),
    }