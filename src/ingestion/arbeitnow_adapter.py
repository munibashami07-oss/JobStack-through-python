from datetime import datetime, timezone

GERMAN_MARKERS = [" und ", " der ", " die ", " das ", " mit ", " für ", " wir ", " du ", " deine "]


def detect_language(text: str) -> str:
    t = f" {text.lower()} "
    hits = sum(t.count(m) for m in GERMAN_MARKERS)
    return "de" if hits >= 3 else "en"


def to_record(raw: dict) -> dict:
    """Map one Arbeitnow job into the JobPosting schema."""
    title = raw.get("title") or ""
    desc = raw.get("description") or ""
    if raw.get("remote"):
        mode = "remote"
    elif "hybrid" in title.lower():
        mode = "hybrid"
    else:
        mode = "unknown"
    ts = raw.get("created_at")
    posted = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else None
    return {
        "posting_id": raw["slug"],
        "source": "arbeitnow",
        "source_url": raw.get("url"),
        "title": title,
        "description": desc,
        "company_name": raw.get("company_name"),
        "category": (raw.get("tags") or [None])[0],
        "tags": raw.get("tags") or [],
        "city": raw.get("location"),
        "work_mode": mode,
        "employment_type": ", ".join(raw.get("job_types") or []) or None,
        "posted_at": posted,
        "language": detect_language(desc[:1500]),
    }