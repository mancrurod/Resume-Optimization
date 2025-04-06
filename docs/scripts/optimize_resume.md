# 🧠 optimize_resume.py

Generates a detailed LLM prompt from your resume and job description.

- Validates the Markdown structure.
- Warns if key sections are missing.
- Output is a `.txt` file ready for LLM ingestion.

**Entry**: processed_cv/*.md and job_description.txt  
**Output**: processed_cv/prompt.txt