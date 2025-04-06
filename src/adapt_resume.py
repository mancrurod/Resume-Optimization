import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, OpenAIError
import google.generativeai as genai
from google.api_core import retry

def load_api_keys() -> dict:
    """
    Load API keys from a .env file.
    
    Returns:
        dict: Dictionary with keys for OpenAI and Google.
    """
    load_dotenv()
    return {
        "openai": os.getenv("OPENAI_API_KEY"),
        "google": os.getenv("GOOGLE_API_KEY")
    }


def read_prompt_file(prompt_path: str) -> str:
    """
    Read the full prompt from a text file.

    Parameters:
        prompt_path (str): Path to the prompt.txt file.

    Returns:
        str: Prompt content.
    """
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()


def generate_resume_openai(prompt: str, api_key: str) -> str:
    """
    Generate the adapted resume using OpenAI's GPT-4o-mini model.

    Parameters:
        prompt (str): The prompt to send.
        api_key (str): Your OpenAI API key.

    Returns:
        str: Adapted resume in Markdown format.
    """
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25
    )
    return response.choices[0].message.content


def generate_resume_google(prompt: str, api_key: str) -> str:
    """
    Generate the adapted resume using Google's Gemini model (fallback).

    Parameters:
        prompt (str): The prompt to send.
        api_key (str): Your Google API key.

    Returns:
        str: Adapted resume in Markdown format.
    """
    genai.configure(api_key=api_key)

    @retry.Retry(predicate=retry.if_exception_type(Exception), deadline=60.0)
    def _generate():
        model = genai.GenerativeModel(
            "gemini-2.0-flash-lite-001",
            generation_config={"temperature": 0.25}
        )
        return model.generate_content(prompt).text

    return _generate()


def clean_adapted_markdown(md: str) -> str:
    """
    Clean the response from the LLM by removing enclosing code blocks.

    Parameters:
        md (str): Raw Markdown content returned by the LLM.

    Returns:
        str: Cleaned Markdown text.
    """
    lines = md.strip().splitlines()
    if lines and lines[0].startswith("```") and lines[-1].startswith("```"):
        lines = lines[1:-1]
    return "\n".join(lines).strip() + "\n"


def write_to_file(content: str, path: str) -> None:
    """
    Write the adapted resume to the output file.

    Parameters:
        content (str): Markdown content to write.
        path (str): Path to the output .md file.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def adapt_resume(prompt_path: str, output_path: str) -> None:
    """
    Main function to adapt the resume using LLM APIs.

    Priority: Use OpenAI, fallback to Gemini if rate-limited.

    Parameters:
        prompt_path (str): Path to the input prompt.txt file.
        output_path (str): Destination path for adapted Markdown resume.
    """
    try:
        keys = load_api_keys()
        prompt = read_prompt_file(prompt_path)

        try:
            raw = generate_resume_openai(prompt, keys["openai"])
        except RateLimitError:
            print("⚠️ OpenAI rate limit hit, using Gemini...")
            raw = generate_resume_google(prompt, keys["google"])

        resume = clean_adapted_markdown(raw)
        write_to_file(resume, output_path)
        print(f"✅ Resume saved to {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    prompt_file = "processed_cv/prompt.txt"
    output_file = "processed_cv/adapted_resume.md"
    adapt_resume(prompt_file, output_file)
