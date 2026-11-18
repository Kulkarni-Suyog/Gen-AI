"""Retrieval-augmented GSTSaral answers with source citations."""
from typing import Any, Dict, List
from app.vectorstore import search_chunks

SYSTEM_PROMPT = """You are GSTSaral, an assistant that answers questions only using the supplied GST records.
Rules:
- Use only the CONTEXT below. Do not add outside facts or guess.
- If the context does not answer the question, say exactly: I don't know based on the available GSTSaral records.
- Answer clearly and briefly. Mention relevant dates and old/new rates if present.
- Cite every factual statement with record citations in square brackets, such as [Record 5].
- Do not invent record IDs, sources, dates, or rates.
"""


def build_context(hits: List[Dict[str, Any]]) -> str:
    lines = []
    for hit in hits:
        meta = hit.get("metadata", {})
        record_id = meta.get("record_id", hit.get("id", "unknown"))
        title = meta.get("title", "GST record")
        source = meta.get("source", "GSTSaral dataset")
        page = meta.get("page", "not specified")
        url = meta.get("source_url", "")
        lines.append(f"[Record {record_id}] Title: {title}\nSource: {source}\nPage: {page}\nURL: {url}\n{hit.get('text', '')}")
    return "\n\n---\n\n".join(lines)


def answer_question(question: str, top_k: int = 3, config: str = "A") -> Dict[str, Any]:
    hits = search_chunks(question, top_k=top_k, config=config)
    context = build_context(hits)
    if not context.strip():
        return {"answer": "I don't know based on the available GSTSaral records.", "citations": [], "retrieved": []}
    from app.llm import generate_answer
    answer = generate_answer(question=question, context=context, system_prompt=SYSTEM_PROMPT)
    citations = []
    seen = set()
    for hit in hits:
        meta = hit.get("metadata", {})
        rid = str(meta.get("record_id", hit.get("id", "unknown")))
        if rid not in seen:
            seen.add(rid)
            citations.append({"record_id": rid, "title": meta.get("title", "GST record"), "source": meta.get("source", "GSTSaral dataset"), "page": meta.get("page", "not specified"), "source_url": meta.get("source_url", "")})
    return {"answer": answer, "citations": citations, "retrieved": [{"record_id": h.get("metadata", {}).get("record_id", h.get("id")), "distance": h.get("distance")} for h in hits]}
