"""LLM provider wrapper: Groq, Gemini, or an offline fake (default when no key is set).

Env:
    LLM_PROVIDER = groq | gemini | fake   (auto: groq if GROQ_API_KEY, gemini if GEMINI_API_KEY, else fake)
    GROQ_API_KEY, GROQ_MODEL (default llama-3.3-70b-versatile)
    GEMINI_API_KEY, GEMINI_MODEL (default gemini-1.5-flash)
"""

from __future__ import annotations

import json
import os
import re

import requests

try:  # optional .env support
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

TIMEOUT = 30


def provider() -> str:
    p = os.getenv("LLM_PROVIDER", "").lower()
    if p:
        return p
    if os.getenv("GROQ_API_KEY"):
        return "groq"
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    return "fake"


def chat(system: str, user: str, temperature: float = 0.1) -> dict:
    """Return {"text": str, "tokens": int, "provider": str}."""
    p = provider()
    if p == "groq":
        return _groq(system, user, temperature)
    if p == "gemini":
        return _gemini(system, user, temperature)
    return _fake(system, user)


def _groq(system: str, user: str, temperature: float) -> dict:
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
        json={
            "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            "temperature": temperature,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        },
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    return {
        "text": data["choices"][0]["message"]["content"],
        "tokens": data.get("usage", {}).get("total_tokens", 0),
        "provider": "groq",
    }


def _gemini(system: str, user: str, temperature: float) -> dict:
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        params={"key": os.environ["GEMINI_API_KEY"]},
        json={
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": temperature},
        },
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    return {
        "text": data["candidates"][0]["content"]["parts"][0]["text"],
        "tokens": data.get("usageMetadata", {}).get("totalTokenCount", 0),
        "provider": "gemini",
    }


def _fake(system: str, user: str) -> dict:
    """Deterministic offline stand-in: answers from the first numbered source in the prompt."""
    m = re.search(r"\[1\]\s*(.+)", user)
    if m:
        answer = f"According to the sources: {m.group(1).strip()} [1]"
        conf = "medium"
    else:
        answer = "I don't know based on the sources I have."
        conf = "low"
    text = json.dumps({"answer": answer, "confidence": conf, "follow_up": "Do you want the rate for another item?"})
    return {"text": text, "tokens": (len(system) + len(user)) // 4, "provider": "fake"}


def parse_json(text: str) -> dict | None:
    """Extract the first JSON object from model text (handles ```json fences)."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
