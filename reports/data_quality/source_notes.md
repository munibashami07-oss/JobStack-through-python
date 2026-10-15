# Source notes

Owner: Person 1 (data acquisition and validation). Raw files were collected on 2026-10-14 and are never edited after download. Items marked **VERIFY** have not been confirmed against the source's own page and must be checked before the data is used beyond course development.

## Summary

| Source | What it is | Coverage | Rows (raw / unique) | Access | Terms status |
|---|---|---|---|---|---|
| `kaggle_pk` | Pakistan's Job Market, a CSV of job ads | Pakistan, all job types, Dec 2019 to Mar 2021 | 6,680 / 5,398 | Downloaded file `data/raw/pakistan_jobs.csv` | ODbL listed on a mirror. **VERIFY** on Kaggle |
| `arbeitnow` | Arbeitnow public job-board API | Europe-wide (London, Berlin, Paris, Amsterdam lead), 28% German-language | 2,665 / 2,598 | Free API, no key, `src/ingestion/fetch_arbeitnow.py` | Free public API. **VERIFY** site terms |
| `remotive` | Remotive public remote-jobs API | Global remote jobs | 15 / 15 | Free API, no key, `src/ingestion/fetch_remotive.py` | Attribution and link-back required |

## Kaggle: Pakistan's Job Market

- **What it is:** about 7,000 Pakistan job openings from December 2019 to March 2021 with title, department, experience, date, city, job type and description. Author: Zeeshan-ul-hassan Usmani. The columns in our CSV (Job Name, Company Name, Job Type, Experience Required, Department, JD, City, Date Posted) match this dataset.
- **License:** a mirror of the dataset on opendata.com.pk lists the Open Data Commons Open Database License (ODbL). **VERIFY** the license on the Kaggle dataset page itself, because the mirror may differ. ODbL generally requires attribution and share-alike for a public derived database. Confirm what that means before publishing a derived dataset.
- **The team plan links a different Kaggle page** (a code notebook by devmarwat). Confirm which page our CSV actually came from and cite that one.
- **Limits:**
  - It covers all industries, not only technology (it contains jobs such as "Tea Boy"). Use `category` (for example IT, Computer Software, Web & E-commerce) to select tech roles.
  - It is 5 to 6 years older than the API data.
  - It has no salary field, no URL and no work mode.
  - `employment_type` is "Full Time" for every row after cleaning.
- **Cleaning done in the adapter:** the "Jobs in Pakistan" title suffix, the Job type prefixes, ", Pakistan" on company names, and the trailing "Job" or "Jobs" on category and job type.
- **Duplicates:** `posting_id` is a hash of title, company, city, date and the first 200 characters of the description. 1,282 rows with an identical hash were dropped.

## Arbeitnow API

- **Endpoint:** `https://www.arbeitnow.com/api/job-board-api`, paginated, no API key. Arbeitnow's own blog describes it as a free, documented job-board API.
- **Our use:** up to 10 pages, 1.5 seconds between requests, with a descriptive User-Agent. This is a snapshot, not a historical archive, so the date range is only 2026-10-07 to 2026-10-14.
- **Coverage:** a European feed with a German-language minority (733 of 2,598 postings detected as German). It is not Germany-heavy and it is not Pakistan data.
- **Limits:** no salary field, tags and job types are free text, and 8.8% of postings have no city after cleaning (location "Remote" was moved to `work_mode`).
- **VERIFY:** read the site terms at arbeitnow.com before any public use.

## Remotive API

- **Endpoint:** `https://remotive.com/api/remote-jobs`, no API key.
- **Terms (from Remotive's published API notice):**
  - Do not submit Remotive jobs to third-party websites or job aggregators.
  - Link back to the URL on Remotive and name Remotive as the source.
  - Listings are delayed by 24 hours.
- **Rate limit:** secondary sources report about 4 fetches per day and 2 requests per minute. **VERIFY** against Remotive's page. Do not re-fetch repeatedly.
- **Coverage:** only 15 postings came back, so it is too small for analysis. It is useful mainly as a third schema example (remote-only, `salary_text` present for 8 of 15).

## Alternatives not used

Adzuna was the preferred API in the team plan. It was not used because Pakistan coverage and its terms for course use were not confirmed. Record the outcome here if someone checks it.

## Open questions for the team

1. **Scope:** only the Kaggle data is from Pakistan. Are Arbeitnow and Remotive part of the real Project 1 dataset or only for developing the pipeline?
2. **Public repository:** the GitHub repository is public. Committing full raw files may conflict with ODbL (Kaggle) or Remotive's terms. Options: commit only `data/validated/sample_300.json` and give download instructions for the rest.
3. **Tech filter:** who applies the tech-only filter on the Kaggle categories, Person 1 in validation or Person 2 in transformation?

## Findings to carry forward

- Salary exists for only 8 of 8,011 rows (0.1%), all from Remotive. Salary analysis is not possible with this data.
- The sources cover different periods (Kaggle 2019 to 2021, APIs 2026), so trends must be split by source.
- No record was rejected by validation (0 of 8,011). Test the rejection path on purpose when demonstrating the pipeline.
- Duplicates are kept and flagged, not deleted. Count unique vacancies by dropping duplicates on title, company_name and city.