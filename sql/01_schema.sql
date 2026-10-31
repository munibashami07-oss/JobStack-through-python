-- JobStack Project 1 | Person 3 | 01_schema.sql
-- Creates the 6 normalized tables, with primary keys, foreign keys,
-- UNIQUE rules, NOT NULL rules and CHECK constraints.
-- Parent tables first, child tables after (order matters for FKs).

PRAGMA foreign_keys = ON;   -- SQLite ignores foreign keys unless this is ON (per connection)

-- 1. companies: one row per company name
CREATE TABLE companies (
    company_id    INTEGER PRIMARY KEY,
    company_name  TEXT NOT NULL UNIQUE
);

-- 2. locations: one row per (city, country). country is NULL where the source gave none.
CREATE TABLE locations (
    location_id  INTEGER PRIMARY KEY,
    city         TEXT NOT NULL,
    country      TEXT,
    UNIQUE (city, country)
);

-- 3. skills: canonical skill names (category stays NULL: no source provides it)
CREATE TABLE skills (
    skill_id        INTEGER PRIMARY KEY,
    canonical_name  TEXT NOT NULL UNIQUE,
    category        TEXT
);

-- 4. postings: one row per job posting.
-- posting_pk is our own surrogate key, because posting_id alone is NOT unique across sources.
-- The natural identity (source, source_posting_id) is enforced with UNIQUE.
CREATE TABLE postings (
    posting_pk          INTEGER PRIMARY KEY,
    source              TEXT NOT NULL,
    source_posting_id   TEXT NOT NULL,
    source_url          TEXT,
    title               TEXT NOT NULL,
    standardized_title  TEXT,
    description         TEXT NOT NULL,      -- cleaned text (HTML stripped by Person 2)
    company_id          INTEGER,            -- NULL when company is unknown
    location_id         INTEGER,            -- NULL when city is unknown
    category            TEXT,
    experience          TEXT,
    employment_type     TEXT,
    work_mode           TEXT NOT NULL CHECK (work_mode IN ('remote', 'onsite', 'hybrid', 'unknown')),
    posted_at           TEXT,               -- ISO-8601 text; SQLite has no real datetime type
    language            TEXT,
    UNIQUE (source, source_posting_id),
    FOREIGN KEY (company_id)  REFERENCES companies (company_id),
    FOREIGN KEY (location_id) REFERENCES locations (location_id)
);

-- 5. posting_skills: the MANY-TO-MANY link table (one job has many skills, one skill is in many jobs)
CREATE TABLE posting_skills (
    posting_pk         INTEGER NOT NULL,
    skill_id           INTEGER NOT NULL,
    extraction_method  TEXT NOT NULL DEFAULT 'dictionary_match',
    evidence           TEXT,                -- NULL: the transformation step did not store evidence
    PRIMARY KEY (posting_pk, skill_id),     -- composite key: the same skill cannot repeat for one posting
    FOREIGN KEY (posting_pk) REFERENCES postings (posting_pk),
    FOREIGN KEY (skill_id)   REFERENCES skills (skill_id)
);

-- 6. salary_observations: only for postings that actually show salary information.
-- Missing salary is NULL, never 0.
CREATE TABLE salary_observations (
    salary_id    INTEGER PRIMARY KEY,
    posting_pk   INTEGER NOT NULL,
    salary_min   REAL,
    salary_max   REAL,
    currency     TEXT,
    pay_period   TEXT,
    salary_text  TEXT,
    CHECK (salary_min IS NULL OR salary_min >= 0),
    CHECK (salary_min IS NULL OR salary_max IS NULL OR salary_max >= salary_min),
    FOREIGN KEY (posting_pk) REFERENCES postings (posting_pk)
);
