
import os
import sys
from dotenv import load_dotenv, find_dotenv
from src.convert_to_md import convert_docx_to_md
from src.optimize_resume import generate_prompt
from src.adapt_cv import adapt_resume
from src.export_resume import convert_md_to_html, convert_html_to_pdf, edit_html_content


def validate_api_keys():
    missing = []
    if not os.getenv("OPENAI_API_KEY"):
        missing.append("OPENAI_API_KEY")
    if not os.getenv("GOOGLE_API_KEY"):
        missing.append("GOOGLE_API_KEY")
    if missing:
        print(f"❌ Missing keys: {', '.join(missing)}. Add them to your .env file.")
        sys.exit(1)
    print("✅ API keys validated.")

def ensure_dirs(dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def get_latest_docx(folder):
    docs = [f for f in os.listdir(folder) if f.endswith(".docx")]
    if not docs:
        print(f"❌ No .docx found in '{folder}'")
        sys.exit(1)
    return sorted(docs, key=lambda f: os.path.getmtime(os.path.join(folder, f)))[-1]

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"❌ Error reading {path}: {e}")
        sys.exit(1)

def save_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"❌ Error saving {path}: {e}")
        sys.exit(1)

def main():
    if not find_dotenv():
        print("⚠️ .env not found")
    load_dotenv()
    validate_api_keys()

    in_dir = "original_docx"
    out_dir = "processed_cv"
    pdf_dir = "pdf_cv"
    job_path = "job_description.txt"
    ensure_dirs([in_dir, out_dir, pdf_dir])

    print("🔍 Step 1: DOCX to Markdown")
    docx = get_latest_docx(in_dir)
    docx_path = os.path.join(in_dir, docx)
    md_path = os.path.join(out_dir, os.path.splitext(docx)[0] + ".md")
    convert_docx_to_md(docx_path, md_path)

    print("🧠 Step 2: Generate prompt")
    md_content = read_file(md_path)
    job_description = read_file(job_path)
    prompt = generate_prompt(md_content, job_description)
    prompt_path = os.path.join(out_dir, "prompt.txt")
    save_file(prompt_path, prompt)

    print("🤖 Step 3: Adapt resume")
    adapted_md = os.path.join(out_dir, "adapted_resume.md")
    adapt_resume(prompt_path, adapted_md)

    print("🌐 Step 4: Markdown to HTML")
    html_path = os.path.join(out_dir, os.path.splitext(docx)[0] + ".html")
    convert_md_to_html(adapted_md, html_path)

    print("✍️ Step 5: Edit HTML (PyQt5)")
    edit_html_content(html_path)

    print("📄 Step 6: Export to PDF")
    pdf_path = os.path.join(pdf_dir, os.path.splitext(docx)[0] + ".pdf")
    convert_html_to_pdf(html_path, pdf_path)

    print("✅ DONE: Resume PDF saved at", pdf_path)

if __name__ == "__main__":
    main()
