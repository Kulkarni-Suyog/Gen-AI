# Resume bullets – GSTSaral

Replace every <...> with your own measured number from `scripts/bench.py`, `/metrics` and your Day 8 eval before using these.

- Built **GSTSaral**, a RAG assistant on official GST Council documents (FastAPI, Chroma, Groq/Gemini, Streamlit) that ranks sources by date so the latest rule wins and flags outdated FAQs; answered <X>/15 eval questions correctly with citations and correctly refused the out-of-scope question.
- Moved invoice and GST-split calculations out of the LLM into a tested Python tool (CGST+SGST/IGST, inclusive-price back-calculation), so every rupee figure in an answer is computed, not generated.
- Took it to production: GitHub Actions CI (ruff, pytest, Docker build), deployed on Render, added request logging with latency and token tracking, a TTL cache (p50 <before> ms to <after> ms on repeat questions), input limits and a prompt-injection guard covered by automated tests.
