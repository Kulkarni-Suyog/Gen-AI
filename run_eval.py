"""Evaluate retrieval + 'I don't know' behaviour for 2 configs; writes eval/results.md.

    python -m eval.run_eval
"""

from __future__ import annotations

import json
from pathlib import Path

from app import vectorstore
from app.chunking import chunk_records
from app.rag import IDK, ask

HERE = Path(__file__).parent
CONFIGS = [
    {"name": "A: per-record chunks, top-k 3", "group_size": 1, "top_k": 3},
    {"name": "B: grouped chunks (4 records), top-k 3", "group_size": 4, "top_k": 3},
    {"name": "C: per-record chunks, top-k 5", "group_size": 1, "top_k": 5},
]


def evaluate(cfg: dict, rows: list[dict]) -> dict:
    col = f"eval_{cfg['name'][0].lower()}"
    vectorstore.build_index(chunk_records(group_size=cfg["group_size"]), name=col)
    hits = idk_ok = 0
    answerable = sum(r["answerable"] for r in rows)
    unanswerable = len(rows) - answerable
    for r in rows:
        out = ask(r["question"], top_k=cfg["top_k"], collection=col)
        if r["answerable"]:
            got = {int(i) for c in out["citations"] for i in [c["id"]]}
            if got & set(r["expected_ids"]):
                hits += 1
        elif out["answer"].startswith(IDK[:20]) and not out["citations"]:
            idk_ok += 1
    return {
        "config": cfg["name"],
        "answerable_hit_rate": f"{hits}/{answerable}",
        "idk_correct": f"{idk_ok}/{unanswerable}",
        "score": (hits + idk_ok) / len(rows),
    }


def main() -> None:
    rows = json.loads((HERE / "eval_set.json").read_text(encoding="utf-8"))
    results = [evaluate(c, rows) for c in CONFIGS]
    best = max(results, key=lambda r: r["score"])
    lines = ["# Eval results (15 questions, offline hashed embeddings, fake LLM)", "",
             "| Config | Answerable hit rate | Correct 'I don't know' | Overall |", "|---|---|---|---|"]
    for r in results:
        mark = " **(winner)**" if r is best else ""
        lines.append(f"| {r['config']}{mark} | {r['answerable_hit_rate']} | {r['idk_correct']} | {r['score']:.0%} |")
    out = "\n".join(lines) + "\n"
    (HERE / "results.md").write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
