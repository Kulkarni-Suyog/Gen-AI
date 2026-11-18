"""Groq LLM client wrapper."""
import os
from dotenv import load_dotenv
load_dotenv()


def generate_answer(question: str, context: str, system_prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Create a .env file from .env.example.")
    from groq import Groq
    client = Groq(api_key=api_key)
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"QUESTION:\n{question}\n\nCONTEXT:\n{context}"},
        ],
    )
    return response.choices[0].message.content.strip()
