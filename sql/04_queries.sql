-- JobStack Project 1 | Person 3 | 04_queries.sql
-- Core metrics. Each query starts with a "-- name:" line (used by run_queries.py).

-- name: jobs_by_city (top 10)
SELECT l.city, COUNT(*) AS n_postings
FROM postings p
JOIN locations l ON l.location_id = p.location_id
GROUP BY l.city
ORDER BY n_postings DESC, l.city
LIMIT 10;

-- name: jobs_by_role (top 10 standardized titles)
SELECT standardized_title, COUNT(*) AS n_postings
FROM postings
GROUP BY standardized_title
ORDER BY n_postings DESC, standardized_title
LIMIT 10;

-- name: skill_frequency (top 15, with share of ALL postings)
SELECT s.canonical_name AS skill,
       COUNT(*) AS n_postings,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM postings), 1) AS pct_of_postings
FROM posting_skills ps
JOIN skills s ON s.skill_id = ps.skill_id
GROUP BY s.canonical_name
ORDER BY n_postings DESC, skill
LIMIT 15;

-- name: skill_frequency_pakistan (postings located in Pakistan only)
SELECT s.canonical_name AS skill, COUNT(*) AS n_postings
FROM posting_skills ps
JOIN skills s    ON s.skill_id = ps.skill_id
JOIN postings p  ON p.posting_pk = ps.posting_pk
JOIN locations l ON l.location_id = p.location_id
WHERE l.country = 'Pakistan'
GROUP BY s.canonical_name
ORDER BY n_postings DESC, skill
LIMIT 10;

-- name: salary_coverage (how much salary data do we really have?)
SELECT (SELECT COUNT(*) FROM postings) AS total_postings,
       (SELECT COUNT(DISTINCT posting_pk) FROM salary_observations) AS with_any_salary_info,
       (SELECT COUNT(*) FROM salary_observations WHERE salary_min IS NOT NULL) AS with_numeric_salary;

-- name: experience_breakdown (NULL means the source did not state it)
SELECT COALESCE(experience, 'not stated') AS experience, COUNT(*) AS n_postings
FROM postings
GROUP BY COALESCE(experience, 'not stated')
ORDER BY n_postings DESC;

-- name: work_mode_breakdown
SELECT work_mode, COUNT(*) AS n_postings
FROM postings
GROUP BY work_mode
ORDER BY n_postings DESC;

-- name: source_breakdown
SELECT source, COUNT(*) AS n_postings
FROM postings
GROUP BY source
ORDER BY n_postings DESC;

-- name: top_skill_pairs (skills that appear together in the same posting)
SELECT a.canonical_name AS skill_1, b.canonical_name AS skill_2, COUNT(*) AS together
FROM posting_skills x
JOIN posting_skills y ON x.posting_pk = y.posting_pk AND x.skill_id < y.skill_id
JOIN skills a ON a.skill_id = x.skill_id
JOIN skills b ON b.skill_id = y.skill_id
GROUP BY a.canonical_name, b.canonical_name
ORDER BY together DESC, skill_1, skill_2
LIMIT 10;
