# 📄 Resume Optimization Project

## 🚀 Overview

Automate your resume optimization process with AI! This project transforms `.docx` resumes into Markdown, customizes them based on job descriptions, and exports the final versions in **HTML** and **PDF** formats.

---

## 📂 Project Structure

```
Resume-Optimization/
├── original_docx/           # Store original .docx resumes
├── processed_cv/            # Store Markdown and intermediate resumes
├── pdf_cv/                  # Store final PDFs
├── src/                     # Source code
│   ├── convert_to_md.py     # Step 1: Convert .docx to Markdown
│   ├── optimize_resume.py   # Step 2: Generate AI optimization prompt
│   ├── adapt_cv.py          # Step 3: Adapt resume using AI APIs
│   ├── export_resume.py     # Step 4: Convert Markdown to HTML & PDF
├── job_description.txt      # Store the target job description
├── requirements.txt         # List of dependencies
├── .env                     # Environment variables (API keys)
├── .gitignore               # Ignore unnecessary files
└── README.md                # Project documentation
```

---

## ✨ Features

✔ **Convert Resumes**: Preserve formatting when converting `.docx` to Markdown.  
✔ **Smart Prompting**: AI-generated prompts tailored to job descriptions.  
✔ **AI-Powered Customization**: Rewrite resumes using OpenAI and Google APIs.  
✔ **Multi-Format Export**: Save the adapted resume as **Markdown, HTML, and PDF**.

---

## ⚙️ Prerequisites

Ensure you have the following installed:

- **Python**: Version 3.8+
- **`wkhtmltopdf`**: Required for PDF generation ([installation guide](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf))
- **API Keys**:
  - OpenAI (`OPENAI_API_KEY`)
  - Google (`GOOGLE_API_KEY`)

---

## 📥 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/resume-optimization.git
    cd resume-optimization
    ```
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Install `wkhtmltopdf`**:  
    Follow the [installation guide](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf).
4. **Set up environment variables**:
    - Create a `.env` file and add:
      ```env
      OPENAI_API_KEY=your_openai_api_key
      GOOGLE_API_KEY=your_google_api_key
      ```

---

## 📖 Usage

1. Place your `.docx` resume in the `original_docx/` folder.
2. Copy the target job description into `job_description.txt`.
3. Ensure your API keys are set.
4. Run the script:
    ```bash
    python main.py
    ```
5. Your optimized resume will be saved as:
    - **Markdown** → `processed_cv/adapted_resume.md`
    - **HTML** → `processed_cv/Your Name CV.html`
    - **PDF** → `pdf_cv/Your Name CV.pdf`

---

## 🔄 Workflow

1. **Convert to Markdown** → Transforms `.docx` into Markdown format.
2. **Generate AI Prompt** → Creates a job-specific optimization prompt.
3. **AI Resume Adaptation** → Uses AI to refine and rewrite your resume.
4. **Manual Editing (Optional)** → Adjust HTML for final touches before export.
5. **Export Resume** → Saves in **HTML & PDF** formats.

---

## 🛠️ Troubleshooting

🔹 **`wkhtmltopdf` not found** → Ensure it’s installed correctly ([guide](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf)).  
🔹 **Missing API keys** → Verify `.env` contains `OPENAI_API_KEY` and `GOOGLE_API_KEY`.  
🔹 **No `.docx` file found** → Place a resume in `original_docx/`.  
🔹 **Job description missing** → Ensure `job_description.txt` is populated.  
🔹 **Formatting Issues?** → Before processing, ensure your `.docx`:
   - Uses **justified** paragraphs for readability.
   - Contains **bullet points** for structure.
   - Applies **bold/italic** styles for emphasis.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/new-feature
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add new feature"
    ```
4. Push to the branch:
    ```bash
    git push origin feature/new-feature
    ```
5. Open a pull request.

---

## 📜 License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

🚀 **Get started today and optimize your resume like a pro!**

Now you can copy and paste this directly into your `README.md` file. Let me know if you need any further tweaks! 🚀