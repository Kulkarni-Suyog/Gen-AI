
from pathlib import Path

from app.vectorstore import semantic_search

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = BASE_DIR / "eval" / "search_results.md"

QUESTIONS = [
    "What is GST in India?",
    "Who is required to register for GST?",
    "What is the GST registration process?",
    "What are the different types of GST?",
    "What is the difference between CGST and SGST?",
    "What is Input Tax Credit under GST?",
    "How can a taxpayer claim Input Tax Credit?",
    "What is the GST return filing process?",
    "What happens if GST returns are filed late?",
    "What is the purpose of an e-way bill?"
]

def run_evaluation():
    """Run semantic search for ten GST questions."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    report = [
        "# GSTSaral Day 07 - Semantic Search Results",
        "",
        "Model: all-MiniLM-L6-v2",
        "",
        "The following results are retrieved from the local GSTSaral",
        "document collection. Similarity scores are retrieval scores,",
        "not measures of factual correctness.",
        ""
    ]

    for number, question in enumerate(QUESTIONS, start=1):

        print(f"\nQuestion {number}: {question}")

        report.append(f"## Question {number}: {question}")
        report.append("")

        try:
            results = semantic_search(question, top_k=3)

            if not results:
                report.append("No matching results found.")
                report.append("")
                continue

            for rank, result in enumerate(results, start=1):

                print(
                    f"Result {rank}: "
                    f"{result['title']} "
                    f"(Similarity: {result['similarity']})"
                )

                report.extend([
                    f"### Result {rank}",
                    f"- **Title:** {result['title']}",
                    f"- **Source:** {result['source']}",
                    f"- **Page:** {result['page']}",
                    f"- **Similarity:** {result['similarity']}",
                    "",
                    "**Retrieved text:**",
                    "",
                    result["text"],
                    ""
                ])

        except Exception as error:
            report.append(f"Search error: {error}")
            report.append("")

        print("-" * 60)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print("\nEvaluation completed!")
    print("Results saved to:", OUTPUT_FILE)

if __name__ == "__main__":
    run_evaluation()