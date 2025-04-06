# ⚙️ Installation

## Requirements

- Python 3.10+
- `wkhtmltopdf` installed and accessible in PATH
- API keys from OpenAI and Google (Gemini)

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create your `.env` file:

```bash
cp .env.example .env
```

3. Add your keys:

```env
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```