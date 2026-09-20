# Mini Project: Resume ↔ Job Description Matcher

Ties together everything from lectures 1–4: LLM calls, system role, structured JSON output via Pydantic, and reading real files.

## What it does
Given a job description and a folder of resumes (PDF or DOCX), it:
1. Parses the job description into a structured `JobD` schema (role, required/preferred skills, min experience, education requirements, responsibilities).
2. Reads each resume file (PDF via `pypdf`, DOCX via `python-docx`) and extracts its raw text.
3. Parses each resume's raw text into a structured `Resume` schema (name, email, phone, total experience, skills, past experiences, education, projects, certifications) — matching by *meaning*, not exact section headings, since resumes vary a lot.
4. Compares the parsed job description against each parsed resume via another LLM call, returning a `MatchResult` (score + details: matching skills, missing skills, whether experience requirement is met, overall match %, final verdict).
5. Ranks all candidates by score and prints the top 2 and bottom 2.

## Structure
- `JobD`, `Resume`, `Experience`, `MatchResult` — Pydantic schemas defining the exact shape of each stage's output.
- `read_pdf` / `read_docx` / `read_resume` — file readers that turn a resume file into plain text regardless of format.
- `parse_resume(resume_text)` — sends resume text to the LLM with the `Resume` schema and gets back a validated `Resume` object.
- `final_score(job, resume)` — sends both structured objects to the LLM and gets back a validated `MatchResult`.
- Main loop — iterates over a `resumes/` folder, parses + scores every resume, then sorts and prints the top and bottom candidates.

## Code
`resume_parser.py` — full end-to-end pipeline as described above.

## Note
Expects a local `resumes/` folder (not included) containing the resume files to process, and relies on a `.env` file with `GROQ_API_KEY` set (also not included — never commit API keys).
