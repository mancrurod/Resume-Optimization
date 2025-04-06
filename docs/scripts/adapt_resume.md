# 🤖 adapt_resume.py

Sends the generated prompt to GPT-4o-mini or Gemini to adapt your resume.

- If OpenAI rate limits, Gemini is used as fallback.
- Cleans code blocks and saves final Markdown output.

**Entry**: processed_cv/prompt.txt  
**Output**: processed_cv/adapted_resume.md