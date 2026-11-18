# GSTSaral Day 9 — Agent, Tools, and LangGraph

Day 9 extends Day 8 RAG with a GST invoice calculator, a hand-written agent loop, a LangGraph workflow with memory, and a one-step approval gate.

## Features
- `app/tools.py`: `gst_invoice_calculator` supports GST-exclusive and GST-inclusive prices. Intra-state sales split GST into CGST and SGST; inter-state sales use IGST.
- `app/agent_loop.py`: routes calculator requests to the tool and other GST questions to Day 8 RAG.
- `app/graph.py`: LangGraph route → execute → approval flow, compiled with `MemorySaver`.
- `POST /agent`: run the agent or graph.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Add your Groq key to `.env`; never commit it.

## Start API
```powershell
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs.

## GST calculation example
`POST /agent`:
```json
{
  "question": "Calculate GST on a 1000 rupee taxable value at 18 percent in Maharashtra",
  "price": 1000,
  "gst_rate": 18,
  "intra_state": true,
  "inclusive": false,
  "use_graph": true,
  "approved": false,
  "thread_id": "invoice-demo-1"
}
```
The first graph response returns `pending_approval` and the calculation. Review it, then repeat with the same `thread_id` and `approved: true` to confirm.

For GST-inclusive price, set `inclusive: true`. For an inter-state sale set `intra_state: false`, which returns IGST.

## RAG question example
```json
{ "question": "What is the GST rate on shampoo?", "use_graph": true, "thread_id": "gst-question-1" }
```

## Day 9 checklist
- [x] GST calculator tool
- [x] Hand-written agent loop
- [x] RAG search path
- [x] LangGraph workflow
- [x] MemorySaver checkpointing
- [x] Approval node
- [x] POST /agent
- [ ] Run locally with Groq and Chroma

Commit message suggested: `day-09: add GST tool and LangGraph agent`
