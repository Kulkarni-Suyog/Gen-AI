"""LangGraph agent with MemorySaver and a single approval node."""
from typing import Any, Dict, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.agent_loop import choose_action
from app.tools import gst_invoice_calculator
from app.rag import answer_question

class AgentState(TypedDict, total=False):
    question: str
    calculator_args: Dict[str, Any]
    top_k: int
    config: str
    approved: bool
    action: str
    result: Dict[str, Any]
    status: str
    answer: Any


def route_node(state: AgentState):
    action = choose_action(state.get("question", ""), state.get("calculator_args"))
    return {"action": action}


def execute_node(state: AgentState):
    action = state.get("action", "rag")
    if action == "calculator":
        args = state.get("calculator_args")
        if not args:
            return {"status": "needs_input", "answer": "Provide price, gst_rate, intra_state, and inclusive to calculate GST."}
        result = gst_invoice_calculator(**args)
        return {"status": "awaiting_approval", "result": result, "answer": result}
    rag = answer_question(state.get("question", ""), top_k=state.get("top_k", 3), config=state.get("config", "A"))
    return {"status": "answered", "result": rag, "answer": rag}


def approval_node(state: AgentState):
    if state.get("action") != "calculator" or state.get("status") != "awaiting_approval":
        return {}
    if state.get("approved", False):
        return {"status": "approved", "answer": {"approved": True, "calculation": state.get("result")}}
    return {"status": "pending_approval", "answer": {"approved": False, "message": "Calculation is ready. Review and send approved=true to confirm it.", "calculation": state.get("result")}}


def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("route", route_node)
    workflow.add_node("execute", execute_node)
    workflow.add_node("approval", approval_node)
    workflow.set_entry_point("route")
    workflow.add_edge("route", "execute")
    workflow.add_edge("execute", "approval")
    workflow.add_edge("approval", END)
    return workflow.compile(checkpointer=MemorySaver())

agent_graph = build_graph()


def run_graph(payload: Dict[str, Any], thread_id: str = "default") -> Dict[str, Any]:
    config = {"configurable": {"thread_id": thread_id}}
    state = agent_graph.invoke(payload, config=config)
    return {"thread_id": thread_id, "action": state.get("action"), "status": state.get("status"), "answer": state.get("answer")}
