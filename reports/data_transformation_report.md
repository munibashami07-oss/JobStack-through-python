# 📊 JobStack: Data Transformation & Skill Intelligence Report (Person 2)

**Author:** Person 2 (Data Transformation and Skill Intelligence)  
**Dataset Input:** `data/validated/sample_300.json` (or `data/validated/jobs_valid.json`)  
**Dataset Output:** `data/transformed/jobs_final.csv` & `data/transformed/jobs_final.json`  

---

## 1. Executive Summary

As **Person 2** in the JobStack project, my responsibility is to transform validated job-posting data into clean, structured, and intelligence-ready datasets for downstream database storage (SQL), exploratory data analysis (EDA), and machine learning baselines.

The entire transformation pipeline consists of four straightforward, transparent steps:
1. **Basic Data Cleaning & Standardization**: Strips HTML, cleans whitespace, standardizes messy titles, cities, employment types, and work modes, while preserving raw columns.
2. **Simple Skill Extraction**: Uses a transparent canonical dictionary and boundary-checked string matching to extract technical and soft skills into `extracted_skills`.
3. **Duplicate Detection & Removal**: Detects reposts and duplicates across title, company, and location using Pandas' native `duplicated()` and `drop_duplicates(keep='first')`.
4. **Final Export & Schema Validation**: Verifies column completeness and exports production-ready files (`jobs_final.csv` and `jobs_final.json`).

---

## 2. What Cleaning Was Performed (Step 1)

* **HTML Entity Decoding & Tag Removal**: 
  - Web scraped job postings from Arbeitnow and Remotive contain HTML tags (such as `<p>`, `<br>`, `<strong>`, `<a href="...">`) and encoded entities (such as `&amp;` for `&`, `&nbsp;` for space).
  - We decoded HTML entities using `html.unescape()` and removed markup tags using regular expressions (`<[^>]+>`).
* **Whitespace Normalization**: 
  - Replaced consecutive spaces, tabs, and newlines (`\s+`) with a single clean space.
* **Dictionary-Based Standardization**:
  - `standardized_title`: Mapped common variations (e.g., `software developer` $\rightarrow$ `Software Engineer`, `sr. software engineer` $\rightarrow$ `Senior Software Engineer`) and stripped German gender markers (`(m/w/d)`).
  - `standardized_city`: Unified location strings (e.g., `Lahore, Pakistan` $\rightarrow$ `Lahore`, `Berlin, Germany` $\rightarrow$ `Berlin`).
  - `standardized_employment_type`: Normalized verbose types (`full_time`, `unbefristeter arbeitsvertrag`) into standard categories (`Full-time`, `Part-time`, `Contract`, `Internship`, `Temporary`).
  - `standardized_work_mode`: Mapped variants like `100 % remote` and `wfh` to `remote`, `in-office` to `onsite`, and unstated modes to `unknown`.
* **Missing Value Integrity**:
  - Whitespace-only strings and literal `"nan"` strings were converted to true `None` (representing `null`).
  - **No invented data**: Per the team data contract, missing salaries remain `null` and are **never** filled with 0 or synthetic averages.

---

## 3. How Skills Were Extracted (Step 2)

* **Canonical Skill Dictionary**:
  - A structured dictionary (`SKILL_DICTIONARY`) maps canonical skill names to lists of search keywords/aliases.
  - Covers requested core skills: `Python`, `SQL`, `Java`, `JavaScript`, `React`, `Excel`, `Pandas`, `Communication`, and `Teamwork`, plus common tools (`Docker`, `AWS`, `Git`, `TypeScript`, `C++`, `C#`, `PHP`).
* **Word Boundary String Matching**:
  - To prevent false positive matches (such as `"Java"` matching inside `"JavaScript"`), regex word boundaries `(?<!\w)` and `(?!\w)` were used.
  - Matching is strictly case-insensitive.
* **Empty Handling**:
  - If a job description contains no recognized skills, an empty list `[]` is assigned. No fake or hallucinated skills are ever generated.

---

## 4. How Duplicates Were Identified (Step 3)

* **Deduplication Criteria**:
  - A job posting is considered a duplicate when its **job title**, **company name**, and **location** are identical.
  - Standardized columns (`standardized_title`, `company_name`, `standardized_city`) are used to prevent superficial variations from bypassing deduplication.
* **Pandas Implementation**:
  - Identification: `df.duplicated(subset=..., keep='first')` flags all occurrences after the first as duplicates.
  - Removal: `df.drop_duplicates(subset=..., keep='first')` retains the original posting and safely drops subsequent reposts.
* **Missing Values in Deduplication**:
  - We do not fill missing company or city values with arbitrary strings like `"Unknown"`, which prevents unrelated anonymous postings from colliding into false duplicates.

---

## 5. Data Dictionary (Output Columns in `jobs_final.csv`)

