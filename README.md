# 📊 JobStack

**Turn Pakistan tech job postings into skills intelligence, salary and fit prediction, and evidence-based career decisions.**

![Status](https://img.shields.io/badge/Status-Early%20Development-FF9F1C?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![PyTorch](https://img.shields.io/badge/DL-PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![License](https://img.shields.io/badge/License-TBD-lightgrey?style=for-the-badge)

> 🧭 **North star:** Don't build a website that merely tells people where jobs are. Build a system that helps them understand the market and decide what to do next.

---

## 🚧 Project status

JobStack is in **early development**. Project 1, step 1 (data acquisition and validation) is implemented: ingestion adapters, Pydantic validation, tests and a data quality report. Everything else marked 🗓️ *Planned* describes the intended design and will be updated as code is added.

---

## ✨ What is this?

Job ads hold useful signals about skills, experience, location, work mode, and sometimes salary. They are hard to use directly:

🔀 Job titles and skill names vary · 💸 Salary is often missing · 👯 Duplicate listings distort counts · 🤷 A list of vacancies doesn't say what to do next

JobStack adds a structured, evidence-driven layer between raw postings and practical decisions. It starts with Pakistan's technology job market. It is a **decision-support project**, not a job board or an automated hiring authority.

### 👥 Who it's for

| Audience | What they get |
|---|---|
| 🎓 Students and job seekers | In-demand skills and learning priorities |
| 🧑‍💼 Recruiters and talent teams | Role requirements and market patterns |
| 🛠️ Engineering leaders | Recurring skill requirements across roles |
| 🏫 Universities and training providers | How job-market demand relates to learning outcomes |

---

## 🎯 Key features

> 🗓️ *Planned. Not yet implemented.*

| Area | Feature |
|---|---|
| 📈 **Market intelligence** | Skill demand by role, city, experience level, and time period |
| 🕸️ **Skill networks** | Skill co-occurrence and role similarity exploration |
| 💰 **Salary insight** | Salary distributions for records with usable salary data |
| 🎯 **Job-fit score** | Explainable score with matched and missing skills |
| 🧗 **Skill gaps** | Prioritized suggestions for what to learn next |
| 🔬 **Experiment tracking** | Reproducible pipelines, tuning, and model comparison |

---

## 🔁 How it works

```mermaid
flowchart LR
    A[📥 Permitted job data] --> B[✅ Validate<br/>Pydantic]
    B --> C[🧹 Clean, normalize,<br/>deduplicate]
    C --> D[(🗄️ SQL database)]
    D --> E[📊 EDA and analytics]
    D --> F[⚙️ Feature engineering]
    F --> G[🌲 scikit-learn<br/>baselines]
    F --> H[🔥 PyTorch matching<br/>+ Optuna]
    G --> I[📒 MLflow tracking]
    H --> I
    I --> J[🚀 FastAPI]
    J --> K[🖥️ Web dashboard]
```

---

## 🧰 Tech stack

| Layer | Tools | Purpose |
|---|---|---|
| 📥 Ingestion | Python, `requests` or a permitted API client | Retrieve source data |
| ✅ Validation | Pydantic | Schema and data-quality checks |
| 🧹 Transformation | Pandas | Cleaning and feature engineering |
| 🗄️ Database | PostgreSQL (SQLite for prototyping) | Normalized storage |
| 📊 Analysis | Pandas, Matplotlib / Plotly | Exploration and visualization |
| 🌲 Classical ML | scikit-learn | Prediction baselines |
| 🔥 Deep learning | PyTorch | Job-candidate compatibility |
| 🎛️ Tuning | Optuna | Hyperparameter optimization |
| 📒 Tracking | MLflow | Parameters, metrics, artifacts, model versions |
| 🚀 Backend | FastAPI | REST API |
| 🖥️ Frontend | React (or team-approved framework) | Interactive dashboard |

### 🗃️ Data model

| Table | Description |
|---|---|
| `postings` | Title, company, location, description, experience, work mode, date, source |
| `companies` | Company metadata where available |
| `locations` | City, province, country |
| `skills` | Canonical skill names and categories |
| `posting_skills` | Many-to-many link between postings and skills, with evidence metadata |
| `salary_observations` | Salary range, currency, pay period, normalized salary |

### 🗺️ Roadmap

| Stage | Focus | Status |
|---|---|---|
| 1️⃣ Data foundation | ETL, validation, SQL, EDA | 🟨 In progress |
| 2️⃣ Classical ML | Salary estimation and job-fit baseline | ⬜ Not started |
| 3️⃣ Deep learning and MLOps | PyTorch matching, Optuna, MLflow | ⬜ Not started |
| 🖥️ Product layer | Web app and REST API | ⬜ Not started |
| 🧪 Validation | Professional feedback | ⬜ Not started |

---

## 🚀 Quick start

> ⚠️ The data acquisition and validation step can be run now (see "Run the data pipeline" below). The API and web app are planned.

**1. 📦 Clone the repository**

```bash
git clone https://github.com/munibashami07-oss/JobStack-through-python.git
cd JobStack-through-python
```

**2. 🐍 Create a virtual environment**

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

**3. 📥 Install dependencies**

```bash
pip install -r requirements.txt
```

**4. 🔐 Configure environment** *(not needed for the current data sources)*

```bash
cp .env.example .env
```

**5. ▶️ Run the API** *(planned)*

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Usage examples and configuration

> 🗓️ *Planned. Endpoints and module names are illustrative.*

### ⚙️ Configuration

| Variable | Description | Required |
|---|---|---|
| `DATABASE_URL` | Database connection string | ✅ Yes |
| `JOB_DATA_API_KEY` | Key for an approved job-data API | Only if the source requires it |

🔒 Never commit `.env` files or credentials.

### 🔎 Query the API

```bash
# Top skills for a role
curl "http://127.0.0.1:8000/skills/top?role=backend&city=Lahore"
```

```bash
# Job-fit score for a candidate profile
curl -X POST "http://127.0.0.1:8000/fit" \
  -H "Content-Type: application/json" \
  -d '{"skills": ["python", "sql", "fastapi"], "target_role": "data engineer"}'
```

### 🏭 Run the data pipeline (Project 1: data acquisition and validation)

No API key or `.env` file is needed for the current sources.

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) fetch fresh API snapshots into data/raw/
python -m src.ingestion.fetch_arbeitnow
python -m src.ingestion.fetch_remotive

