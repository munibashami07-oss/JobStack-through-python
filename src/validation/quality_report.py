import pathlib
import sqlite3
import sys

import pandas as pd

from src.validation.run_all import SOURCES, latest

DB = pathlib.Path("data/jobstack.db")
OUT = pathlib.Path("reports/data_quality/data_quality_report.md")
FIELDS = ["company_name", "category", "city", "country", "candidate_location", "work_mode",
          "employment_type", "experience", "salary_min", "salary_max", "salary_text", "posted_at", "language"]


def md(df: pd.DataFrame) -> str:
    df = df.reset_index(drop=True).astype(str)
    lines = ["| " + " | ".join(df.columns) + " |", "|" + "---|" * len(df.columns)]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def main():
    # 1. Raw vs unique counts per source (re-reads the raw files)
    rows = []
    for name, pattern, loader, adapter, id_field in SOURCES:
        path = latest(pattern)
        if path is None:
            continue
        raw = loader(path)
        unique = len({r.get(id_field) for r in raw})
        rows.append({"source": name, "file": path.name, "raw_rows": len(raw),
                     "duplicates": len(raw) - unique, "unique_rows": unique})
    ingest = pd.DataFrame(rows)

    with sqlite3.connect(DB) as con:
        df = pd.read_sql("SELECT * FROM jobs", con)

    out = ["# Data quality report", "",
           "Generated from `data/jobstack.db` by `python -m src.validation.quality_report`.", "",
           f"Total validated postings: **{len(df)}**. Rejected by validation: see `data/validated/jobs_rejected.json`.", "",
           "## 1. Ingestion and duplicates", md(ingest), ""]

    # 2. Missing values per field and source (% missing)
    miss = df.groupby("source")[FIELDS].agg(lambda s: round(s.isna().mean() * 100, 1)).T
    miss.index.name = "field"
    out += ["## 2. Missing values (% of rows)", md(miss.reset_index()), ""]

    # 3. Salary coverage
    has_salary = df[["salary_min", "salary_max", "salary_text"]].notna().any(axis=1)
    sal = df.assign(has_salary=has_salary).groupby("source")["has_salary"].agg(["sum", "count"])
    sal["pct"] = (sal["sum"] / sal["count"] * 100).round(1)
    sal = sal.rename(columns={"sum": "with_salary", "count": "rows"})
    out += ["## 3. Salary coverage", md(sal.reset_index()),
            "Salary is mostly missing. It is left as null, never 0.", ""]

    # 4. Language mix
    lang = df.fillna({"language": "unknown"}).groupby(["source", "language"]).size().reset_index(name="rows")
    out += ["## 4. Language mix", md(lang), ""]

    # 5. Date range per source (the sources cover different periods)
    dates = df.dropna(subset=["posted_at"]).assign(day=lambda d: d["posted_at"].str[:10])
    rng = dates.groupby("source")["day"].agg(earliest="min", latest="max").reset_index()
    out += ["## 5. Posting date range", md(rng),
            "Kaggle covers Dec 2019 to Mar 2021; Remotive and Arbeitnow are from October 2026. "
            "Do not compare trends across sources without splitting by source.", ""]

    # 6. Top cities and work mode
    for src in df["source"].unique():
        top = df[df["source"] == src]["city"].value_counts().head(8).reset_index()
        top.columns = ["city", "rows"]
        out += [f"## 6. Top cities: {src}", md(top), ""]
    wm = df.groupby(["source", "work_mode"]).size().reset_index(name="rows")
    out += ["## 7. Work mode", md(wm), ""]

    # 8. Duplicate title+company+city inside the final table
    dup = df.duplicated(subset=["title", "company_name", "city", "source"], keep=False).sum()
    out += ["## 8. Possible near-duplicates left in the data",
            f"{dup} rows share the same title, company, city and source. "
            "They have different ids, so they were kept. Review before analysis.", ""]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()