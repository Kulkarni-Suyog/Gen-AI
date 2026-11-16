"""Run the 10 GST questions through semantic search and write eval/search_results.md.

Usage (from the day07 folder):  python -m app.evaluate_search
"""

from __future__ import annotations

from pathlib import Path

from app.vectorstore import build_index, semantic_search

ROOT = Path(__file__).resolve().parent.parent
OUT_FILE = ROOT / "eval" / "search_results.md"
TOP_K = 3

QUESTIONS = [
    "What is the GST rate on toilet soap now?",
    "Is paneer still taxed after September 2025?",
    "Up to what turnover can I use the composition scheme?",
    "Do I pay GST on roti and chapati?",
    "What is the rate on notebooks for school?",
    "What GST will apply to my shop next year after the next Council meeting?",
    "What is the old composition limit of 75 lakh?",
    "What is the GST on TV and AC?",
    "Is crypto taxed under GST?",
    "GST on baby diapers",
]


def run() -> str:
    build_index()  # fresh index so results always match current data
    lines = [
        "# Semantic search results for the 10 questions",
        "",
        f"Top {TOP_K} hits per question (score = cosine similarity).",
        "",
    ]
    for i, q in enumerate(QUESTIONS, 1):
        lines.append(f"**Q{i}. {q}**")
        for h in semantic_search(q, TOP_K):
            title = h["metadata"].get("title", "?")
            lines.append(f"- {h['score']:.3f} | {title} (id {h['id']})")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(run(), encoding="utf-8")
    print(f"Wrote {OUT_FILE}")
