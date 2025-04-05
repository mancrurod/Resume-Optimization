# 📄 Resume Optimization

Welcome to **Resume Optimization** — a modular Python project that turns your `.docx` resume into a lean, clean, ATS-beating machine. With the help of LLMs, Markdown, and just enough automation to make it magic, your CV will finally look like it belongs in 2025.

---

## 🚀 What This Project Does

1. **Converts** your `.docx` resume into clean, structured `Markdown`.
2. **Builds a tailored prompt** based on your resume and a job description.
3. **Adapts** the content using GPT-4o-mini to match the job — this is the core of the optimization.
4. **Exports** the adapted Markdown to beautiful `HTML` and `PDF`.
5. **Lets you tweak** the final HTML visually with a built-in editor.
6. **Keeps things modular**, so you can swap models, templates, or scripts easily.

---

## 📁 Project Structure

```
Resume-Optimization/
│
├── cv_template/              # Optional resume templates (e.g. template.docx)
├── original_docx/            # Your original .docx resumes
├── pdf_cv/                   # Final exported PDFs
├── processed_cv/             # Markdown + HTML outputs (auto-generated)
│
├── src/                      # All core scripts live here
│   ├── convert_to_md.py      # DOCX → Markdown (structure preserved)
│   ├── optimize_resume.py    # Builds prompt for LLM based on job and CV
│   ├── adapt_cv.py           # GPT-powered adaptation using that prompt
│   ├── export_resume.py      # Markdown → HTML + PDF (+ WYSIWYG editor)
│   └── ...
│
├── .env                      # OpenAI API keys and credentials
├── job_description.txt       # Paste job ad text here to tailor your resume
├── main.py                   # Full pipeline from DOCX → PDF
├── requirements.txt
├── environment.yml
└── README.md
```

---

## 🤖 How It Works

### 1. Convert: DOCX → Markdown

```bash
python src/convert_to_md.py
```

Creates a Markdown version of your resume with proper headers, bullet points, and structure — even if your Word doc was chaotic.

### 2. Generate Prompt

```bash
python src/optimize_resume.py
```

Builds a tailored prompt based on your resume content and job description. Saves it to `processed_cv/prompt.txt`.

### 3. Adapt

```bash
python src/adapt_cv.py --job-description job_description.txt
```

Uses GPT-4o-mini (or Gemini as fallback) to align your resume with the job post. Adds keywords, improves bullet points, and enhances ATS compatibility.

### 4. Export & Edit

```bash
python src/export_resume.py
```

Converts the adapted Markdown into HTML and PDF. Edit the HTML visually in a PyQt5-based WYSIWYG editor.

### 🔁 Full Pipeline

To run everything in one go:

```bash
python main.py
```

---

## ✨ Features

- **ATS-friendly output**: Clean Markdown and semantic HTML.
- **Visual HTML editor**: Powered by PyQt5 and QWebEngineView.
- **Models to choose from**: Use OpenAI or Gemini.
- **Custom styling**: Built-in HTML themes with Garamond + Roboto.
- **Well-structured code**: SOLID principles, modularity, and clarity.

---

## 🛠 Requirements

- Python 3.10+
- [`wkhtmltopdf`](https://wkhtmltopdf.org/) (must be in your system PATH)
- Key Python packages:
  - `python-docx`, `markdown2`, `pdfkit`, `openai`, `PyQt5`

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

## 📌 Roadmap & Ideas

- [ ] Add support for multiple resumes and job descriptions in batch mode.
- [ ] Plug-and-play support for Claude/Gemini/LLama2.
- [ ] Deploy as a web app with Flask or Streamlit.
- [ ] Add CI tests for Markdown structure.

---

## 🤓 About the Author

Crafted by **Manuel Cruz Rodríguez**, Data Analyst and NLP explorer.  
Fueled by Markdown, espresso, and a mild obsession with resume formatting.

> "Because your skills deserve better than Word Art."

---

## 📬 Feedback & Contributions

Found a bug? Have an idea? Want your resume to sing?  
Open an issue, fork the repo, or just [connect on LinkedIn](https://www.linkedin.com/in/mancrurod/).

---

## 📘 License

MIT. Use it, fork it, remix it. Just don’t make a Comic Sans version. Please.