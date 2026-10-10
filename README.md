# JobStack

**Turn Pakistan tech job-postings data into skills intelligence, salary and fit prediction, and evidence-based career decisions.**

![Status: in development](https://img.shields.io/badge/status-in%20development-orange)
![Focus: Pakistan tech market](https://img.shields.io/badge/focus-Pakistan%20tech%20market-5B45E8)
![License: TBD](https://img.shields.io/badge/license-TBD-lightgrey)

> **North star:** Don't build a website that merely tells people where jobs are. Build a system that helps them understand the market and decide what to do next.

## Contents

- [Key Features and Problem Solved](#key-features-and-problem-solved)
- [Tech Stack and Architecture](#tech-stack-and-architecture)
- [Installation and Quick Start](#installation-and-quick-start)
- [Usage Examples and Configuration](#usage-examples-and-configuration)
- [Testing and Limitations](#testing-and-limitations)
- [Contributing](#contributing)
- [References](#references)

---

## Key Features and Problem Solved

### The problem

Job advertisements contain useful signals about skills, experience, location, work mode, and sometimes salary. They are hard to use directly: job titles and skill names vary, salary data is often missing, duplicate listings distort counts, and a long list of vacancies rarely tells anyone what to do next.

JobStack adds a structured, evidence-driven layer between raw postings and practical decisions. The initial scope is Pakistan's technology job market. It is a decision-support project, not a job board or an automated hiring authority.

### Who it is for

| Audience | Value |
|---|---|
| Students and job seekers | Explore in-demand skills and learning priorities |
| Recruiters and talent teams | Investigate role requirements and market patterns |
| Engineering leaders | Compare recurring skill requirements across roles |
| Universities and training providers | Relate job-market demand to learning outcomes |

### Features

> Features describe the intended scope and are not necessarily implemented yet.

**Market intelligence**
- Skill demand by role, city, experience level, and time period
- Skill co-occurrence and role similarity exploration
- Salary distributions for records with usable salary data
- Company and location comparisons where coverage allows

**Candidate decision support**
- Explainable job-fit score with matched and missing skills
- Prioritized skill-gap suggestions
- Salary estimates or bands when data is sufficient

**Experimentation and tracking**
- Reproducible scikit-learn pipelines with cross-validation and tuning
- PyTorch matching model compared against a classical baseline
- Optuna optimization and MLflow experiment tracking

### Roadmap

| Stage | Focus | Deliverables |
|---|---|---|
| 1. Data foundation | ETL, validation, SQL, EDA | Documented source, validated dataset, normalized schema, findings |
| 2. Classical ML | Salary estimation and job-fit baseline | Pipeline, cross-validation, tuning, held-out evaluation |
| 3. Deep learning and MLOps | PyTorch matching, Optuna, MLflow | Neural model, optimization study, baseline comparison |
| Product layer | Web app and REST API | Dashboard, filters, visualizations, model outputs |
| Validation | Professional feedback | Structured feedback and documented improvements |

---

## Tech Stack and Architecture

### Tech stack

| Layer | Tools | Purpose |
|---|---|---|
| Ingestion | Python, `requests` or a permitted API client | Retrieve source data |
| Validation | Pydantic | Schema and data-quality checks |
| Transformation | Pandas | Cleaning and feature engineering |
| Database | PostgreSQL (SQLite for prototyping) | Normalized storage |
| Analysis | Pandas, Matplotlib / Plotly | Exploration and visualization |
| Classical ML | scikit-learn | Prediction baselines |
| Deep learning | PyTorch | Job-candidate compatibility |
| Tuning | Optuna | Hyperparameter optimization |
| Tracking | MLflow | Parameters, metrics, artifacts, model versions |
| Backend | FastAPI | REST API |
| Frontend | React (or team-approved framework) | Interactive dashboard |

Exact dependencies and versions should be confirmed in the repository as implementation progresses.

### Architecture

```text
Permitted job data source / dataset
                |
                v
       Extraction / ingestion
                |
                v
     Validation (Pydantic schemas)
                |
                v
 Cleaning, normalization & deduplication
                |
                v
       Relational SQL database
                |
        +-------+--------+
        |                |
        v                v
  EDA & analytics    Feature engineering
                         |
                  +------+------+
                  |             |
                  v             v
             scikit-learn    PyTorch matching
              baselines      + Optuna tuning
                  |             |
                  +------+------+
                         |
                    MLflow tracking
                         |
                         v
                FastAPI REST service
                         |
                         v
              Responsive web dashboard
```

### Data model

| Table | Description |
|---|---|
| `postings` | Title, company, location, description, experience, work mode, date, source |
| `companies` | Company metadata where available |
| `locations` | City, province, country |
| `skills` | Canonical skill names and categories |
| `posting_skills` | Many-to-many link between postings and skills, with evidence and extraction metadata |
| `salary_observations` | Salary range, currency, pay period, normalized salary |

The schema may evolve with implementation.

### Data principles

- **Use permitted sources:** official APIs, licensed datasets, or data whose terms allow reuse.
- **Document provenance:** record source, collection date, and usage conditions.
- **Validate before analysis:** check fields, types, ranges, and duplicates.
- **Handle missing salary honestly:** missing salary is not zero.
- **Avoid duplicate inflation** and **preserve posting dates**.
- **Protect personal information:** never commit personal data, secrets, or credentials.

---

## Installation and Quick Start

> The commands below are a starting template. Update them to match the actual repository structure, dependency files, and entry points.

### Prerequisites

- Python 3.11+
- Git
- SQLite (prototype) or PostgreSQL
- Node.js and npm (if the frontend uses React)
- API credentials, only if an approved data source requires them

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values (see [Configuration](#configuration)).

### 5. Initialize the database

```bash
# Replace with the project's actual initialization command
python -m app.db.init
```

### 6. Run the application

```bash
# Backend (FastAPI)
uvicorn app.main:app --reload

# Frontend (if present)
cd frontend
npm install
npm run dev
```

The API is then available at `http://127.0.0.1:8000`, with interactive docs at `/docs`.

---

## Usage Examples and Configuration

### Configuration

| Variable | Description | Required |
|---|---|---|
| `DATABASE_URL` | Database connection string | Yes |
| `JOB_DATA_API_KEY` | Key for an approved job-data API | Only if the source requires it |

Never commit `.env` files or credentials. Keep `.env.example` free of real secrets.

### Example: query the API

```bash
# Top skills for a role (illustrative endpoint)
curl "http://127.0.0.1:8000/skills/top?role=backend&city=Lahore"
```

```bash
# Job-fit score for a candidate profile (illustrative endpoint)
curl -X POST "http://127.0.0.1:8000/fit" \
  -H "Content-Type: application/json" \
  -d '{"skills": ["python", "sql", "fastapi"], "target_role": "data engineer"}'
```

Expected output includes a fit score, matched skills, missing skills, and prioritized skill gaps.

### Example: run the pipeline

```bash
python -m pipeline.ingest --source <permitted-source>
python -m pipeline.clean
python -m pipeline.load
```

> Endpoint paths and module names above are placeholders. Replace them as the implementation is finalized.

---

## Testing and Limitations

_To be added._

---

## Contributing

Contributions are welcome in data engineering, analytics, machine learning, backend, frontend, documentation, and testing.

### How to contribute

1. **Check existing work.** Review open issues and pull requests. For a significant change, open an issue first to agree on scope.
2. **Fork** the repository if you lack write access.
3. **Create a focused branch** from the default branch:
   ```bash
   git checkout -b type/short-description
   ```
   Prefixes: `feature/`, `fix/`, `docs/`, `test/`, `refactor/`, `data/`.
4. **Make a focused change.** Keep pull requests small; don't mix unrelated refactors and features.
5. **Add or update tests** for new behavior and bug fixes. For data or model changes, document the expected behavior and evaluation method.
6. **Run checks locally:** tests, formatter, and linter.
7. **Commit with a clear message:**
   ```bash
   git commit -m "feat: add canonical skill normalization"
   ```
   Examples: `fix: handle missing salary ranges`, `test: cover duplicate posting detection`, `docs: clarify local database setup`.
8. **Push and open a pull request** against the default branch. Describe the problem, solution, how it was tested, and any trade-offs. Link related issues and add screenshots for UI changes.
9. **Respond to review feedback.**

### Pull request checklist

- [ ] Addresses one clear problem or improvement
- [ ] Preserves existing behavior unless intentionally changed
- [ ] Includes tests or a manual verification plan
- [ ] Updates documentation and configuration examples
- [ ] Contains no credentials, private data, or unlicensed datasets
- [ ] Justifies and documents new dependencies
- [ ] Reports metrics and limitations for model changes
- [ ] UI changes are responsive and accessible

### Data and model contributions

- Include source and licensing details.
- Explain cleaning, deduplication, and missing-value handling.
- Don't commit large raw datasets unless the license and repository policy allow it.
- Keep train/validation/test separate; never tune on the held-out test set.
- Compare complex models against a baseline.
- Don't present correlations as causation or model scores as hiring decisions.

### Development guidelines

- Prefer clarity over cleverness.
- Make work reproducible (fixed seeds, documented data and model versions).
- Validate data at boundaries.
- Keep secrets out of version control.
- Explain model output with matched and missing skills plus limitations.

### Reporting bugs and requesting features

**Bug report:** what happened, what you expected, steps to reproduce, logs (secrets removed), environment and versions.

**Feature request:** the user problem, who benefits, a reasonable first version, how to measure success, and any data, privacy, licensing, or maintenance concerns.

---

## References

- [Lightcast: Job Postings](https://lightcast.io/our-data/postings)
- [Lightcast: Job Posting Analytics Methodology](https://kb.lightcast.io/en/articles/6957446-job-posting-analytics-jpa-methodology)
- [Adzuna API Overview](https://developer.adzuna.com/overview)
- [Adzuna Jobsworth](https://developer.adzuna.com/docs/jobsworth)
- [P@SHA Skills Survey 2025 summary](https://www.linkedin.com/posts/pashapk_pashareport-skillsreport2025-pashaskillssurvey-activity-7370781643378331648-YKM_)
- [Analysing IT Job Market Dynamics in Pakistan (2026 preprint)](https://www.preprints.org/manuscript/202609.0274)
- [Indeed: Software Engineer salary in Pakistan](https://pk.indeed.com/career/software-engineer/salaries)

These sources provide context and are not necessarily JobStack's data sources. Any source used to populate the project must be reviewed independently for access, licensing, and reuse conditions.

---

**JobStack: from raw job postings to clearer career decisions.**
