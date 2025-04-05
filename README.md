# 📄 Resume Optimization

Welcome to **Resume Optimization** — a modular Python project that turns your humble `.docx` resume into a lean, clean, ATS-beating machine. With the help of LLMs, Markdown, and just enough automation to make it magic, your CV will finally look like it belongs in 2025.

---

## 🚀 What This Project Does

1. **Converts** your `.docx` resume to structured `Markdown`.
2. **Adapts** the content using GPT-4o-mini to better match a job description (optionally).
3. **Exports** the adapted Markdown to `HTML` and `PDF`, with editable HTML styling.
4. **Lets you edit** the final HTML with a built-in visual editor (in PyQt5).
5. **Keeps things modular**, so you can swap in different models, templates or flows.

---

## 🧱 Project Structure

```
Resume-Optimization/
│
├── original_docx/            # Your original .docx resumes
├── pdf_cv/                   # Final PDF output
├── processed_cv/             # Cleaned Markdown/HTML output
│
├── src/                      # All scripts live here
│   ├── convert_to_md.py      # DOCX → clean Markdown
│   ├── export_resume.py      # Markdown → HTML + PDF (with HTML editor!)
│   ├── adapt_cv.py           # Uses GPT-4o-mini to tailor your resume
│   └── ...                   # Other modular tools and helpers
│
├── .env                      # OpenAI keys or API credentials
├── .gitignore
├── environment.yml           # Conda environment file
├── job_description.txt       # Paste a JD here to adapt your resume to it
├── main.py                   # Orchestrates the pipeline
├── README.md
└── requirements.txt
```

---

## 🤖 How It Works

### 1. Convert
Turn `.docx` into Markdown with proper headings, bullet points, and structure — even if your original Word doc was a mess.  
*Spoiler: It probably was.*

```bash
python src/convert_to_md.py
```

### 2. Adapt (Optional)
Feed the Markdown into GPT-4o-mini and let the AI highlight what recruiters want to see. Buzzwords included, guilt-free.

```bash
python src/adapt_cv.py --job-description job_description.txt
```

### 3. Export & Edit
Generate beautiful HTML + PDF files with typographic control. Then tweak the HTML visually with a full WYSIWYG editor.

```bash
python src/export_resume.py
```

---

## ✨ Features

- **ATS-friendly output**: Clean, semantic HTML and Markdown.
- **Visual HTML editor**: Built with PyQt5 and QWebEngineView.
- **Model-agnostic**: Swap GPT with any other LLM or skip it altogether.
- **Custom styling**: Typography based on EB Garamond + Roboto.
- **Nerd-approved**: Follows SOLID principles and clean code practices.

---

## 🛠 Requirements

- Python 3.10+
- `docx`, `markdown2`, `pdfkit`, `PyQt5`, `openai` (if you adapt with GPT)
- `wkhtmltopdf` installed and in your PATH for PDF export

Install dependencies:

```bash
pip install -r requirements.txt
```

Or, using Conda:

```bash
conda env create -f environment.yml
conda activate resume_optimization
```

---

## 🤓 Who Made This?

Crafted by **Manuel Cruz Rodríguez**, Data Analyst and NLP explorer.  
Fueled by Markdown, espresso, and a mild obsession with resume formatting.

> "Because your skills deserve better than Word Art."

---

## 📬 Contributing / Feedback

Spotted a bug? Have a feature request? Want your resume to sing?  
Open an issue or pull request — or just [connect with me](https://linkedin.com/in/mcruzrodriguez).

---

## 📘 License

MIT. Use it, fork it, remix it. Just don’t make a Comic Sans version. Please.