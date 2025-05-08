# 🚀 Usage Instructions

## 1. Add your input resume

Place your `.docx` file into the `original_docx/` folder.

---

## 2. Add the job description

Paste your job description into a file named:

```
job_description.txt
```

---

## 3. Run the pipeline

Use:

```bash
python main.py
```

This will:

- Validate your `.docx`
- Build a prompt for the LLM
- Rewrite the resume to match the job
- Convert the result to HTML
- Let you visually edit the layout and spacing
- Export the final PDF to `pdf_cv/`

---

## 🖋️ Fonts

Make sure `GaramondPremrPro.otf`, `GaramondPremrPro-Bd.otf`, and `SourceSans3-Regular.ttf` are in:

```
assets/fonts/
```

---

## 🔍 Output

- Final Markdown: `processed_cv/adapted_resume.md`
- Visual HTML: `processed_cv/<filename>.html`
- Final PDF: `pdf_cv/<filename>.pdf`

---

> You do **not** need to run individual scripts. The full pipeline is handled by `main.py`.