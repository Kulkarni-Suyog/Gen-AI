"""Day 13 - input limits and a simple prompt-injection check.

Put this file at app/guards.py and call validate_question() at the top of
/ask, /chat and /agent before anything reaches retrieval or the LLM.
"""
import re

from fastapi import HTTPException

MAX_QUESTION_CHARS = 500

_VERB = r"(ignore|disregard|forget|override|bypass)"
_NOUN = r"(instructions?|prompts?|rules?|guidelines?)"

INJECTION_PATTERNS = [
    # "ignore all previous instructions", "forget your rules"
    rf"\b{_VERB}\b.{{0,30}}\b(previous|prior|above|earlier|all|your|system|these)\b.{{0,30}}\b{_NOUN}\b",
    # "ignore the instructions", "disregard the prompt"
    rf"\b{_VERB}\b.{{0,30}}\b(instructions?|prompts?)\b",
    # "disregard the rules above"
    rf"\b{_VERB}\b.{{0,30}}\b{_NOUN}\b.{{0,15}}\b(above|before|earlier)\b",
    # asking for hidden text or secrets
    r"\b(reveal|show|print|repeat|leak|tell me)\b.{0,30}\b((system|hidden|initial|original) (prompt|instructions?)|api[ _-]?key|secret key|\.env)\b",
    # role-play jailbreaks
    r"\byou are now (a|an|dan|in)\b|\bact as (a |an )?(dan|unrestricted|jailbroken)\b|\bdeveloper mode\b|\bjailbreak\b|\bpretend (to be|you are)\b",
]
_COMPILED = [re.compile(p) for p in INJECTION_PATTERNS]
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def looks_like_injection(text: str) -> bool:
    normalized = re.sub(r"\s+", " ", text.lower())
    return any(p.search(normalized) for p in _COMPILED)


def validate_question(text: str) -> str:
    """Return the cleaned question, or raise an HTTP error."""
    cleaned = _CONTROL_CHARS.sub("", text or "").strip()
    if not cleaned:
        raise HTTPException(status_code=422, detail={"error": "empty_question"})
    if len(cleaned) > MAX_QUESTION_CHARS:
        raise HTTPException(
            status_code=422,
            detail={"error": "question_too_long", "max_chars": MAX_QUESTION_CHARS},
        )
    if looks_like_injection(cleaned):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "blocked_input",
                "reason": "The message looks like an attempt to change the assistant's instructions.",
            },
        )
    return cleaned
