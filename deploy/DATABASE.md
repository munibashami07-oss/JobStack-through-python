# JobStack Database: Build, Verify and Deploy

The database is a single **SQLite file**: `data/jobstack_final.db`. It is not committed to git (it is rebuilt from the committed data), so every environment builds its own copy. There is no database server to run or pay for.

## 1. Build and verify (one command)

From the repository root, with the virtual environment active:

```bash
python deploy/build_database.py
```

This loads `data/transformed/jobs_final.json` (Person 2's output) into SQLite using the scripts in `sql/`, then runs Person 3's integrity and QA checks. It stops with an error if anything fails. Expected result on the current 300-row dataset:

| Table | Rows |
|---|---|
| companies | 259 |
| locations | 69 |
| skills | 20 |
| postings | 300 |
| posting_skills | 234 |
| salary_observations | 3 |

Last line on success: `OK: database ready at ... `

Other options: `--db <path>` writes the file somewhere else, `--skip-verify` only builds.

## 2. Schema (summary)

```
companies(company_id PK, company_name)
locations(location_id PK, city, country)
skills(skill_id PK, canonical_name, category)
postings(posting_pk PK, source, source_posting_id, source_url, title, standardized_title,
         description, company_id FK, location_id FK, category, experience,
         employment_type, work_mode, posted_at, language)
posting_skills(posting_pk FK, skill_id FK, extraction_method, evidence)   -- many-to-many
salary_observations(salary_id PK, posting_pk FK, salary_min, salary_max, currency, pay_period, salary_text)
```

Ready-made views (use these in a backend or for charts):

| View | Columns |
|---|---|
| `v_postings_flat` | posting_pk, source, source_posting_id, title, standardized_title, company_name, city, country, category, experience, employment_type, work_mode, posted_at, language |
| `v_posting_skills_flat` | posting_pk, skill, extraction_method, evidence |
| `v_skill_counts` | skill, n_postings |

Notes: salary is never stored as 0 (missing is NULL), and only 3 postings have a salary record. The `posting_skills` table is the many-to-many link between postings and skills.

## 3. Try it

```bash
python -m src.database.run_queries          # runs the queries in sql/04_queries.sql
```

Or in Python:

```python
import sqlite3
con = sqlite3.connect("data/jobstack_final.db")
print(con.execute("SELECT skill, n_postings FROM v_skill_counts ORDER BY n_postings DESC LIMIT 5").fetchall())
# [('Communication', 45), ('Teamwork', 35), ('Python', 26), ('Excel', 16), ('PHP', 15)]
```

## 4. Deploying it (for the backend)

Because the database is a file, "deploying the database" means building it on the same host that runs the backend. Use these two commands on the host:

| Setting | Value |
|---|---|
| Build command | `pip install -r requirements.txt && python deploy/build_database.py` |
| Database path for the backend | `data/jobstack_final.db` (or the path passed with `--db`) |

If the build command fails, the deploy fails. That is intended: the backend never starts on a broken database.

Limits to be aware of: SQLite is fine for this read-only demo. On free hosts the disk may reset on restart, which is why the database is rebuilt at build time instead of being uploaded. If the team later needs PostgreSQL, the SQL in `sql/` is the starting point, but that is outside Project 1.

## 5. Check list (database ownership)

- [x] Schema represents the many-to-many posting-skill relationship
- [x] Database can be rebuilt from scripts with one command
- [x] Integrity, foreign-key, duplicate and "salary is never 0" checks pass
- [x] Verification report: `reports/database/database_verification_report.md`
