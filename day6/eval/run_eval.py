import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

API_URL = "http://127.0.0.1:8000/chat"

QUESTIONS_FILE = BASE_DIR / "eval" / "questions.json"
RESULTS_FILE = BASE_DIR / "eval" / "results.json"

def main():

    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    results = []

    for index, question in enumerate(questions, start=1):

        print(f"\nQuestion {index}/10")
        print(question)

        for version in ["v1", "v2"]:

            payload = {
                "question": question,
                "prompt_version": version
            }

            response = requests.post(
                API_URL,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            answer = response.json()

            print(f"\n{version.upper()} Answer:")
            print(answer["answer"])

            results.append({
                "question_number": index,
                "question": question,
                "prompt_version": version,
                "answer": answer["answer"],
                "confidence": answer["confidence"],
                "follow_up": answer["follow_up"]
            })

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n================================")
    print("Evaluation completed!")
    print("Results saved to eval/results.json")
    print("================================")

if __name__ == "__main__":
    main()