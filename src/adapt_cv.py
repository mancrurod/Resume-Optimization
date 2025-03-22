import os
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, OpenAIError
import google.generativeai as genai
from google.api_core import retry

def load_api_keys() -> dict:
    """Loads and returns the OpenAI and Google API keys from environment variables."""
    load_dotenv()
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not openai_api_key:
        raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in .env file.")
    if not google_api_key:
        raise ValueError("Missing Google API key. Set GOOGLE_API_KEY in .env file.")
    
    return {"openai": openai_api_key, "google": google_api_key}

def read_prompt_file(prompt_path: str) -> str:
    """Reads and returns the prompt from the specified file."""
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()

def generate_resume_openai(prompt: str, openai_api_key: str) -> str:
    """Generates resume content using OpenAI API."""
    openai_client = OpenAI(api_key=openai_api_key)
    
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25
    )
    return response.choices[0].message.content

def generate_resume_google(prompt: str, google_api_key: str) -> str:
    """Generates resume content using Google Gemini API."""
    genai.configure(api_key=google_api_key)

    @retry.Retry(predicate=retry.if_exception_type(Exception), deadline=60.0)
    def generate_with_retry():
        gemini_prompt = [{"role": "user", "parts": [{"text": prompt}]}]
        model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite-001", generation_config={"temperature": 0.25})
        response = model.generate_content(gemini_prompt)
        return response.text

    return generate_with_retry()

def write_resume_to_file(resume: str, output_path: str):
    """Writes the generated resume to the specified output file."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(resume)
    print(f"✅ Optimized resume saved to {output_path}")

def adapt_resume(prompt_path: str, output_path: str):
    """Attempts to adapt the resume using OpenAI API, falling back to Google Gemini API on failure."""
    try:
        # Load API keys
        keys = load_api_keys()
        
        # Read the prompt from the file
        prompt = read_prompt_file(prompt_path)
        
        # Attempt to generate resume using OpenAI
        try:
            resume = generate_resume_openai(prompt, keys["openai"])
            print("🎉 Successfully generated resume using OpenAI API.")
        except RateLimitError:
            print("⚠️  OpenAI rate limit reached. Falling back to Google Gemini API...")
            resume = generate_resume_google(prompt, keys["google"])
            print("🎉 Successfully generated resume using Google Gemini API.")
        except OpenAIError as e:
            raise Exception(f"❌ OpenAI API error: {e}")
        
        # Write the adapted resume to the output file
        write_resume_to_file(resume, output_path)
    
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    prompt_file = "processed_cv/prompt.txt"
    output_file = os.path.join("processed_cv", os.path.splitext(os.path.basename(prompt_file))[0] + "_adapted.md")
    adapt_resume(prompt_file, output_file)
