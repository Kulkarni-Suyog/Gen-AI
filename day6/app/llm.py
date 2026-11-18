import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Find day06 folder
BASE_DIR = Path(__file__).resolve().parents[1]

# Load environment variables
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in day06/.env")

client = Groq(api_key=API_KEY)


def generate_response(system_prompt, user_prompt):

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.2,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Groq API Error:", str(e))
        raise