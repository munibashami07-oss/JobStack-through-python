# Data contract: validated postings (Person 1 to Person 2)

Input for transformation: `data/validated/jobs_valid.json` (JSON array, one object per posting). A 300-row sample for development is in `data/validated/sample_300.json` (5 Remotive, 115 Arbeitnow, 180 Kaggle, random seed 42).

Rebuild from raw files:

```
python -m src.validation.run_all
```

The schema is defined in `src/validation/models.py` (`JobPosting`). Records that fail validation go to `data/validated/jobs_rejected.json` with a reason. At the last run, 0 of 8,011 records were rejected.

## Rules

- Raw data is never modified. This file is the only input Person 2 needs.
- Missing values are `null`, never an empty string and never 0. Salary missing means `null`, not 0.
- Identity is the pair (`source`, `posting_id`). `posting_id` alone is not unique across sources.
- No normalization of titles, locations or skills has been done yet. That is Person 2's work.
- Rows with the same title, company, city and source are kept and flagged in the quality report (section 8). They are not deleted.

## Fields

| Field | Type | Nullable | Notes and example |
|---|---|---|---|
| `posting_id` | string | no | Arbeitnow slug, Remotive id as text, Kaggle 16-character hash |
| `source` | `remotive`, `arbeitnow`, `kaggle_pk` | no | |
| `source_url` | string | yes | Null for Kaggle |
| `title` | string | no | Kaggle titles have the "Jobs in Pakistan" suffix removed |
| `description` | string | no | Arbeitnow and Remotive contain HTML. Kaggle is plain text |
| `company_name` | string | yes | Null for 6.2% of Kaggle rows |
| `category` | string | yes | Kaggle: for example `IT`, `Computer Software`. Arbeitnow: the first tag. Remotive: its category |
| `tags` | list of strings | no (may be empty) | Arbeitnow and Remotive only |
| `city` | string | yes | Arbeitnow cities are free text (for example "Paris, Île-de-France, France" or "United Kingdom"). Remotive has none |
| `country` | string | yes | Only Kaggle fills it ("Pakistan") |
| `candidate_location` | string | yes | Only Remotive (for example "Worldwide") |
| `work_mode` | `remote`, `onsite`, `hybrid`, `unknown` | no | Kaggle is always `unknown`. Arbeitnow is mostly `unknown`. `onsite` is never produced yet |
| `employment_type` | string | yes | Free text. Arbeitnow has German and English mixed values. Kaggle is always "Full Time" |
| `experience` | string | yes | Only Kaggle, free text (for example "2 Years Job Exp.", "< 1 Year", "Job for Fresh Graduates") |
| `salary_min`, `salary_max` | number | yes | Always null in current data |
| `currency` | string | yes | Always null in current data |
| `salary_text` | string | yes | Only Remotive (8 of 15 rows), free text such as "$50-$75 /hour" |
| `posted_at` | datetime | yes | See the timestamp note below |
| `language` | `en`, `de` | yes | Detected from the first 1,500 characters of the description with a simple German-word count |

## Known gaps against the shared team contract

- **`salary_period` and `province` are not in the schema.** No source provides them. Either Person 2 derives province from city for Pakistan, or the team agrees to drop them.
- **Salary is effectively absent** (8 of 8,011 rows). Do not build salary logic on this data.
- **Timestamps are mixed.** Arbeitnow values end in `Z` (UTC). Remotive and Kaggle values have no timezone. Kaggle has a date only, at midnight. Normalize to one format in the transformation step.
- **Language values** are limited to `en` and `de`.

## Handling notes for Person 2

- Strip HTML from Arbeitnow and Remotive descriptions before skill extraction, but keep the original text.
- Kaggle covers all industries. Select tech postings with `category` before skill analysis.
- Kaggle dates are 2019 to 2021 and API dates are 2026. Do not compare time trends across sources.