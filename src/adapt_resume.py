import os  # Module for interacting with the operating system
from dotenv import load_dotenv  # Module for loading environment variables from a .env file
from openai import OpenAI, RateLimitError, OpenAIError  # OpenAI SDK for interacting with OpenAI APIs
import google.generativeai as genai  # Google Generative AI SDK
from google.api_core import retry  # Retry mechanism for handling transient errors

def load_api_keys() -> dict:
    """
    Load API keys from a .env file.
    
    Returns:
        dict: Dictionary with keys for OpenAI and Google.
    """
    load_dotenv()  # Load environment variables from a .env file
    return {
        "openai": os.getenv("OPENAI_API_KEY"),  # Fetch OpenAI API key
        "google": os.getenv("GOOGLE_API_KEY")  # Fetch Google API key
    }

def read_prompt_file(prompt_path: str) -> str:
    """
    Read the full prompt from a text file.

    Parameters:
        prompt_path (str): Path to the prompt.txt file.

    Returns:
        str: Prompt content.
    """
    with open(prompt_path, "r", encoding="utf-8") as file:  # Open the file in read mode with UTF-8 encoding
        return file.read()  # Read and return the file content

def generate_resume_openai(prompt: str, api_key: str) -> str:
    """
    Generate the adapted resume using OpenAI's GPT-4o-mini model.

    Parameters:
        prompt (str): The prompt to send.
        api_key (str): Your OpenAI API key.

    Returns:
        str: Adapted resume in Markdown format.
    """
    client = OpenAI(api_key=api_key)  # Initialize OpenAI client with the provided API key
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the model to use
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},  # System message for context
            {"role": "user", "content": prompt}  # User-provided prompt
        ],
        temperature=0.25  # Control randomness in the response
    )
    return response.choices[0].message.content  # Extract and return the generated content

def generate_resume_google(prompt: str, api_key: str) -> str:
    """
    Generate the adapted resume using Google's Gemini model (fallback).

    Parameters:
        prompt (str): The prompt to send.
        api_key (str): Your Google API key.

    Returns:
        str: Adapted resume in Markdown format.
    """
    genai.configure(api_key=api_key)  # Configure the Google Generative AI client with the API key

    @retry.Retry(predicate=retry.if_exception_type(Exception), deadline=60.0)  # Retry on transient errors
    def _generate():
        model = genai.GenerativeModel(
            "gemini-2.0-flash-lite-001",  # Specify the Gemini model to use
            generation_config={"temperature": 0.25}  # Control randomness in the response
        )
        return model.generate_content(prompt).text  # Generate and return the content

    return _generate()  # Call the retry-wrapped function

def clean_adapted_markdown(md: str) -> str:
    """
    Clean the response from the LLM by removing enclosing code blocks.

    Parameters:
        md (str): Raw Markdown content returned by the LLM.

    Returns:
        str: Cleaned Markdown text.
    """
    lines = md.strip().splitlines()  # Split the Markdown content into lines and strip whitespace
    if lines and lines[0].startswith("```") and lines[-1].startswith("```"):  # Check for enclosing code blocks
        lines = lines[1:-1]  # Remove the first and last lines if they are code block markers
    return "\n".join(lines).strip() + "\n"  # Join the cleaned lines and ensure a trailing newline

def write_to_file(content: str, path: str) -> None:
    """
    Write the adapted resume to the output file.

    Parameters:
        content (str): Markdown content to write.
        path (str): Path to the output .md file.
    """
    with open(path, "w", encoding="utf-8") as f:  # Open the file in write mode with UTF-8 encoding
        f.write(content)  # Write the content to the file

def adapt_resume(prompt_path: str, output_path: str) -> None:
    """
    Main function to adapt the resume using LLM APIs.

    Priority: Use OpenAI, fallback to Gemini if rate-limited.

    Parameters:
        prompt_path (str): Path to the input prompt.txt file.
        output_path (str): Destination path for adapted Markdown resume.
    """
    try:
        keys = load_api_keys()  # Load API keys from the .env file
        prompt = read_prompt_file(prompt_path)  # Read the prompt from the specified file

        try:
            raw = generate_resume_openai(prompt, keys["openai"])  # Try generating the resume using OpenAI
        except RateLimitError:  # Handle OpenAI rate limit errors
            print("⚠️ OpenAI rate limit hit, using Gemini...")  # Notify the user about fallback
            raw = generate_resume_google(prompt, keys["google"])  # Fallback to Google's Gemini model

        resume = clean_adapted_markdown(raw)  # Clean the generated Markdown content
        write_to_file(resume, output_path)  # Write the cleaned content to the output file
        print(f"✅ Resume saved to {output_path}")  # Notify the user about successful completion

    except Exception as e:  # Catch any unexpected errors
        print(f"❌ Error: {e}")  # Print the error message

if __name__ == "__main__":
    # Define the input prompt file and output resume file paths
    prompt_file = "processed_cv/prompt.txt"
    output_file = "processed_cv/adapted_resume.md"
    adapt_resume(prompt_file, output_file)  # Call the main function to adapt the resume
