# Prompt comparison: task_answer_v1 vs task_answer_v2

Provider used for this run: **fake**. Offline fake LLM: only structure is compared, not answer quality. Re-run with an API key for real quality numbers.

| Prompt | Template chars | Valid JSON | With citations | 'I don't know' |
|---|---|---|---|---|
| v1 | 162 | 10/10 | 8/10 | 2/10 |
| v2 | 526 | 10/10 | 8/10 | 2/10 |

v2 adds an explicit 'check for a later-dated source' step and a forced IDK rule. Expect it to help most on Q3 and Q7 (old vs new composition limit).
