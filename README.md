# 📄 Resume Optimization

Welcome to **Resume Optimization** — a modular, extensible pipeline that transforms your `.docx` resume into a customized, ATS-friendly PDF, fine-tuned for a specific job offer using LLMs like GPT-4o-mini or Gemini.

---

## 🚀 What This Project Does

1. **Converts** your `.docx` resume into clean, structured `Markdown`.
2. **Builds a dynamic LLM prompt** based on your resume and a job description.
3. **Adapts** the content using GPT or Gemini to match job requirements.
4. **Exports** the adapted Markdown to beautiful `HTML` and `PDF`.
5. **Opens a visual editor** so you can tweak the final HTML by hand.
6. **Logs everything** and validates your files to avoid surprises.
7. **Previews the final PDF** automatically.

---

## 📁 Project Structure

```
Resume-Optimization/
│
├── original_docx/            # Original .docx resumes (input)
├── processed_cv/             # Intermediate Markdown, HTML, prompt
├── pdf_cv/                   # Final exported PDFs
├── cv_template/              # Optional base resume templates
├── logs/                     # Pipeline logs (.log) per execution
│
├── src/                      # Modular source code
│   ├── convert_to_md.py
│   ├── optimize_resume.py
│   ├── adapt_resume.py
│   ├── export_resume.py
│   └── __init__.py
│
├── .env                      # 🔒 DO NOT COMMIT — contains API keys
├── .env.example              # ✅ Safe template to share
├── job_description.txt       # Paste job ad text here
├── main.py                   # Full pipeline: DOCX → Markdown → GPT → PDF
├── requirements.txt
├── environment.yml
└── README.md
```

---

## 🤖 Pipeline Overview

### 1. Convert DOCX → Markdown

```bash
python src/convert_to_md.py
```

Creates a structured Markdown version of your resume with headers, lists, formatting, and hyperlinks.

### 2. Generate LLM Prompt

```bash
python src/optimize_resume.py
```

Generates a detailed, language-aware prompt using your resume and a job description.

### 3. Adapt Resume with LLM

```bash
python src/adapt_resume.py
```

Uses OpenAI's GPT-4o-mini or Gemini as fallback to tailor your resume to the job description.

### 4. Export to HTML + Edit

```bash
python src/export_resume.py
```

Converts the adapted Markdown to HTML and opens a WYSIWYG editor to polish the formatting.

### 5. Generate PDF

Done automatically when you run the pipeline — and the PDF opens instantly when done ✅

### 🔁 Full Pipeline (Recommended)

```bash
python main.py
```

This script orchestrates the entire process, including file validation, logging, LLM calls, editing, exporting, and preview.

---

## ✨ Features

- ✅ **End-to-end pipeline** from `.docx` to `PDF`.
- ✍️ **Visual HTML editor** (PyQt5-based).
- 🧠 **Smart prompt generation** with multilingual LLM support.
- 📂 **Logging per execution** (`logs/resume_YYYYMMDD_HHMMSS.log`).
- 🔍 **Validation** of `.docx` inputs before processing.
- 🧾 **`.env.example`** for easy setup.
- 🖼️ **Auto-preview** of the final PDF on completion.
- 🧱 **Modular code**, fully SOLID and documented.

---

## 🛠 Requirements

- Python 3.10+
- [`wkhtmltopdf`](https://wkhtmltopdf.org/) (must be in your system PATH)
- Key packages:
  - `python-docx`, `markdown2`, `pdfkit`, `openai`, `PyQt5`, `google-generativeai`

Install with pip:

```bash
pip install -r requirements.txt
```

Or with Conda:

```bash
conda env create -f environment.yml
conda activate resume_optimization
```

---

## 🔐 Setup

1. Copy `.env.example` → `.env`
2. Add your API keys:

```dotenv
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_gemini_key_here
```

---

## 📌 Roadmap

- [x] Add logging system and `.log` files
- [x] Validate `.docx` input structure
- [x] Previsualize exported PDF automatically
- [x] Add `.env.example` for safer sharing
- [ ] Add versioned filenames with timestamps
- [ ] Batch mode: multiple resumes / jobs
- [ ] Streamlit web version (GUI)
- [ ] Add Claude or LLama2 support

---

## 👨‍💻 Author

Crafted with care by **Manuel Cruz Rodríguez**,  
Graduate in Hispanic Philology, NLP specialist, and AI enthusiast.

> “Because your skills deserve better than a Word template.”

🔗 [LinkedIn](https://www.linkedin.com/in/mancrurod/)  
📫 Feel free to fork, star, or open issues for feedback!

---

## 📘 License

MIT — free to use, modify, and share.  
Please don’t generate Comic Sans PDFs. 🥲