# 3. Validate raw data -> data/validated/jobs_valid.json
python -m src.validation.run_all

# 4. Load a flat table for the quality report (not the final database)
python -m src.ingestion.load_db

# 5. Generate the report -> reports/data_quality/data_quality_report.md
python -m src.validation.quality_report

# Run the tests
python -m pytest
```

Sources, terms and limits: `reports/data_quality/source_notes.md`.
Field definitions for the next pipeline step: `reports/data_quality/data_contract.md`.

---

## 🧷 Data principles

- ✅ **Use permitted sources:** official APIs, licensed datasets, or data whose terms allow reuse
- 🧾 **Document provenance:** source, collection date, usage conditions
- 🔍 **Validate before analysis:** fields, types, ranges, duplicates
- 💸 **Missing salary is not zero**
- 👯 **Avoid duplicate inflation** and keep posting dates
- 🔒 **Protect personal information:** never commit personal data, secrets, or credentials

---

## 🧪 Testing and limitations

_To be added._

---

## 🤝 Contributing

Contributions are welcome in data engineering, analytics, ML, backend, frontend, docs, and testing. At this early stage, the most useful help is schema design, data-source review, and project structure.

1. 🔎 **Check existing work.** Review [issues](https://github.com/munibashami07-oss/JobStack-through-python/issues) and [pull requests](https://github.com/munibashami07-oss/JobStack-through-python/pulls). For big changes, open an issue first.
2. 🍴 **Fork** the repo and clone your fork:
   ```bash
   git clone https://github.com/<your-username>/JobStack-through-python.git
   cd JobStack-through-python
   ```
3. 🌿 **Create a focused branch** from `main`:
   ```bash
   git checkout -b type/short-description
   ```
   Prefixes: `feature/` `fix/` `docs/` `test/` `refactor/` `data/`
4. 🛠️ **Make a focused change.** Keep PRs small; don't mix refactors and features.
5. ✅ **Add or update tests.** For data or model changes, document the expected behavior and how you evaluated it.
6. 🧹 **Run checks locally:** tests, formatter, linter (once configured).
7. 💬 **Commit with a clear message:**
   ```bash
   git commit -m "feat: add canonical skill normalization"
   ```
   More examples: `fix: handle missing salary ranges` · `test: cover duplicate posting detection` · `docs: clarify local database setup`
8. 📤 **Push and open a pull request** against `main`. Describe the problem, solution, testing, and trade-offs. Add screenshots for UI changes.
9. 🔁 **Respond to review feedback.**

### ☑️ Pull request checklist

- [ ] Addresses one clear problem or improvement
- [ ] Preserves existing behavior unless intentionally changed
- [ ] Includes tests or a manual verification plan
- [ ] Updates docs and configuration examples
- [ ] Contains no credentials, private data, or unlicensed datasets
- [ ] Justifies and documents new dependencies
- [ ] Reports metrics and limitations for model changes
- [ ] UI changes are responsive and accessible

### 📐 Data and model contributions

- Include source and licensing details
- Explain cleaning, deduplication, and missing-value handling
- Don't commit large raw datasets unless the license allows it
- Keep train/validation/test separate; never tune on the test set
- Compare complex models against a baseline
- Don't present correlations as causation or model scores as hiring decisions

### 🐞 Bugs and feature requests

**Bug report:** what happened, what you expected, steps to reproduce, logs (secrets removed), environment and versions.

**Feature request:** the user problem, who benefits, a reasonable first version, how to measure success, and any data, privacy, licensing, or maintenance concerns.

---

## 📚 References

- [Lightcast: Job Postings](https://lightcast.io/our-data/postings)
- [Lightcast: Job Posting Analytics Methodology](https://kb.lightcast.io/en/articles/6957446-job-posting-analytics-jpa-methodology)
- [Adzuna API Overview](https://developer.adzuna.com/overview)
- [Adzuna Jobsworth](https://developer.adzuna.com/docs/jobsworth)
- [P@SHA Skills Survey 2025 summary](https://www.linkedin.com/posts/pashapk_pashareport-skillsreport2025-pashaskillssurvey-activity-7370781643378331648-YKM_)
- [Analysing IT Job Market Dynamics in Pakistan (2026 preprint)](https://www.preprints.org/manuscript/202609.0274)
- [Indeed: Software Engineer salary in Pakistan](https://pk.indeed.com/career/software-engineer/salaries)

These sources give context and are not necessarily JobStack's data sources. Any source used to populate the project must be reviewed independently for access, licensing, and reuse conditions.

---

   ### Large data files (not stored in Git)
   Download these and place them in the folders shown:
   - arbeitnow_20261014_1917.json → data/raw/  <https://drive.google.com/file/d/17D06lN8BWO9Yki3Csd4P7I_qfricw8Tk/view?usp=sharing>
   - pakistan_jobs.csv → data/raw/  <https://drive.google.com/file/d/1bpqkPq3fgIttTxDKRH-QXgCmTd2UyunZ/view?usp=drive_link>
   - jobs_valid.json → data/validated/  <https://drive.google.com/file/d/1dXQLT3vFhLhiWmUxmWKXDYKKCgqAgwTE/view?usp=sharing>


## ⭐ Support

If JobStack is useful to you, give the repo a **star** ⭐ and share it with someone exploring the tech job market.

Made with ❤️ by **[Imama](https://github.com/Fatima-09-ai)**
