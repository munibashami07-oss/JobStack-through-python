<div align="center">

# JobStack
### From Job Postings to Skills Intelligence, Prediction & Career Decision Support

**Turning raw job-market data into actionable insights for Pakistan's technology ecosystem.**

![Project Status](https://img.shields.io/badge/status-in%20development-orange)
![Focus](https://img.shields.io/badge/focus-Pakistan%20Tech%20Market-2563eb)
![Pipeline](https://img.shields.io/badge/pipeline-ETL%20%7C%20SQL%20%7C%20EDA-0f766e)
![License](https://img.shields.io/badge/license-to%20be%20determined-lightgrey)

</div>

---

## Overview

JobStack is a data-driven labor-market intelligence project designed to turn job advertisements into structured, explainable insights. Instead of treating job listings as isolated vacancies, JobStack organizes information about roles, skills, employers, locations, experience requirements, work arrangements, and advertised salaries—where available.

The project is planned as a connected, three-stage system:

| Stage | Focus | Goal |
|---|---|---|
| **Project 1** | Data Engineering & Exploratory Data Analysis | Build a reliable job-posting dataset, normalized SQL database, and evidence-based market insights. |
| **Project 2** | Classical Machine Learning | Explore salary estimation and job-fit prediction using reproducible scikit-learn pipelines. |
| **Project 3** | Deep Learning & MLOps | Develop and evaluate a neural job–candidate matching approach with PyTorch, Optuna, and MLflow. |

This repository currently focuses on establishing the **Project 1 data foundation**. Later stages depend on the quality and reproducibility of this foundation.

## The Problem

Job advertisements contain useful labor-market signals, but those signals are difficult to compare directly:

- The same skill may appear under different names or spellings.
- Job titles and location labels are inconsistent.
- Duplicate postings can distort demand estimates.
- Salary information is often missing or expressed in different formats.
- A large collection of listings does not automatically explain which skills are in demand or how requirements differ by role and location.

JobStack aims to structure these signals so that students, job seekers, recruiters, educators, and other stakeholders can investigate the advertised technology-job market more effectively.

## Project 1: ETL + SQL + EDA

### Core workflow

```text
Permitted Job Data Source
          |
          v
      Extraction
          |
          v
   Validation (Pydantic)
          |
          v
 Transformation & Cleaning
          |
          v
 Skill Extraction & Normalization
          |
          v
     SQL Database
          |
          v
 Exploratory Data Analysis
          |
          v
  Evidence-Based Findings
```

### What Project 1 aims to deliver

- **Data ingestion:** Retrieve job-posting records from a permitted API or legally usable dataset.
- **Validation:** Check data types, required fields, value ranges, and record structure.
- **Transformation:** Clean text and standardize job titles, locations, employment types, and work modes where possible.
- **Skill intelligence:** Extract skills using a transparent dictionary/keyword approach, map aliases to canonical names, and retain evidence where practical.
- **Relational database:** Store postings, companies, locations, skills, and posting–skill relationships in a normalized SQL schema.
- **EDA:** Investigate skill demand, role/location differences, skill co-occurrence, salary distributions where data permits, and trends where dates are available.
- **Reproducibility:** Keep scripts, schemas, queries, analysis, assumptions, and limitations documented.

## Questions JobStack Can Investigate

Depending on the coverage and quality of the selected dataset, Project 1 will explore questions such as:

- Which technical skills appear most frequently in the collected postings?
- Which skills are particularly associated with specific job roles?
- Which skills commonly appear together?
- How do advertised requirements vary across cities and remote roles?
- How do advertised salary distributions vary by role, location, or experience when usable salary data is available?
- How do skill requirements change over time when posting dates and sufficient historical data are available?
- Which job titles have similar skill profiles despite using different names?

> **Interpretation note:** Job-posting data reflects advertised demand in the collected sample. It does not necessarily represent every vacancy in the labor market. Skill–salary relationships should be described as associations, not proof that a skill causes higher pay.

## Planned Technology Stack

| Area | Planned tools | Purpose |
|---|---|---|
| Programming | Python | Data processing and analysis |
| Data acquisition | `requests` or a permitted API client | Retrieve job-posting data |
| Validation | Pydantic | Validate record structure and field values |
| Data manipulation | Pandas | Cleaning, normalization, and analysis |
| Database | PostgreSQL or SQLite | Store normalized job and skill data |
| SQL | SQL | Database schema, integrity checks, and analytical queries |
| Exploratory analysis | Jupyter Notebook | Document analysis workflow |
| Visualization | Matplotlib or Plotly | Communicate patterns and findings |
| Version control | Git and GitHub | Collaboration and reproducibility |

*This is the planned stack; exact versions and final choices should be recorded by the team once implementation begins.*

## Architecture & Data Model

The proposed relational model includes the following entities:

| Table | Purpose |
|---|---|
| `postings` | Job title, description, company/location references, experience, work mode, date, and source |
| `companies` | Company names and other available company attributes |
| `locations` | City, province, and country |
| `skills` | Canonical skill names and categories |
| `posting_skills` | Many-to-many relationship between job postings and skills, with evidence/extraction metadata where available |
| `salary_observations` | Salary range, currency, pay period, and normalized salary where the source supports it |

A single posting can require multiple skills, and a skill can appear in many postings. The `posting_skills` relationship is therefore central to the data model.

## Repository Structure

The following is a suggested structure. Update it to match the actual repository as the implementation evolves.

```text
jobstack/
├── data/
│   ├── raw/                 # Original source snapshots; do not overwrite
│   ├── validated/           # Records that pass validation
│   ├── transformed/         # Cleaned and normalized records
│   └── skills/              # Skill dictionaries and alias mappings
├── src/
│   ├── ingestion/           # Data extraction
│   ├── validation/          # Pydantic models and data-quality checks
│   ├── transformation/     # Cleaning and normalization
│   ├── skills/              # Skill extraction and canonicalization
│   ├── database/            # Loading and database utilities
│   └── eda/                 # Reusable analysis code
├── sql/                     # DDL, constraints, indexes, and queries
├── notebooks/               # Exploratory notebooks
├── tests/                   # Automated tests
├── reports/
│   ├── data_quality/
│   ├── skill_extraction/
│   ├── database/
│   └── findings/
├── requirements.txt         # Or pyproject.toml, depending on setup
├── .env.example             # Names of required environment variables
├── .gitignore
└── README.md
```

**Data hygiene:** keep raw data immutable; avoid committing secrets; and follow the dataset/API license and sharing restrictions. If data cannot legally be redistributed, document how authorized team members can obtain it rather than committing it to the repository.

## Team Responsibilities — Project 1

The work is divided into four workstreams designed to run in parallel using agreed data contracts.

| Team member | Ownership | Main deliverables |
|---|---|---|
| **Person 1 — Data Acquisition & Validation** | Source evaluation, extraction, Pydantic validation, data-quality reporting | Ingestion scripts, raw snapshot (where permitted), validated records, validation report |
| **Person 2 — Transformation & Skill Intelligence** | Cleaning, normalization, deduplication, skill dictionary and extraction | Transformation pipeline, canonical skill mappings, extraction examples, transformed records |
| **Person 3 — SQL Database Engineering** | ERD, normalized schema, constraints, data loading, SQL queries | ERD, DDL scripts, loading script, integrity checks, analytical queries |
| **Person 4 — EDA & Insights** | Statistical summaries, charts, analysis questions, findings and limitations | Reproducible EDA, visualizations, documented findings, limitations |

### How the work connects

1. Person 1 publishes a documented schema and sample validated records.
2. Person 2 builds transformations against that contract and publishes the transformed-data specification.
3. Person 3 develops the database from the agreed schema and loads the transformed records when ready.
4. Person 4 develops analysis against sample data first, then reruns it on the final analytical dataset.

This reduces waiting time while preserving a coherent end-to-end pipeline.

## Contributor Guide — How to Contribute

Contributions are welcome from all team members. The goal is to keep JobStack reproducible, reviewable, and consistent across the four Project 1 workstreams. Please follow this workflow before changing the code or data.

### 1. Choose a task before starting

- Check the project task board or open GitHub issues before beginning work.
- If the task is not listed, open an issue describing the problem, proposed change, expected output, and any dependencies.
- Assign the issue to yourself only after confirming that it does not conflict with another contributor's work.
- Keep pull requests focused: one feature, fix, documentation update, or analysis improvement per PR where practical.

### 2. Set up your local copy

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd jobstack
git checkout main
git pull origin main
python -m venv .venv
```

Activate the virtual environment using the instructions in **Getting Started**, then install the project's dependencies once `requirements.txt` or `pyproject.toml` is available. Never place API keys, passwords, or personal access tokens directly in code.

### 3. Create a branch for your work

Do not work directly on `main`. Create a branch from the latest `main` branch:

```bash
git checkout main
git pull origin main
git checkout -b <type>/<short-description>
```

Suggested branch prefixes:

- `feat/` — new functionality, such as `feat/skill-alias-mapping`
- `fix/` — bug fixes, such as `fix/posting-deduplication`
- `data/` — source or data-contract changes, such as `data/validation-rules`
- `analysis/` — EDA or findings, such as `analysis/skill-demand-by-city`
- `docs/` — documentation, such as `docs/contributor-guide`
- `test/` — tests, such as `test/skill-normalization`

### 4. Follow the project's data contracts

Before changing an input or output format, coordinate with the contributors who consume it. In particular:

- Person 1 (Data Acquisition & Validation) owns source documentation, raw extraction, and the validated-record contract.
- Person 2 (Transformation & Skill Intelligence) owns cleaning rules, normalized fields, and skill names/aliases.
- Person 3 (SQL Database Engineering) owns the relational schema, constraints, and loading expectations.
- Person 4 (EDA & Insights) owns analytical questions, notebook/report outputs, and interpretation of findings.

If your change affects another workstream, document the change in the issue or PR and notify the affected contributor before merging. Use a small, clearly described sample for development when possible; do not make downstream work depend on undocumented local files.

### 5. Make changes that are reproducible

- Keep reusable pipeline logic in `src/`; use notebooks mainly for exploration and communicating analysis.
- Use clear names, small functions, and comments to explain non-obvious decisions—not every line of code.
- Make cleaning and normalization rules explicit. Do not silently discard records or replace missing values with invented values.
- Add or update automated tests for data validation, transformation rules, deduplication, skill extraction, and database constraints where relevant.
- Set random seeds when randomness affects results, and document assumptions and limitations.
- Avoid machine-specific absolute paths. Use configuration or paths relative to the repository.
- If a schema, field, dependency, or command changes, update the relevant documentation and examples.

### 6. Protect data, credentials, and source terms

- Never commit `.env` files, API keys, passwords, tokens, or other secrets.
- Do not commit raw or derived datasets unless the source license and project rules explicitly permit redistribution.
- Do not upload personal, confidential, or restricted data to public services or repositories.
- Preserve source attribution and record the source, collection date, license/terms checked, and any relevant restrictions.
- Keep raw snapshots immutable where storage is permitted; write cleaned outputs to separate locations.
- If you are unsure whether data can be shared, ask the team before committing it.

### 7. Test and review your changes

Before opening a pull request:

1. Run the relevant tests and checks available in the repository.
2. Run the changed pipeline step or notebook from a clean, documented starting point when feasible.
3. Inspect outputs for obvious data-quality issues, unexpected row loss, duplicates, or misleading visualizations.
4. Remove temporary files, local database files, credentials, and unrelated edits from the change.
5. Update documentation and include a small sample of expected output when it helps reviewers.

If the repository does not yet have automated tests or a standard test command, state which manual checks you performed rather than claiming tests passed.

### 8. Open a pull request

Push your branch and open a PR against `main`:

```bash
git add <files-you-changed>
git commit -m "feat: add canonical skill mapping"
git push -u origin <your-branch-name>
```

Use a short, descriptive commit message. Suggested prefixes are `feat:`, `fix:`, `data:`, `analysis:`, `docs:`, `test:`, and `refactor:`.

Every PR should explain:

- **Purpose:** What issue or project need does this address?
- **Changes:** What did you change?
- **Validation:** Which tests, scripts, or manual checks did you run?
- **Data impact:** Did the change affect fields, row counts, cleaning rules, skill mappings, or the database schema?
- **Evidence:** Include relevant screenshots, charts, query results, or a small non-sensitive sample if useful.
- **Limitations:** Mention known gaps, assumptions, or follow-up work.

Link the related issue when one exists. Request review from the contributor responsible for the affected workstream. Do not merge your own PR unless the team has explicitly agreed to that process; resolve review comments and wait for approval first.

### 9. Definition of done

A contribution is ready to merge when:

- [ ] It solves the agreed task and stays within its intended scope.
- [ ] Relevant tests/checks have been run, and their results are reported accurately.
- [ ] Data assumptions, schema changes, and limitations are documented.
- [ ] No secrets or unauthorized data are included.
- [ ] Related README, setup instructions, and examples are updated where needed.
- [ ] A reviewer has approved the change and any requested revisions are resolved.

**When in doubt:** open an issue or ask the team before making a breaking change to the data contract, database schema, source choice, or shared pipeline. Early communication is preferable to incompatible work that must be rewritten.

---

## Dataset Strategy

The team should select a source only after checking access conditions, license/terms, geographic coverage, field availability, and suitability for the intended academic use.

Potential starting points to investigate:

- **Adzuna API:** https://developer.adzuna.com/overview — investigate available endpoints and verify Pakistan coverage and current usage terms before committing.
- **Pakistan-focused job-market research referenced in the project proposal:** https://www.preprints.org/manuscript/202609.0274 — useful as research context; the underlying dataset must be separately confirmed as available and reusable.
- **Kaggle datasets:** https://www.kaggle.com/datasets — search for job-posting datasets, then inspect the specific dataset's license, provenance, fields, date range, and completeness.

### Dataset acceptance checklist

- [ ] Use is permitted for the intended course/project.
- [ ] Source and collection date can be documented.
- [ ] Job title and description are available.
- [ ] Company and location fields are available where possible.
- [ ] Posting date and work/employment type are available where possible.
- [ ] Salary availability is measured, not assumed.
- [ ] The dataset has sufficient records and coverage for the intended questions.
- [ ] Duplicate handling and missing values can be assessed.

**Never invent missing salary values or treat missing salary as zero.** If the chosen source does not support salary analysis, report that limitation or select a more suitable source.

## Getting Started

The commands below are a general setup template. They will work only after the repository contains the referenced files and a dependency list.

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd jobstack
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Once the team has created the dependency file:

```bash
pip install -r requirements.txt
```

If the repository uses `pyproject.toml` instead, follow the installation instructions defined there.

### 4. Configure environment variables

If an API is selected, copy `.env.example` to `.env` and fill in the required values locally.

```text
# Example only — use the actual variable names required by the chosen source
JOB_API_KEY=replace_with_your_key
```

Do not commit `.env` or API credentials.

### 5. Run the pipeline

The final run commands should be added here after the team implements and tests the entry points. A reproducible Project 1 run should execute:

1. Data extraction
2. Validation and data-quality reporting
3. Transformation and skill extraction
4. SQL database creation/loading
5. EDA and report generation

> **Repository setup status:** replace this note with tested commands once the scripts are implemented. Do not advertise untested commands as working.

## Quality, Ethics & Limitations

JobStack is intended to provide transparent analysis, not definitive claims about the entire labor market.

- **Data licensing:** follow the source's terms; public visibility does not automatically grant permission to scrape or redistribute.
- **Missing salaries:** report salary coverage and analyze only suitable records.
- **Duplicate postings:** identify and document duplicate handling to reduce distorted counts.
- **Skill ambiguity:** retain evidence and manually inspect samples where possible.
- **Sampling bias:** describe findings as patterns in the collected postings, not a census of all vacancies.
- **Temporal drift:** use posting dates where available and avoid unsupported trend claims.
- **Causality:** salary differences by skill are associations unless a suitable causal design supports stronger conclusions.
- **Privacy:** avoid collecting or exposing unnecessary personal information.

## Milestones

| Milestone | Completion evidence |
|---|---|
| **1. Source & schema** | Source reviewed, terms documented, schema agreed, sample data stored |
| **2. ETL** | Repeatable extraction, validation, cleaning, and skill extraction |
| **3. SQL database** | Normalized schema, loading script, integrity checks, useful queries |
| **4. EDA** | Reproducible charts, summaries, findings, and limitations |
| **5. Integration** | One documented end-to-end run from source data to final analysis |
| **6. Final handover** | README, ERD, data-quality report, findings, and presentation/demo materials |

## Future Roadmap

### Project 2 — Classical Machine Learning
- Build a salary-estimation baseline and compare suitable scikit-learn models where salary coverage supports it.
- Use reproducible preprocessing, cross-validation, tuning, and held-out evaluation.
- Explore interpretable job-fit scoring and skill-gap outputs.

### Project 3 — Deep Learning & MLOps
- Compare a PyTorch job–candidate matching model against a meaningful baseline.
- Use Optuna for systematic hyperparameter optimization.
- Use MLflow to track parameters, metrics, model versions, and artifacts.
- Communicate model limitations and the evidence behind matching outputs.

These are planned stages, not claims that the functionality is already implemented.

## Contributing

Team members should:

1. Work in their assigned component and keep changes focused.
2. Use descriptive branch names and commit messages.
3. Add or update tests when changing reusable logic.
4. Document new fields, assumptions, data mappings, and query definitions.
5. Never commit credentials or data that cannot be redistributed.
6. Open a pull request and explain how the changes were tested.
7. Keep interfaces and data contracts aligned with the team.

## Project Status

**Current focus:** Project 1 — ETL, SQL database engineering, and exploratory data analysis.

As development progresses, update this README with verified setup commands, actual dataset/source details, schema/ERD, test instructions, representative findings, screenshots, and a demo link.

## Acknowledgements & References

- JobStack project proposal (Fall 2026).
- Adzuna API documentation: https://developer.adzuna.com/overview
- Pakistan IT job-market research referenced in the proposal: https://www.preprints.org/manuscript/202609.0274
- Kaggle dataset catalogue: https://www.kaggle.com/datasets

---

<div align="center">

**JobStack**  
*Understand the market. Identify the skills. Make better career decisions.*

</div>
#   J o b S t a c k - t h r o u g h - p y t h o n  
 