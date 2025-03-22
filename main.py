import os
import sys
from dotenv import load_dotenv, find_dotenv
from src.convert_to_md import convert_docx_to_md
from src.optimize_resume import generate_prompt
from src.adapt_cv import adapt_resume
from src.export_resume import convert_md_to_html, convert_html_to_pdf, edit_html_content


def validate_api_keys():
    """Validate that necessary API keys are present."""
    missing_keys = []

    if not os.getenv("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    if not os.getenv("GOOGLE_API_KEY"):
        missing_keys.append("GOOGLE_API_KEY")

    if missing_keys:
        print(f"❌ Error: Missing required API keys: {', '.join(missing_keys)}")
        print("⚠️ Please add these keys to your .env file.")
        sys.exit(1)

    print("✅ API keys validated successfully.")


def ensure_directories_exist(directories):
    """Ensure that the required directories exist."""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("📂 Necessary directories checked/created.")


def get_latest_docx_file(folder):
    """Retrieve the latest .docx file from the specified folder."""
    docx_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".docx")]

    if not docx_files:
        print(f"❌ Error: No .docx resume files found in the '{folder}' folder. Please add your resume and try again.")
        sys.exit(1)

    latest_file = max(docx_files, key=os.path.getmtime)  # Get the most recently modified file
    return os.path.basename(latest_file)


def read_file(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                print(f"⚠️ Warning: {file_path} is empty.")
            return content
    except FileNotFoundError:
        print(f"❌ Error: {file_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        sys.exit(1)


def save_file(file_path, content):
    """Save content to a file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        print(f"❌ Error writing to {file_path}: {e}")
        sys.exit(1)


def main():
    # Load .env file safely
    if not find_dotenv():
        print("⚠️ Warning: .env file not found. Ensure your API keys are set.")
    load_dotenv()
    
    validate_api_keys()

    input_folder = "original_docx"
    processed_folder = "processed_cv"
    pdf_folder = "pdf_cv"
    job_desc_path = "job_description.txt"

    ensure_directories_exist([input_folder, processed_folder, pdf_folder])

    print("🔍 Step 1: Searching for .docx resumes...")
    latest_docx = get_latest_docx_file(input_folder)
    docx_path = os.path.join(input_folder, latest_docx)
    md_resume_path = os.path.join(processed_folder, os.path.splitext(latest_docx)[0] + ".md")

    print(f"📝 Converting '{latest_docx}' to Markdown format...")
    try:
        convert_docx_to_md(docx_path, md_resume_path)
        print(f"✅ Markdown resume saved at: {md_resume_path}")
    except Exception as e:
        print(f"❌ Error converting {latest_docx}: {e}")
        sys.exit(1)

    print("📖 Step 2: Reading the resume and job description...")
    md_resume = read_file(md_resume_path)
    job_description = read_file(job_desc_path)

    print("💡 Step 3: Generating optimization prompt...")
    try:
        prompt = generate_prompt(md_resume, job_description)
        prompt_path = os.path.join(processed_folder, "prompt.txt")
        save_file(prompt_path, prompt)
        print(f"✅ Prompt saved at {prompt_path}")
    except Exception as e:
        print(f"❌ Error generating optimization prompt: {e}")
        sys.exit(1)

    print("🤖 Step 4: Adapting resume using AI APIs...")
    adapted_md_path = os.path.join(processed_folder, "adapted_resume.md")
    try:
        adapt_resume(prompt_path, adapted_md_path)
        print(f"✅ Adapted resume saved at {adapted_md_path}")
    except Exception as e:
        print(f"❌ Error adapting resume: {e}")
        sys.exit(1)

    print("🌐 Step 5: Converting Markdown resume to HTML...")
    your_name_CV = os.path.splitext(latest_docx)[0]
    html_resume_path = os.path.join(processed_folder, f"{your_name_CV}.html")
    try:
        convert_md_to_html(adapted_md_path, html_resume_path)
        print(f"✅ HTML resume saved at {html_resume_path}")
    except Exception as e:
        print(f"❌ Error converting Markdown to HTML: {e}")
        sys.exit(1)

    print("✏️ Step 6: Editing the HTML content...")
    try:
        edit_html_content(html_resume_path)
    except Exception as e:
        print(f"⚠️ Warning: Error editing HTML content: {e}")

    print("📄 Step 7: Converting edited HTML resume to PDF...")
    pdf_resume_path = os.path.join(pdf_folder, f"{your_name_CV}.pdf")
    try:
        convert_html_to_pdf(html_resume_path, pdf_resume_path)
        print(f"✅ PDF resume saved at {pdf_resume_path}")
    except Exception as e:
        print(f"❌ Error converting HTML to PDF: {e}")
        sys.exit(1)

    print("🎉 Resume optimization process completed successfully!")


if __name__ == "__main__":
    main()
