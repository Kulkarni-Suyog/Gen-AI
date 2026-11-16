# Eval results (15 questions, offline hashed embeddings, fake LLM)

| Config | Answerable hit rate | Correct 'I don't know' | Overall |
|---|---|---|---|
| A: per-record chunks, top-k 3 **(winner)** | 12/12 | 3/3 | 100% |
| B: grouped chunks (4 records), top-k 3 | 11/12 | 3/3 | 93% |
| C: per-record chunks, top-k 5 | 12/12 | 3/3 | 100% |
