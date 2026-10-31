-- JobStack Project 1 | Person 3 | 03_views.sql
-- Stable analytical views for Person 4 (EDA). A view is a saved SELECT that behaves like a table.

CREATE VIEW v_postings_flat AS
SELECT p.posting_pk, p.source, p.source_posting_id, p.title, p.standardized_title,
       c.company_name, l.city, l.country, p.category, p.experience,
       p.employment_type, p.work_mode, p.posted_at, p.language
FROM postings p
LEFT JOIN companies c ON c.company_id  = p.company_id
LEFT JOIN locations l ON l.location_id = p.location_id;

CREATE VIEW v_posting_skills_flat AS
SELECT ps.posting_pk, s.canonical_name AS skill, ps.extraction_method, ps.evidence
FROM posting_skills ps
JOIN skills s ON s.skill_id = ps.skill_id;

CREATE VIEW v_skill_counts AS
SELECT s.canonical_name AS skill, COUNT(*) AS n_postings
FROM posting_skills ps
JOIN skills s ON s.skill_id = ps.skill_id
GROUP BY s.canonical_name;
