from app.records import load_records, search
from app.vectorstore import LocalVectorStore
from app.llm import generate_answer
from pathlib import Path

SYSTEM_PROMPT = Path("prompts/system.txt").read_text(encoding="utf-8") if Path("prompts/system.txt").exists() else "Use only source context. Do not guess."

def answer_question(question: str, top_k: int = 5) -> dict:
    records = load_records()
    matches = search(records, question)
    store = LocalVectorStore()
    chunks = store.search(question, top_k=top_k)
    context_parts = []
    for row in matches[:top_k]:
        context_parts.append(f"Record: {row.get('item_or_topic')} | old: {row.get('old_rule')} | current/demo: {row.get('new_rule')} | effective: {row.get('effective_from')} | source: {row.get('document')} {row.get('source_url')}")
    for chunk in chunks:
        context_parts.append(f"Document chunk ({chunk.get('source')}): {chunk.get('text','')[:900]}")
    context = "\n".join(context_parts)
    if not context:
        return {"answer": "I don't know from the available GSTSaral records. Please provide the exact product description or official notification.", "confidence": 0.0, "follow_up": "Can you share the exact product name and HSN code?", "citations": []}
    prompt = f"Question: {question}\n\nSource context:\n{context}"
    generated = generate_answer(SYSTEM_PROMPT, prompt)
    citations = [{"document": r.get("document"), "source_url": r.get("source_url"), "effective_from": r.get("effective_from")} for r in matches[:top_k]]
    if generated:
        answer = generated
    else:
        answer = "Here is the closest information in the GSTSaral sample records. " + "\n".join(f"- {r.get('item_or_topic')}: {r.get('old_rule')} → {r.get('new_rule')} (effective {r.get('effective_from')})." for r in matches[:3])
        answer += "\n\nNote: sample data must be checked against the exact HSN classification and latest notification before applying it to an invoice."
    return {"answer": answer, "confidence": 0.55 if matches else 0.2, "follow_up": "What is the exact product description or HSN code?", "citations": citations, "warning": _old_faq_warning(matches)}

def _old_faq_warning(matches):
    for row in matches:
        if "2017" in str(row.get("document")) or "2018" in str(row.get("document")):
            return {"message": "This FAQ may be outdated. Check the later notified rule and compare both citations.", "document": row.get("document")}
    return None
