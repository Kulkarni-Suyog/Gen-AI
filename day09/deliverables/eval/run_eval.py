import json
from app.rag import answer_question

rows = json.loads(open("eval/eval_set.json", encoding="utf-8").read())
for i, row in enumerate(rows, 1):
    result = answer_question(row["question"])
    print(f"{i}. Q: {row['question']}\n   Answer: {result['answer'][:300]}\n")
