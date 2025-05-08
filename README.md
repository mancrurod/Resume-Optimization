# 📄 Resume Optimization

**Resume Optimization** is an end-to-end, LLM-powered pipeline that transforms a `.docx` resume into a tailored, ATS-friendly PDF aligned with a specific job description. It leverages OpenAI or Gemini for semantic rewriting and includes a visual HTML editor for layout polishing.

---

## 🚀 What It Does

- 🧾 Converts `.docx` resumes into structured Markdown
- 🧠 Uses LLMs (GPT/Gemini) to adapt the content to any job ad
- 🧰 Applies intelligent style mapping and formatting
- 🖋️ Allows visual editing (PyQt5 WYSIWYG)
- 📄 Outputs a polished, print-ready PDF

---

## 📁 Project Structure

```
Resume-Optimization/
│
├── assets/fonts/                 # Custom font files (Garamond, Source Sans)
├── cv_template/                  # DOCX styling template (Word)
├── docs/                         # Markdown documentation
├── logs/                         # Runtime logs
├── original_docx/                # Input resumes (.docx)
├── processed_cv/                 # Intermediate files (.md, .html, .txt)
├── pdf_cv/                       # Final exported resumes (.pdf)
│
├── src/                          # Python source code
│   ├── convert_to_md.py          # DOCX → Markdown
│   ├── optimize_resume.py        # Build prompt
│   ├── adapt_resume.py           # Generate adapted Markdown
│   ├── export_resume.py          # HTML generation + visual editor + PDF export
│   └── __init__.py
│
├── main.py                       # 🔁 Orchestrates full ETL pipeline
├── requirements.txt              # Pip dependencies
├── environment.yml               # Conda environment (optional)
├── .env / .env.example           # API keys and configuration
├── README.md
├── CHECKLIST.md                  # Manual QA/testing checklist
└── CHANGELOG.md
```

---

## 🧠 How It Works

Just run:

```bash
python main.py
```

This will:

1. ✅ Extract and map styles from `original_docx/`
2. ✍️ Adapt the content using GPT or Gemini based on `job_description.txt`
3. 🧱 Rebuild the resume structure semantically
4. 🎨 Open an interactive WYSIWYG HTML editor for final tweaks
5. 📄 Export a clean, custom-styled PDF in `pdf_cv/`

> No need to run individual scripts manually — the full process is handled by `main.py`.

---

## 🛠 Requirements

- Python 3.10+
- [`wkhtmltopdf`](https://wkhtmltopdf.org/) installed and added to PATH
- Fonts:
  - Garamond Premier Pro
  - Source Sans 3 (Regular)

Install dependencies:

```bash
pip install -r requirements.txt
```

Or use Conda:

```bash
conda env create -f environment.yml
conda activate resume_optimization
```

---

## 🔐 Setup

1. Copy `.env.example` → `.env`
2. Add your keys:

```env
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
```

---

## 📌 Features

- Full resume pipeline: `.docx` → Markdown → Adaptation → HTML → PDF
- Job-specific rewriting using GPT or Gemini
- Visual HTML editor (PyQt5)
- Custom typographic styling (Garamond, Source Sans)
- Controlled spacing (`line-height`, bullets, paragraphs)
- PDF preview auto-open
- Structured logging and modular code

---

## 👨‍💻 Author

Created by **Manuel Cruz Rodríguez**  
Humanities graduate pivoting into Data Science & NLP.

🔗 [LinkedIn](https://www.linkedin.com/in/mancrurod/)  
📬 Feedback, issues and suggestions welcome.

---

## 📘 License

MIT License.  
Feel free to fork, adapt and improve — just don't ship Comic Sans. 😉