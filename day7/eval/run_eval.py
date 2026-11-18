"""Run semantic search for the 10 GSTSaral evaluation questions."""
import json
from pathlib import Path
from app.vectorstore import rebuild_index, search_semantic

BASE = Path(__file__).resolve().parents[1]
QUESTIONS_FILE = BASE / "eval" / "questions.json"
OUTPUT_FILE = BASE / "eval" / "search_results.md"


def main():
    count = rebuild_index()
    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    lines = ["# GSTSaral Semantic Search Evaluation", "", f"Chunks indexed: {count}", "", "Model: sentence-transformers/all-MiniLM-L6-v2", ""]
    for number, question in enumerate(questions, start=1):
        hits = search_semantic(question, top_k=3)
        lines.extend([f"## Q{number}: {question}", ""])
        if not hits:
            lines.append("No results returned.")
        for rank, hit in enumerate(hits, start=1):
            metadata = hit["metadata"]
            lines.extend([
                f"### Hit {rank}",
                f"- Record ID: {hit['id']}",
                f"- Title: {metadata.get('title', 'Unknown')}",
                f"- Source: {metadata.get('source', 'Unknown')}",
                f"- Page: {metadata.get('page', 'not specified')}",
                f"- Distance: {hit['distance']:.4f}",
                f"- Source URL: {metadata.get('source_url', 'not available')}",
                "- Text:",
                "```text",
                hit["text"],
                "```",
                "",
            ])
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Indexed {count} chunks. Evaluation saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
