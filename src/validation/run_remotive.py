import json
import pathlib
import sys

from pydantic import ValidationError

from src.ingestion.remotive_adapter import to_record
from src.validation.models import JobPosting


def latest_raw() -> pathlib.Path:
    files = sorted(pathlib.Path("data/raw").glob("remotive_*.json"))
    if not files:
        sys.exit("No raw file found. Run fetch_remotive first.")
    return files[-1]


def main():
    raw_path = latest_raw()
    jobs = json.loads(raw_path.read_text(encoding="utf-8")).get("jobs", [])
    valid, rejected = [], []
    for raw in jobs:
        try:
            valid.append(JobPosting(**to_record(raw)).model_dump(mode="json"))
        except (ValidationError, KeyError, TypeError) as e:
            rejected.append({"raw_id": raw.get("id"), "error": str(e)[:300]})

    out = pathlib.Path("data/validated")
    out.mkdir(parents=True, exist_ok=True)
    (out / "remotive_valid.json").write_text(json.dumps(valid, indent=2), encoding="utf-8")
    (out / "remotive_rejected.json").write_text(json.dumps(rejected, indent=2), encoding="utf-8")
    print(f"Source file: {raw_path.name}")
    print(f"Total: {len(jobs)} | valid: {len(valid)} | rejected: {len(rejected)}")


if __name__ == "__main__":
    main()