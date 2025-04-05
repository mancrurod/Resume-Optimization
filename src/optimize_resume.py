
import os
import re

def generate_prompt(md_resume: str, job_description: str) -> str:
    return f"""
    I have a resume in Markdown format and a job description. Your task is to **refine and tailor my resume** to closely match the job requirements while ensuring it remains professional, well-structured, and ATS-friendly.  

    ### **Key Objectives:**  
    - Align my resume with the job description by emphasizing **relevant skills, experiences, and achievements**.  
    - **Incorporate** keywords and phrases from the job posting to improve ATS compatibility.  
    - **Enhance bullet points** by making them **quantifiable** and **impact-driven**.  
    - Ensure **clarity, conciseness, and a professional tone**.  
    - Maintain the **Markdown format**, preserving proper spacing, bullet points, and hyperlinks.  
    - **Position dates** after each work/study experience on a **new line** for better readability.
    - If my **education or experience does not fully match** the job description, identify and emphasize **transferable skills** that demonstrate my ability to perform the role effectively.  

    ### **Language Guidelines:**  
    - If **both** the resume and job description are in **Spanish**, return the revised resume in **Spanish**.  
    - If **both** are in **English**, return the revised resume in **English**.  
    - If they are in **different languages**, keep the language of the original resume.  

    ### **Input Data:**  
    #### **Resume (Markdown format):**  
    {md_resume}  

    #### **Job Description:**  
    {job_description}  

    ### **Expected Output:**  
    Return the **optimized resume in Markdown**, ensuring it is refined according to the outlined objectives.  
    **Do not enclose the output in code blocks (\`\`\`), return it as plain Markdown content.**
    """

def get_latest_docx_file(input_folder: str) -> str:
    docx_files = [f for f in os.listdir(input_folder) if f.endswith(".docx")]
    if not docx_files:
        raise FileNotFoundError(f"No .docx file found in folder: {input_folder}")
    return sorted(docx_files, key=lambda f: os.path.getmtime(os.path.join(input_folder, f)))[-1]

def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def clean_markdown_for_prompt(md_text: str) -> str:
    lines = md_text.strip().splitlines()
    if lines and lines[0].startswith("```") and lines[-1].startswith("```"):
        lines = lines[1:-1]
    return "\n".join(lines).strip()

def save_prompt_to_file(prompt: str, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)

def main():
    input_folder = "original_cv"
    processed_folder = "processed_cv"
    job_desc_path = "job_description.txt"

    try:
        latest_docx = get_latest_docx_file(input_folder)
        md_resume_path = os.path.join(processed_folder, os.path.splitext(latest_docx)[0] + ".md")

        md_resume = clean_markdown_for_prompt(read_file(md_resume_path))
        job_description = read_file(job_desc_path)

        prompt = generate_prompt(md_resume, job_description)
        save_prompt_to_file(prompt, os.path.join(processed_folder, "prompt.txt"))
        print("✅ Prompt saved.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
