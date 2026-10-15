import json
import pathlib
import sys

from pydantic import ValidationError

from src.ingestion import arbeitnow_adapter, kaggle_adapter, remotive_adapter
from src.validation.models import JobPosting


def load_json(key):
    def _load(path):
        return json.loads(path.read_text(encoding="utf-8")).get(key, [])
    return _load


# name, file pattern, loader, adapter, id field
SOURCES = [
    ("remotive", "remotive_*.json", load_json("jobs"), remotive_adapter.to_record, "id"),
    ("arbeitnow", "arbeitnow_*.json", load_json("data"), arbeitnow_adapter.to_record, "slug"),
    ("kaggle_pk", "pakistan_jobs.csv", kaggle_adapter.load_rows, kaggle_adapter.to_record, "_id"),
]


def latest(pattern):
    files = sorted(pathlib.Path("data/raw").glob(pattern))
    return files[-1] if files else None


def main():
    valid, rejected = [], []
    for name, pattern, loader, adapter, id_field in SOURCES:
        path = latest(pattern)
        if path is None:
            print(f"{name}: no raw file, skipped")
            continue
        raw_jobs = loader(path)
        seen, dupes, ok, bad = set(), 0, 0, 0
        for raw in raw_jobs:
            rid = raw.get(id_field)
            if rid in seen:
                dupes += 1
                continue
            seen.add(rid)
            try:
                valid.append(JobPosting(**adapter(raw)).model_dump(mode="json"))
                ok += 1
            except (ValidationError, KeyError, TypeError, ValueError) as e:
                rejected.append({"source": name, "raw_id": rid, "error": str(e)[:300]})
                bad += 1
        print(f"{name}: file={path.name} total={len(raw_jobs)} duplicates={dupes} valid={ok} rejected={bad}")

    out = pathlib.Path("data/validated")
    out.mkdir(parents=True, exist_ok=True)
    (out / "jobs_valid.json").write_text(json.dumps(valid, ensure_ascii=False), encoding="utf-8")
    (out / "jobs_rejected.json").write_text(json.dumps(rejected, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"TOTAL valid={len(valid)} rejected={len(rejected)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()