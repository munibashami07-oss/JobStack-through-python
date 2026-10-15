# Data quality report

Generated from `data/jobstack.db` by `python -m src.validation.quality_report`.

Total validated postings: **8011**. Rejected by validation: see `data/validated/jobs_rejected.json`.

## 1. Ingestion and duplicates
| source | file | raw_rows | duplicates | unique_rows |
|---|---|---|---|---|
| remotive | remotive_20261014_1910.json | 15 | 0 | 15 |
| arbeitnow | arbeitnow_20261014_1917.json | 2665 | 67 | 2598 |
| kaggle_pk | pakistan_jobs.csv | 6680 | 1282 | 5398 |

## 2. Missing values (% of rows)
| field | arbeitnow | kaggle_pk | remotive |
|---|---|---|---|
| company_name | 0.0 | 6.2 | 0.0 |
| category | 5.2 | 0.0 | 0.0 |
| city | 8.8 | 0.0 | 100.0 |
| country | 100.0 | 0.0 | 100.0 |
| candidate_location | 100.0 | 100.0 | 0.0 |
| work_mode | 0.0 | 0.0 | 0.0 |
| employment_type | 18.4 | 0.0 | 0.0 |
| experience | 100.0 | 0.0 | 100.0 |
| salary_min | 100.0 | 100.0 | 100.0 |
| salary_max | 100.0 | 100.0 | 100.0 |
| salary_text | 100.0 | 100.0 | 46.7 |
| posted_at | 0.0 | 0.0 | 0.0 |
| language | 0.0 | 0.0 | 0.0 |

## 3. Salary coverage
| source | with_salary | rows | pct |
|---|---|---|---|
| arbeitnow | 0 | 2598 | 0.0 |
| kaggle_pk | 0 | 5398 | 0.0 |
| remotive | 8 | 15 | 53.3 |
Salary is mostly missing. It is left as null, never 0.

## 4. Language mix
| source | language | rows |
|---|---|---|
| arbeitnow | de | 733 |
| arbeitnow | en | 1865 |
| kaggle_pk | en | 5398 |
| remotive | en | 15 |

## 5. Posting date range
| source | earliest | latest |
|---|---|---|
| arbeitnow | 2026-10-07 | 2026-10-14 |
| kaggle_pk | 2019-12-18 | 2021-03-15 |
| remotive | 2026-09-14 | 2026-10-11 |
Kaggle covers Dec 2019 to Mar 2021; Remotive and Arbeitnow are from October 2026. Do not compare trends across sources without splitting by source.

## 6. Top cities: arbeitnow
| city | rows |
|---|---|
| London | 234 |
| Berlin | 171 |
| Paris | 148 |
| Amsterdam | 146 |
| Munich | 71 |
| Hamburg | 58 |
| Delft | 54 |
| United Kingdom | 35 |

## 6. Top cities: kaggle_pk
| city | rows |
|---|---|
| Lahore | 1700 |
| Islamabad | 1542 |
| Karachi | 1376 |
| Faisalabad | 185 |
| Rawalpindi | 107 |
| Sialkot | 79 |
| Multan | 54 |
| Gujranwala | 50 |

## 7. Work mode
| source | work_mode | rows |
|---|---|---|
| arbeitnow | hybrid | 7 |
| arbeitnow | remote | 243 |
| arbeitnow | unknown | 2348 |
| kaggle_pk | unknown | 5398 |
| remotive | remote | 15 |

## 8. Possible near-duplicates left in the data
| source | kind | rows |
|---|---|---|
| arbeitnow | different posted_at (likely reposts) | 75 |
| arbeitnow | same posted_at (likely true duplicates) | 33 |
| kaggle_pk | different posted_at (likely reposts) | 359 |
| kaggle_pk | same posted_at (likely true duplicates) | 10 |
All rows were kept (they have different ids). Reposts on different dates are real postings. For counts of unique vacancies, drop duplicates on title + company_name + city.