| Column Name | Type | Description |
|---|---|---|
| `posting_id` | string | Unique source identifier for the posting |
| `source` | string | Data source (`kaggle_pk`, `arbeitnow`, `remotive`) |
| `source_url` | string / null | Web link to original ad (null for Kaggle) |
| `title` | string | Original unedited job title |
| `standardized_title` | string | Normalized canonical job title (e.g., "Software Engineer") |
| `description` | string | Original job description (may contain HTML) |
| `cleaned_description`| string | Plain text description with HTML tags and excess spaces removed |
| `company_name` | string / null | Hiring company or organization |
| `category` | string / null | Job sector or industry category |
| `tags` | list | List of job tags from source |
| `city` | string / null | Original unedited city |
| `standardized_city` | string / null | Normalized city name (e.g., "Lahore", "Karachi") |
| `country` | string / null | Country name (e.g., "Pakistan") |
| `work_mode` | string | Original work mode value |
| `standardized_work_mode`| string | Canonical work mode (`remote`, `onsite`, `hybrid`, `unknown`) |
| `employment_type` | string / null | Original employment type string |
| `standardized_employment_type`| string / null | Canonical employment type (`Full-time`, `Part-time`, etc.) |
| `experience` | string / null | Required years of experience |
| `salary_min`, `salary_max` | float / null | Numeric salary limits (null if absent) |
| `currency` | string / null | Currency code (e.g., PKR, USD) |
| `salary_text` | string / null | Free-text salary notes if provided |
| `posted_at` | string / null | Date and timestamp of posting |
| `language` | string / null | Detected language (`en`, `de`) |
| `extracted_skills` | list of str | List of detected skills from `SKILL_DICTIONARY` (e.g., `['Python', 'SQL']`) |

---

## 6. Limitations of the Simple Skill-Matching Approach

While dictionary-based keyword matching is transparent, explainable, and fast, it has known trade-offs:
1. **Implicit Skills**: If an employer writes *"built RESTful microservices and schemas"* without saying the words *"API"* or *"SQL"*, string matching will not detect them.
2. **Vocabulary Limits**: Unlisted synonyms or emerging tools not present in `SKILL_DICTIONARY` are skipped.
3. **Absence of Negative Context**: If an ad states *"No Python experience required"*, basic string matching still detects *"Python"*.
4. **Polysemy (Word Ambiguity)**: Words like *"Go"* or *"R"* require careful handling because they are common English words as well as programming language names.

---

## 7. Concrete Before-and-After Examples

### Example 1: HTML & Description Cleaning (Step 1)
* **Raw Description**:
  ```html
  <p dir="ltr">We are looking for a <strong>Senior Developer</strong> &amp; architect.<br>Apply now!  </p>
  ```
* **Cleaned Description**:
  ```text
  We are looking for a Senior Developer & architect. Apply now!
  ```

### Example 2: Standardization of Attributes (Step 1)
* **Before**:
  - `title`: `"Senior .NET Full-stack Developer"`
  - `city`: `"Lahore, Pakistan"`
  - `employment_type`: `"unbefristeter arbeitsvertrag"`
  - `work_mode`: `"100 % remote"`
* **After**:
  - `standardized_title`: `"Full Stack Developer"`
  - `standardized_city`: `"Lahore"`
  - `standardized_employment_type`: `"Full-time"`
  - `standardized_work_mode`: `"remote"`

### Example 3: Skill Extraction & Boundary Matching (Step 2)
* **Description Snippet**:
  ```text
  "Candidates must have deep experience in JavaScript, React, and SQL. Teamwork and strong communication skills are required."
  ```
* **Extracted Skills**:
  ```python
  ["Communication", "JavaScript", "React", "SQL", "Teamwork"]
  ```
  *(Notice: `JavaScript` was matched, but `Java` was correctly ignored thanks to regex word boundaries).*

### Example 4: Duplicate Detection (Step 3)
* **Input Postings**:
  - Posting A: Title: `Software Engineer`, Company: `Eurosoft`, City: `Karachi`, Posted: `2026-01-01`
  - Posting B: Title: `Software Engineer`, Company: `Eurosoft`, City: `Karachi`, Posted: `2026-01-08` *(Repost)*
* **Deduplication Result**:
  - Duplicate detected: Posting B
  - Retained: Posting A (`keep='first'`)

---

## 8. Pipeline Row Count & Verification Metrics

* **Input Rows**: 300
* **Duplicates Detected & Removed**: 0 (all 300 rows in development sample were unique)
* **Final Retained Rows**: 300
* **Required Column Verification**: 100% pass (all 15 required columns present)
* **Postings with Extracted Skills**: 114 (38.0%)
* **Postings without Skills**: 186 (62.0%) (stored as clean `[]`, no fabricated data)

---

## 9. Commands to Run Pipeline and Tests

```bash
# 1. Run all transformation steps end-to-end:
python -m src.transformation.clean_data
python -m src.transformation.extract_skills
python -m src.transformation.detect_duplicates
python -m src.transformation.export_final

# 2. Run the complete unit test suite (73 tests):
python -m pytest
```
