-- JobStack Project 1 | Person 3 | 05_qa_checks.sql
-- Manual QA you can run in any SQLite tool. Every "problem" query should return 0.

-- Row counts per table
SELECT 'companies' AS tbl, COUNT(*) AS n FROM companies
UNION ALL SELECT 'locations', COUNT(*) FROM locations
UNION ALL SELECT 'skills', COUNT(*) FROM skills
UNION ALL SELECT 'postings', COUNT(*) FROM postings
UNION ALL SELECT 'posting_skills', COUNT(*) FROM posting_skills
UNION ALL SELECT 'salary_observations', COUNT(*) FROM salary_observations;

-- Orphans: posting_skills rows pointing to a missing posting or skill (must be 0)
SELECT COUNT(*) AS orphan_posting_links
FROM posting_skills ps LEFT JOIN postings p ON p.posting_pk = ps.posting_pk
WHERE p.posting_pk IS NULL;

SELECT COUNT(*) AS orphan_skill_links
FROM posting_skills ps LEFT JOIN skills s ON s.skill_id = ps.skill_id
WHERE s.skill_id IS NULL;

-- Postings pointing to a missing company/location (must be 0)
SELECT COUNT(*) AS bad_company_refs
FROM postings p LEFT JOIN companies c ON c.company_id = p.company_id
WHERE p.company_id IS NOT NULL AND c.company_id IS NULL;

SELECT COUNT(*) AS bad_location_refs
FROM postings p LEFT JOIN locations l ON l.location_id = p.location_id
WHERE p.location_id IS NOT NULL AND l.location_id IS NULL;

-- Salary must never be silently zero (must be 0)
SELECT COUNT(*) AS zero_salaries FROM salary_observations WHERE salary_min = 0 OR salary_max = 0;

-- Information only: postings with no extracted skills
SELECT COUNT(*) AS postings_without_skills
FROM postings p
WHERE NOT EXISTS (SELECT 1 FROM posting_skills ps WHERE ps.posting_pk = p.posting_pk);
