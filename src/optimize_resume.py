import os
import re

def generate_prompt(md_resume: str, job_description: str) -> str:
    """
    Generate a detailed prompt to optimize a resume according to a job description.
    
    Parameters:
        md_resume (str): The resume content in Markdown format.
        job_description (str): The job description text.
    
    Returns:
        str: The complete prompt to send to a language model.
    """
    return f"""
I have a resume in Markdown format and a job description. Your task is to **refine and tailor my resume** to closely match the job requirements while ensuring it remains professional, well-structured, and ATS-friendly. Below are the details. You MUST follow the instructions carefully.

### **Key Objectives:**  
- Align my resume with the job description by emphasizing **relevant skills, experiences, and achievements**.  
- **Incorporate** keywords and phrases from the job posting to improve ATS compatibility.  
- **Enhance bullet points** by making them **quantifiable** and **impact-driven**.  
- Ensure **clarity, conciseness, and a professional tone**.  
- Maintain the **Markdown format**, preserving proper spacing, bullet points, and hyperlinks.  
- **Keep job and education dates** on the **same line**, right after the job title or degree, using a clear separator like `·`.  
- Format each **job title** AND **degree** as: **Title**, *Institution* · Dates, keeping everything on the same line.  
- If my **education or experience does not fully match** the job description, identify and emphasize **transferable skills** that demonstrate my ability to perform the role effectively.

### **Language Guidelines:**  
- If **both** the resume and job description are in **Spanish**, return the revised resume in **Spanish**.  
- If **both** are in **English**, return the revised resume in **English**.  

### **Input Data:**  
#### **Resume (Markdown format):**  
{md_resume}  

#### **Job Description:**  
{job_description}  

### **Expected Output:**  
- Return the **optimized resume in Markdown**, ensuring it is refined according to the outlined objectives.  
- **Do not enclose the output in code blocks (` ``` `), return it as plain Markdown content.**
- Example for **Title**, *Institution* · Dates: **Máster en Data Science & IA**, *Evolve Academy* · Enero 2025 - Junio 2025
"""


def get_latest_docx_file(input_folder: str) -> str:
    """
    Retrieve the most recently modified .docx file from a folder.
    
    Parameters:
        input_folder (str): Path to the folder containing .docx files.
    
    Returns:
        str: Filename of the latest .docx file.
    
    Raises:
        FileNotFoundError: If no .docx files are found in the folder.
    """
    docx_files = [f for f in os.listdir(input_folder) if f.endswith(".docx")]
    if not docx_files:
        raise FileNotFoundError(f"No .docx file found in folder: {input_folder}")
    return sorted(docx_files, key=lambda f: os.path.getmtime(os.path.join(input_folder, f)))[-1]


def read_file(file_path: str) -> str:
    """
    Read the content of a text file with UTF-8 encoding.
    
    Parameters:
        file_path (str): Full path to the text file.
    
    Returns:
        str: File content.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def clean_markdown_for_prompt(md_text: str) -> str:
    """
    Remove surrounding code block markers (```), if present.
    
    Parameters:
        md_text (str): Markdown content that may include code fences.
    
    Returns:
        str: Cleaned Markdown content.
    """
    lines = md_text.strip().splitlines()
    if lines and lines[0].startswith("```") and lines[-1].startswith("```"):
        lines = lines[1:-1]
    return "\n".join(lines).strip()


def validate_markdown(md_text: str) -> list:
    """
    Validate Markdown structure and syntax for common formatting issues.
    
    Parameters:
        md_text (str): Markdown content to validate.
    
    Returns:
        list: List of warnings or issues detected (empty if valid).
    """
    issues = []
    lines = md_text.splitlines()

    for i, line in enumerate(lines, 1):
        if re.match(r"^#{1,6}[^\s#]", line):
            issues.append(f"Line {i}: Missing space after header marker → `{line}`")

    if md_text.count("**") % 2 != 0:
        issues.append("Unmatched `**` for bold formatting.")
    if md_text.count("*") % 2 != 0:
        issues.append("Unmatched `*` for italic formatting.")

    malformed_links = re.findall(r"\[[^\]]*\]\([^\)]*$", md_text)
    if malformed_links:
        issues.append("Detected malformed Markdown link(s).")

    required_sections = ["## Experiencia", "## Educación"]
    for section in required_sections:
        if section not in md_text:
            issues.append(f"Missing required section: `{section}`")

    return issues


def log_validation_issues(issues: list, cv_filename: str):
    """
    Save validation issues to a log file inside the logs/ directory.
    
    Parameters:
        issues (list): List of issues to log.
        cv_filename (str): Name of the markdown file (used for naming the log).
    """
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(cv_filename))[0]
    log_filename = f"logs/validation_{base_name}_{timestamp}.log"

    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(f"📄 Validation Log for {cv_filename}\n")
        log_file.write(f"🕒 Timestamp: {timestamp}\n")
        log_file.write("⚠️ Issues Detected:\n\n")
        for issue in issues:
            log_file.write(f"- {issue}\n")
    
    print(f"📝 Issues saved to {log_filename}")


def save_prompt_to_file(prompt: str, output_path: str) -> None:
    """
    Save the generated prompt to a text file.
    
    Parameters:
        prompt (str): The complete prompt content.
        output_path (str): Destination file path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)


def main():
    """
    Main function to generate and save a language model prompt
    based on the latest resume and a job description.
    """
    input_folder = "original_cv"
    processed_folder = "processed_cv"
    job_desc_path = "job_description.txt"

    try:
        latest_docx = get_latest_docx_file(input_folder)
        md_resume_path = os.path.join(processed_folder, os.path.splitext(latest_docx)[0] + ".md")

        md_resume = clean_markdown_for_prompt(read_file(md_resume_path))
        job_description = read_file(job_desc_path)

        # Validate Markdown content
        issues = validate_markdown(md_resume)
        if issues:
            print("⚠️ Markdown validation failed. Please fix the following issues before proceeding:")
            for issue in issues:
                print("-", issue)
            log_validation_issues(issues, md_resume_path)
            return

        prompt = generate_prompt(md_resume, job_description)
        save_prompt_to_file(prompt, os.path.join(processed_folder, "prompt.txt"))
        print("✅ Prompt saved.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
