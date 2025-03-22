import os


def generate_prompt(md_resume: str, job_description: str) -> str:
    """Generates a tailored resume optimization prompt based on job description."""
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
    Return the **optimized resume in Markdown format**, ensuring it is refined according to the outlined objectives.  
    """


def get_latest_docx_file(input_folder: str) -> str:
    """Returns the path of the most recently modified .docx file in the input folder."""
    docx_files = [f for f in os.listdir(input_folder) if f.endswith(".docx")]
    
    if not docx_files:
        raise FileNotFoundError(f"No .docx file found in folder: {input_folder}")
    
    latest_file = sorted(docx_files, key=lambda f: os.path.getmtime(os.path.join(input_folder, f)))[-1]
    return latest_file


def read_file(file_path: str) -> str:
    """Reads the content of a file and returns it as a string."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def save_prompt_to_file(prompt: str, output_path: str) -> None:
    """Saves the generated prompt string to the specified file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure output folder exists
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(prompt)


def main():
    # Define folder paths
    input_folder = "original_cv"
    processed_folder = "processed_cv"
    job_desc_path = "job_description.txt"

    try:
        # Get the latest .docx file and construct the corresponding Markdown resume path
        latest_docx = get_latest_docx_file(input_folder)
        md_resume_path = os.path.join(processed_folder, os.path.splitext(latest_docx)[0] + ".md")

        # Read the contents of the Markdown resume and job description
        md_resume = read_file(md_resume_path)
        job_description = read_file(job_desc_path)

        # Generate the tailored prompt
        prompt = generate_prompt(md_resume, job_description)

        # Save the generated prompt to a text file
        output_prompt_path = os.path.join(processed_folder, "prompt.txt")
        save_prompt_to_file(prompt, output_prompt_path)

        print(f"Prompt successfully generated and saved to {output_prompt_path}")

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
