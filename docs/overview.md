# 🧠 Project Overview

**Resume Optimization** is a semantic, layout-aware ETL pipeline that transforms `.docx` resumes into ATS-friendly, customized PDFs using GPT or Gemini.

---

## 🔁 How It Works

The pipeline is run entirely through:

```bash
python main.py
```

This executes:

1. 📄 Converts `.docx` to Markdown with structural style mapping
2. 🧠 Builds an LLM prompt using the resume and a job description
3. 🤖 Adapts the resume using OpenAI or Gemini
4. 🌐 Converts adapted Markdown into HTML
5. ✍️ Opens a visual HTML editor (PyQt5) to fine-tune layout and spacing
6. 📄 Exports the resume to PDF with professional typography and spacing

---

## ✨ Key Features

- ✅ One-command full pipeline (`main.py`)
- 🎨 Uses Garamond + Source Sans with precise PDF rendering
- 🧠 Prompt-based rewriting for job targeting
- ✍️ PyQt5 WYSIWYG HTML editor
- 🔍 Markdown cleanup + style normalization
- 📄 PDF generated with `wkhtmltopdf` for full typographic control