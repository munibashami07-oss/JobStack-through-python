# Source notes

Owner: Person 1 (data acquisition and validation). Raw files were collected on 2026-10-14 and are never edited after download. Items marked **VERIFY** have not been confirmed against the source's own page and must be checked before the data is used beyond course development.

## Summary

| Source | What it is | Coverage | Rows (raw / unique) | Access | Terms status |
|---|---|---|---|---|---|
| `kaggle_pk` | Pakistan's Job Market, a CSV of job ads | Pakistan, all job types, Dec 2019 to Mar 2021 | 6,680 / 5,398 | Downloaded file `data/raw/pakistan_jobs.csv` | Kaggle license: "Data files © Original Authors" (not an open license). See the License note below |
| `arbeitnow` | Arbeitnow public job-board API | Europe-wide (London, Berlin, Paris, Amsterdam lead), 28% German-language | 2,665 / 2,598 | Free API, no key, `src/ingestion/fetch_arbeitnow.py` | Free public API. **VERIFY** site terms |
| `remotive` | Remotive public remote-jobs API | Global remote jobs | 15 / 15 | Free API, no key, `src/ingestion/fetch_remotive.py` | Attribution and link-back required |

## Kaggle: Pakistan's Job Market

- **What it is:** about 7,000 Pakistan job openings from December 2019 to March 2021 with title, department, experience, date, city, job type and description. Author: Zeeshan-ul-hassan Usmani. The columns in our CSV (Job Name, label, Company Name, Job Type, Experience Required, Department, JD, City, Date Posted) match this dataset's description.
- **Our file:** `data/raw/pakistan_jobs.csv`, 6,680 rows, 9 columns: Job Name, label, Company Name, Job Type, Experience Required, Department, JD, City, Date Posted. SHA-256: 91BF0902F97C1697CAAA111243754B98AE07A160F48C11B7EF670233C4852544. Downloaded 2026-10-14. The `label` column is the premium label of the job post, as described on the Kaggle dataset page.
- **Original dataset:** "Pakistan's Job Market" by Zeeshan-ul-hassan Usmani, https://www.kaggle.com/datasets/zusmani/pakistans-job-market (page checked on 2026-10-15). Our CSV matches its columns. Kaggle describes "close to 7,000 job openings"; our file has 6,680 rows.
- **License:** the Kaggle dataset page (checked 2026-10-15) shows the license as "Data files © Original Authors", which is not an open license. The opendata.com.pk mirror lists ODbL, but the Kaggle page is the original source, so we do not rely on the mirror. Treat the data as not freely redistributable: use it for this course project, cite the author and the Kaggle page, and do not republish the raw or derived rows publicly without the author's permission or guidance from the instructor.
- **The team plan's Kaggle link** is a code notebook by devmarwat (Apache 2.0, which covers its code, not the data). It reads `/kaggle/input/pakistan-jobs/pakistan_jobs.csv` from a different Kaggle dataset, "Pakistan Jobs" by Muhammad Hassan (CC0: Public Domain, described as daily LinkedIn job postings across Pakistan, updated daily; page checked 2026-10-15). Our file has the same file name, but its date range (December 2019 to March 2021) and columns match the zusmani dataset above, not that description. The notebook has only one version, so we cannot tell whether that dataset once held the zusmani data. We therefore treat our CSV as the zusmani data and its license ("© Original Authors") as the one that applies. We do not claim CC0 for our file.
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
2. **Public repository:** raw files are no longer tracked (`data/raw/*` is ignored) and the large files are shared through Google Drive. Still open: the Kaggle license is "© Original Authors" and Remotive's terms say not to submit its jobs to third-party websites, so the committed validated files (`data/validated/sample_300.json` if it contains Kaggle rows, and `data/validated/remotive_valid.json`) and any "anyone with the link" Drive links may also be a problem. Options: make the repository private with teammates as collaborators, keep only non-restricted or synthetic sample data in the public repo, and share Drive links with teammates only. Decide with the instructor.
3. **Tech filter:** who applies the tech-only filter on the Kaggle categories, Person 1 in validation or Person 2 in transformation?
4. **Alternative Pakistan source:** the Kaggle dataset "Pakistan Jobs" by Muhammad Hassan (CC0, daily LinkedIn postings across Pakistan) is current, Pakistan-specific and freely redistributable. Check its Data Card (columns, row count, whether it has descriptions and salary) and decide whether it should replace or add to the zusmani CSV. This would also remove the redistribution concern in question 2.

## Findings to carry forward

- Salary exists for only 8 of 8,011 rows (0.1%), all from Remotive and only as free text in `salary_text`. No row has numeric `salary_min` or `salary_max`. See `validation_and_salary_notes.md`. Salary analysis is not possible with this data.
- The sources cover different periods (Kaggle 2019 to 2021, APIs 2026), so trends must be split by source.
- No record was rejected by validation (0 of 8,011). The rejection path is tested in `tests/test_rejection.py` with deliberately broken records.
- Duplicates are kept and flagged, not deleted. Count unique vacancies by dropping duplicates on title, company_name and city.