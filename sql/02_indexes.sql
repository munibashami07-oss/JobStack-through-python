-- JobStack Project 1 | Person 3 | 02_indexes.sql
-- Indexes speed up JOINs and GROUP BY. PRIMARY KEY and UNIQUE columns already have indexes.
CREATE INDEX idx_postings_company       ON postings (company_id);
CREATE INDEX idx_postings_location      ON postings (location_id);
CREATE INDEX idx_postings_std_title     ON postings (standardized_title);
CREATE INDEX idx_postings_work_mode     ON postings (work_mode);
CREATE INDEX idx_posting_skills_skill   ON posting_skills (skill_id);
CREATE INDEX idx_salary_posting         ON salary_observations (posting_pk);
