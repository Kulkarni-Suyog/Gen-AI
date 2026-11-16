"""RAG: answer GSTSaral questions from retrieved chunks, with citations and 'latest rule wins'."""

from __future__ import annotations

import os
import re
from pathlib import Path

from app import llm
from app.conflicts import conflict_warning, newer_rule
from app.records import get_by_id, load_records
from app.vectorstore import COLLECTION, semantic_search

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"
MIN_SCORE = float(os.getenv("RAG_MIN_SCORE", "0.12"))
MAX_QUESTION_CHARS = 500
IDK = "I don't know based on the sources I have."

INJECTION_RE = re.compile(
    r"(ignore|disregard|forget)\s+(all\s+|any\s+|the\s+|your\s+)?(previous\s+|prior\s+|above\s+)?(instructions|rules|prompt)"
    r"|reveal\s+(the\s+|your\s+)?system\s+prompt|you\s+are\s+now\s+",
    re.I,
)


def load_prompt(name: str) -> str:
    return (PROMPTS / f"{name}.md").read_text(encoding="utf-8")


def validate_question(question: str) -> str | None:
    """Return an error message if the input is not acceptable, else None."""
    if not question or not question.strip():
        return "Please type a question."
    if len(question) > MAX_QUESTION_CHARS:
        return f"Question too long (max {MAX_QUESTION_CHARS} characters)."
    if INJECTION_RE.search(question):
        return "That looks like an attempt to change my instructions. I can only answer GST questions from my sources."
    return None


def _record_for_chunk(hit: dict, records: list[dict]) -> list[dict]:
    ids = [int(x) for x in hit["metadata"].get("record_ids", "").split(",") if x]
    return [r for r in (get_by_id(i, records) for i in ids) if r]


def retrieve(question: str, top_k: int = 4, collection: str = COLLECTION, min_score: float = MIN_SCORE) -> list[dict]:
    hits = semantic_search(question, k=top_k, name=collection)
    return [h for h in hits if h["score"] >= min_score]


def ask(
    question: str,
    top_k: int = 4,
    prompt_version: str = "v2",
    collection: str = COLLECTION,
    min_score: float = MIN_SCORE,
) -> dict:
    err = validate_question(question)
    if err:
        return _response(err, "low", "Ask me about a GST rate or limit.", [], [], 0, "guard", refused=True)

    records = load_records()
    hits = retrieve(question, top_k, collection, min_score)
    if not hits:
        return _response(IDK, "low", "Would you like to ask about a specific item's rate?", [], [], 0, "none")

    # Collect source records; if a hit is superseded, pull in the newer rule too.
    sources: dict[int, dict] = {}
    warnings: list[dict] = []
    for h in hits:
        for r in _record_for_chunk(h, records):
            sources.setdefault(r["id"], {**r, "score": h["score"]})
            w = conflict_warning(r, records)
            if w:
                warnings.append(w)
                latest = newer_rule(r, records)
                sources.setdefault(latest["id"], {**latest, "score": h["score"]})
    # Latest rule first; never average old and new.
    ordered = sorted(sources.values(), key=lambda r: (r["effective_from"], r["score"]), reverse=True)

    numbered = "\n".join(
        f"[{i}] {r['item_or_topic']}. Old rule: {r['old_rule']}. New rule: {r['new_rule']}. "
        f"Effective from {r['effective_from']}. (Document: {r['document']})"
        for i, r in enumerate(ordered, start=1)
    )
    system = load_prompt("system")
    user = load_prompt(f"task_answer_{prompt_version}").format(sources=numbered, question=question)
    out = llm.chat(system, user)
    data = llm.parse_json(out["text"]) or {"answer": out["text"], "confidence": "low", "follow_up": ""}

    citations = [
        {
            "n": i,
            "id": r["id"],
            "title": r["item_or_topic"],
            "document": r["document"],
            "source_url": r["source_url"],
            "effective_from": r["effective_from"],
            "verified": r.get("verified", True),
        }
        for i, r in enumerate(ordered, start=1)
    ]
    retrieved = [{"id": h["id"], "score": h["score"]} for h in hits]
    return _response(
        data.get("answer", IDK),
        data.get("confidence", "low"),
        data.get("follow_up", ""),
        citations,
        _dedupe(warnings),
        out.get("tokens", 0),
        out.get("provider", "?"),
        retrieved=retrieved,
    )


def _dedupe(warnings: list[dict]) -> list[dict]:
    seen, out = set(), []
    for w in warnings:
        key = (w["old"]["id"], w["new"]["id"])
        if key not in seen:
            seen.add(key)
            out.append(w)
    return out


def _response(answer, confidence, follow_up, citations, warnings, tokens, provider, retrieved=None, refused=False):
    return {
        "answer": answer,
        "confidence": confidence,
        "follow_up": follow_up,
        "citations": citations,
        "warnings": warnings,
        "tokens": tokens,
        "provider": provider,
        "retrieved": retrieved or [],
        "refused": refused,
    }
