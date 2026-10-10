# JobStack

### From Job Postings to Skills Intelligence, Prediction & Career Decision Support

```{=html}
<p align="center">
```
`<strong>`{=html}Turn job-market data into evidence-based career
decisions.`</strong>`{=html}
```{=html}
</p>
```
```{=html}
<p align="center">
```
```{=html}
<!-- Replace these placeholders after the repository is published/configured. -->
```
`<img src="https://img.shields.io/badge/status-in%20development-orange" alt="Project status: in development">`{=html}
`<img src="https://img.shields.io/badge/focus-Pakistan%20tech%20market-5B45E8" alt="Focus: Pakistan tech market">`{=html}
`<img src="https://img.shields.io/badge/license-TBD-lightgrey" alt="License to be decided">`{=html}
```{=html}
</p>
```
JobStack is a Pakistan-focused job-market intelligence project that
transforms job advertisements into structured, useful insights. It aims
to help students, job seekers, recruiters, HR teams, and universities
understand which skills employers request, how skills relate to
advertised salaries, how closely a candidate matches a role, and which
skill gaps may be worth addressing next.

> **Our north star:** Don't build a website that merely tells people
> where jobs are. Build a system that helps them understand the market
> and decide what to do next.

------------------------------------------------------------------------

## Contents

-   [Why JobStack?](#why-jobstack)
-   [Project Goals](#project-goals)
-   [Planned Features](#planned-features)
-   [Project Roadmap](#project-roadmap)
-   [Proposed Architecture](#proposed-architecture)
-   [Technology Stack](#technology-stack)
-   [Data Principles](#data-principles)
-   [Getting Started](#getting-started)
-   [Contributing](#contributing)
-   [Development Guidelines](#development-guidelines)
-   [Evaluation and Quality](#evaluation-and-quality)
-   [Limitations and Responsible Use](#limitations-and-responsible-use)
-   [Team and Acknowledgements](#team-and-acknowledgements)
-   [References](#references)

## Why JobStack?

Job advertisements contain signals about skills, experience, location,
work arrangements, education, and sometimes salary. But those signals
are difficult to use directly: job titles and skill names vary, salary
information is often missing, duplicate listings can distort counts, and
a long list of vacancies rarely explains what someone should do next.

JobStack is designed to add a structured, evidence-driven intelligence
layer between raw postings and practical decisions.

  -----------------------------------------------------------------------
  Question                            Intended JobStack insight
  ----------------------------------- -----------------------------------
  What are employers asking for?      Ranked skills, roles, locations,
                                      companies, and demand trends

  Which skills appear together?       Skill co-occurrence analysis and
                                      skill-network insights

  What salary is advertised for a     Salary distributions and estimates
  role?                               where reliable data permits

  How well does a candidate fit a     An explainable fit score, matched
  role?                               skills, and missing skills

  What should a candidate learn next? Prioritized skill gaps informed by
                                      observed demand and model evidence

  How can organizations understand    Role/skill demand, salary
  the market?                         benchmarking, and talent-market
                                      indicators
  -----------------------------------------------------------------------

### Who is it for?

-   **Students and job seekers** --- explore in-demand skills and
    identify potential learning priorities.
-   **Recruiters and talent teams** --- investigate role requirements
    and market patterns.
-   **Engineering leaders and employers** --- compare recurring skill
    requirements across roles.
-   **Universities and training providers** --- explore how observed
    job-market demand relates to learning outcomes.

The initial scope is deliberately focused on Pakistan's technology job
market. JobStack is an intelligence and decision-support project, not a
job board or an automated hiring authority.

## Project Goals

1.  Build a reproducible pipeline that collects legally usable job data
    and validates its structure.
2.  Clean and normalize job titles, locations, work arrangements, salary
    fields, and skill names.
3.  Store postings and their many-to-many skill relationships in a
    relational database.
4.  Explore skill demand, skill combinations, geographic differences,
    and advertised salary patterns.
5.  Build and evaluate classical machine-learning baselines for salary
    estimation and job-fit support.
6.  Compare a PyTorch-based job--candidate matching model against a
    meaningful baseline.
7.  Track experiments and model artifacts to make results reproducible.
8.  Present insights through a responsive web dashboard with clear
    explanations and limitations.

## Planned Features

Features below describe the intended scope; they should not be
interpreted as already implemented.

### Market intelligence

-   Skill demand by role, city, experience level, and time period
-   Skill co-occurrence and role similarity exploration
-   Salary distributions for records with usable salary information
-   Company and location comparisons where data coverage supports them
-   Trends over time when historical data is available

### Candidate decision support

-   Candidate/job fit score
-   Clearly listed matched and missing skills
-   Prioritized skill-gap suggestions
-   Salary estimates or bands when the data is sufficient
-   Explanations of the factors that contributed to a result

### Experimentation and model tracking

-   Reproducible scikit-learn pipelines
-   Cross-validation and hyperparameter search
-   Held-out model evaluation
-   PyTorch matching model compared with a classical baseline
-   Optuna optimization and MLflow experiment tracking

### Possible future extensions

These are optional and should follow a stable core pipeline: - Career
path exploration - Personalized learning roadmaps - Market trend
alerts - Resume-to-job matching - Curriculum-to-market alignment -
Recruiter-focused market views

## Project Roadmap

JobStack is planned as one product that grows across three technical
stages rather than three disconnected assignments.

  -----------------------------------------------------------------------
  Stage                   Focus                   Planned deliverables
  ----------------------- ----------------------- -----------------------
  **Project 1 --- Data    ETL, validation, SQL,   Documented data source,
  foundation**            and exploratory data    validated dataset,
                          analysis                normalized schema,
                                                  reproducible analysis,
                                                  and findings

  **Project 2 ---         scikit-learn salary     Preprocessing/model
  Classical ML**          estimation and job-fit  pipeline,
                          baseline                cross-validation,
                                                  tuning, held-out
                                                  evaluation, and error
                                                  analysis

  **Project 3 --- Deep    PyTorch matching,       Neural model,
  learning & MLOps**      Optuna, and MLflow      optimization study,
                                                  experiment history, and
                                                  comparison with
                                                  baseline

  **Product layer**       Responsive web          Dashboard, filters,
                          application and REST    forms, visualizations,
                          API                     and model outputs

  **Validation**          Feedback from relevant  Structured feedback,
                          professionals           documented limitations,
                                                  and visible
                                                  improvements
  -----------------------------------------------------------------------

## Proposed Architecture

``` text
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

### Suggested data model

The proposal recommends a normalized relational design. The final schema
may evolve with implementation.

-   `postings` --- job title, company, location, description,
    experience, work mode, date, and source
-   `companies` --- company metadata where available
-   `locations` --- city, province, and country
-   `skills` --- canonical skill names and categories
-   `posting_skills` --- many-to-many relationship between postings and
    skills, including evidence and extraction metadata
-   `salary_observations` --- salary range, currency, pay period, and
    normalized salary where possible

A posting can require many skills, and a skill can appear in many
postings. The `posting_skills` relationship is therefore central to the
model.

## Technology Stack

The following stack is proposed in the project plan. Exact dependencies
and versions should be confirmed in the repository as implementation
progresses.

  -----------------------------------------------------------------------
  Layer                   Proposed tools          Purpose
  ----------------------- ----------------------- -----------------------
  Data ingestion          Python, `requests` or a Retrieve source data
                          permitted API client    

  Validation              Pydantic                Validate schemas and
                                                  data quality

  Transformation          Pandas                  Clean data and engineer
                                                  features

  Database                PostgreSQL or SQLite    Store normalized
                          for a course-scale      records
                          prototype               

  Analysis                Pandas, Matplotlib or   Explore and visualize
                          Plotly                  patterns

  Classical ML            scikit-learn            Build and evaluate
                                                  prediction baselines

  Deep learning           PyTorch                 Learn job--candidate
                                                  compatibility

  Hyperparameter          Optuna                  Run systematic tuning
  optimization                                    

  Experiment tracking     MLflow                  Track parameters,
                                                  metrics, artifacts, and
                                                  model versions

  Backend                 FastAPI                 Expose data and model
                                                  functionality through
                                                  an API

  Frontend                React or another        Provide an interactive
                          team-approved web       dashboard
                          framework               
  -----------------------------------------------------------------------

## Data Principles

Data quality and lawful use are core project requirements, not optional
cleanup tasks.

-   **Use permitted sources.** Prefer official APIs, licensed datasets,
    or data whose collection and reuse are allowed by its terms.
-   **Document provenance.** Record the source, collection date, and
    relevant usage conditions for each dataset.
-   **Validate before analysis.** Check required fields, types, ranges,
    duplicates, and inconsistent values.
-   **Normalize carefully.** Preserve original text when useful, and
    retain evidence for extracted or canonicalized skills.
-   **Handle missing salary values honestly.** Missing salary is not
    zero; salary models should use only records suitable for the chosen
    target.
-   **Avoid duplicate inflation.** Identify likely duplicate postings
    and document the deduplication approach.
-   **Preserve time context.** Job-market signals change, so retain
    posting dates when available.
-   **Protect personal information.** Do not commit personal data,
    secrets, credentials, or unnecessary candidate information to the
    repository.

## Getting Started

> **Implementation note:** The project proposal defines the intended
> architecture and stack, but it does not specify the final repository
> structure, dependency files, environment variable names, or completed
> setup commands. The instructions below are a safe starting template.
> Update them to match the actual implementation before treating this
> README as a release guide.

### Prerequisites

Depending on which project stages are implemented, contributors may
need:

-   Python 3.11 or another version specified by the project
-   Git
-   A supported SQL database (SQLite may be sufficient for an initial
    prototype)
-   Node.js and npm if the frontend uses React
-   API credentials only if an approved data source requires them

### 1. Clone the repository

Replace `<repository-url>` with the actual Git remote URL.

``` bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Python environment

``` bash
python -m venv .venv
```

Activate it:

**Windows (PowerShell):**

``` powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

``` bash
source .venv/bin/activate
```

### 3. Install backend dependencies

Once the project has a committed dependency file, install from that
file. For example, if it uses `requirements.txt`:

``` bash
pip install -r requirements.txt
```

If the backend has its own dependency file or uses `pyproject.toml`,
follow the instructions in that directory instead.

### 4. Configure environment variables

If the application requires configuration, create a local `.env` file
based on a maintained `.env.example` file. Use only variable names
documented by the project.

``` text
# Example placeholders only — replace with the project's actual variables.
DATABASE_URL=
JOB_DATA_API_KEY=
```

Never commit `.env` files, API keys, passwords, database credentials, or
other secrets. Keep `.env.example` free of real credentials.

### 5. Prepare the database and data

Follow the repository's documented database initialization and migration
commands. Use a small, permitted sample dataset for local development.
Do not assume that a database schema, migration system, or
data-ingestion command exists until it has been added to the repository.

### 6. Run the application

Start the backend and frontend using the commands documented in their
respective directories. For a FastAPI application, the command may
resemble the following if the application entry point is `app.main:app`:

``` bash
uvicorn app.main:app --reload
```

This is an example only; verify the actual entry point and configuration
before use. If a frontend is present, install its dependencies and run
its documented development script.

### 7. Run checks

Before opening a pull request, run the available tests, linting,
formatting, and type checks. Add reproducible commands to this README as
these tools are selected.

## Contributing

Contributions are welcome! JobStack is modular by design, so
contributors can help with data engineering, analytics, machine
learning, model evaluation, backend APIs, frontend experience,
documentation, and testing.

### Ways to contribute

-   Improve data validation, normalization, or deduplication.
-   Add tests for data transformations and skill extraction.
-   Improve SQL schema design or analytical queries.
-   Build clear visualizations with appropriate context and coverage
    information.
-   Develop and evaluate a salary-estimation or job-fit baseline.
-   Improve matching explanations and skill-gap prioritization.
-   Add experiment tracking or improve reproducibility.
-   Improve accessibility, responsive design, documentation, and setup
    instructions.
-   Review data-source terms and document data provenance.

### Contribution workflow

1.  **Check existing work.** Review open issues and pull requests before
    starting. For a significant change, open an issue or discussion
    first to agree on scope.

2.  **Fork the repository** if you do not have direct write access.

3.  **Create a focused branch** from the default branch.

    ``` bash
    git checkout -b type/short-description
    ```

    Suggested prefixes: `feature/`, `fix/`, `docs/`, `test/`,
    `refactor/`, and `data/`.

4.  **Make a focused change.** Keep pull requests small enough to
    review. Avoid mixing unrelated refactors and features.

5.  **Add or update tests.** Include tests for bug fixes and new
    behavior where practical. For data or model changes, document the
    expected behavior and evaluation method.

6.  **Run checks locally.** Run the project's available test suite,
    formatter, linter, and relevant pipeline checks.

7.  **Commit with a clear message.**

    ``` bash
    git add .
    git commit -m "docs: improve contributor setup guide"
    ```

    Use concise messages that explain the change. Examples:

    -   `feat: add canonical skill normalization`
    -   `fix: handle missing salary ranges`
    -   `test: cover duplicate posting detection`
    -   `docs: clarify local database setup`

8.  **Push your branch** and open a pull request against the default
    branch.

9.  **Describe the change.** Explain the problem, solution, how it was
    tested, and any trade-offs or limitations. Link related issues and
    include screenshots for meaningful UI changes.

10. **Respond to review feedback** and keep the pull request up to date
    with the project's contribution requirements.

### Pull request checklist

Before requesting review, confirm that:

-   [ ] The change addresses one clear problem or improvement.
-   [ ] Existing behavior is preserved unless the change intentionally
    updates it.
-   [ ] Tests or a clear manual verification plan are included.
-   [ ] Documentation and configuration examples are updated where
    needed.
-   [ ] No credentials, private data, or unlicensed datasets are
    included.
-   [ ] New dependencies are justified and documented.
-   [ ] Model results include suitable metrics and limitations.
-   [ ] UI changes are responsive and accessible where applicable.

### Reporting bugs and proposing features

When opening an issue, include the relevant context:

**Bug report** - What happened? - What did you expect to happen? - Steps
to reproduce - Relevant logs or screenshots, with secrets removed -
Environment and versions, if relevant

**Feature request** - What user problem does it solve? - Who benefits
from it? - What is a reasonable first version? - How could success be
evaluated? - Are there data, privacy, licensing, or maintenance
concerns?

### Data and model contributions

For changes involving datasets, skill extraction, or ML:

-   Include source and licensing/provenance details.
-   Explain cleaning, deduplication, and missing-value handling.
-   Avoid committing large raw datasets unless repository policy and the
    data license explicitly allow it.
-   Use train/validation/test separation appropriately; do not tune on
    the held-out test set.
-   Compare complex models with a relevant baseline.
-   Report metrics, data coverage, and important failure cases.
-   Do not present correlations as proof of causation or model scores as
    hiring decisions.

## Development Guidelines

-   **Prefer clarity over cleverness.** Keep modules focused and
    interfaces documented.
-   **Make work reproducible.** Fix random seeds where appropriate and
    document data/model versions.
-   **Validate at boundaries.** Check data before it enters the database
    or model pipeline.
-   **Keep secrets out of version control.** Use environment variables
    and local configuration.
-   **Explain model output.** Show relevant matched/missing skills and
    limitations alongside scores.
-   **Do not overstate findings.** Describe what the observed dataset
    supports, not what the entire labor market must be doing.
-   **Document architectural changes.** Update diagrams, setup
    instructions, and design notes when the implementation changes.

## Evaluation and Quality

JobStack should be evaluated on more than whether the code runs.

### Data pipeline

-   Schema validation and failure handling
-   Duplicate detection and normalization quality
-   Skill extraction examples and evidence
-   Data coverage and missingness summaries
-   Reproducibility of ingestion and analysis

### Analytics

-   Clear definitions for counts, rates, and salary summaries
-   Appropriate comparisons by role, geography, experience, and time
-   Transparent treatment of incomplete or biased samples

### Machine learning

-   A simple baseline before a complex model
-   Cross-validation and tuning without test-set leakage
-   Appropriate metrics (for example, MAE/RMSE for salary estimates)
-   Error analysis and comparison across relevant slices
-   Documented model versions, parameters, and limitations

### Product

-   Clear labels and explanations
-   Useful filters and understandable visualizations
-   Responsive, accessible interface
-   No suggestion that a match score is a definitive hiring
    recommendation

## Limitations and Responsible Use

JobStack analyzes **observed job advertisements**, not every vacancy or
the entire labor market. Its results may be affected by incomplete
salary disclosure, duplicate listings, source coverage, ambiguous skill
terminology, changing demand, and bias in historical postings.

-   Salary relationships are observational; an association between a
    skill and advertised pay does not prove that the skill causes higher
    pay.
-   Predictions are estimates, not guarantees of salary or employment
    outcomes.
-   A job-fit score is decision support, not a hiring decision or a
    measure of a person's worth.
-   Results should include uncertainty and data limitations where
    relevant.
-   Data collection and reuse must comply with applicable laws, platform
    terms, and dataset licenses.
-   Personal or sensitive candidate data should be minimized and handled
    carefully.

## Team and Acknowledgements

JobStack is a collaborative project concept intended to bring data
engineering, analytics, machine learning, deep learning/MLOps, and
product development into one coherent system.

Add team member names, roles, institutional affiliation (if
appropriate), and individual contributions here as the team is
finalized.

## References

These sources were identified in the project proposal as useful starting
points for understanding job-posting analytics, data access, and the
Pakistan technology labor market:

-   [Lightcast --- Job Postings](https://lightcast.io/our-data/postings)
-   [Lightcast --- Job Posting Analytics
    Methodology](https://kb.lightcast.io/en/articles/6957446-job-posting-analytics-jpa-methodology)
-   [Adzuna API Overview](https://developer.adzuna.com/overview)
-   [Adzuna Jobsworth](https://developer.adzuna.com/docs/jobsworth)
-   [P@SHA Skills Survey 2025
    summary](https://www.linkedin.com/posts/pashapk_pashareport-skillsreport2025-pashaskillssurvey-activity-7370781643378331648-YKM_)
-   [Analysing IT Job Market Dynamics in Pakistan (2026
    preprint)](https://www.preprints.org/manuscript/202609.0274)
-   [Indeed --- Software Engineer salary in
    Pakistan](https://pk.indeed.com/career/software-engineer/salaries)

These references provide context; they are not necessarily JobStack's
data sources. Any source used to populate the project must be reviewed
independently for access, licensing, and reuse conditions.

------------------------------------------------------------------------

```{=html}
<p align="center">
```
`<strong>`{=html}JobStack --- From raw job postings to clearer career
decisions.`</strong>`{=html}
```{=html}
</p>
```
