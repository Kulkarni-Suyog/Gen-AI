import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# Find Day 09 folder
BASE_DIR = Path(__file__).resolve().parents[1]

# Load Day 09 .env file
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)


# Get API key
API_KEY = os.getenv("GROQ_API_KEY")

MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)


# Check API key
if not API_KEY:
    raise RuntimeError(
        f"GROQ_API_KEY is missing. Please add it to: {ENV_FILE}"
    )


# Connect to Groq
client = Groq(api_key=API_KEY)


# Generate answer
def generate_answer(question, context, system_prompt):

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
                    "content": (
                        f"Question: {question}\n\n"
                        f"Context:\n{context}\n\n"
                        "Answer the question using the supplied context. "
                        "If the context does not contain the answer, "
                        "clearly say so."
                    )
                }
            ],

            temperature=0.2,
            max_tokens=1000

        )

        answer = response.choices[0].message.content

        return answer or "No answer was generated."

    except Exception as e:

        print("Groq API Error:", str(e))

        raise