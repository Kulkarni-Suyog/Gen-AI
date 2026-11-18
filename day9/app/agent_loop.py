"""Simple hand-written agent that chooses RAG search or the GST calculator."""
from typing import Any, Dict, Optional
from app.rag import answer_question
from app.tools import gst_invoice_calculator

CALCULATION_WORDS = ("calculate", "invoice", "total", "inclusive", "exclusive", "taxable", "cgst", "sgst", "igst", "bill", "price")


def choose_action(question: str, calculator_args: Optional[Dict[str, Any]] = None) -> str:
    if calculator_args is not None:
        return "calculator"
    q = question.lower()
    if any(word in q for word in CALCULATION_WORDS):
        return "calculator"
    return "rag"


def run_agent(question: str, calculator_args: Optional[Dict[str, Any]] = None, top_k: int = 3, config: str = "A") -> Dict[str, Any]:
    action = choose_action(question, calculator_args)
    if action == "calculator":
        if not calculator_args:
            return {
                "action": "calculator",
                "status": "needs_input",
                "answer": "To calculate GST, provide price, GST rate, intra_state (true for Maharashtra/intra-state sale), and inclusive (true if the entered price already includes GST).",
                "required_fields": ["price", "gst_rate", "intra_state", "inclusive"],
            }
        result = gst_invoice_calculator(**calculator_args)
        return {"action": "calculator", "status": "calculated", "answer": result, "tool": "gst_invoice_calculator"}
    result = answer_question(question, top_k=top_k, config=config)
    return {"action": "rag_search", "status": "answered", **result}
