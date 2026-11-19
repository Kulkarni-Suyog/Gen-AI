"""Tests for the GST calculator and agent routing/tool execution."""
import pytest
from app.tools import gst_invoice_calculator
from app.agent_loop import choose_action, run_agent

def test_calculator_splits_intra_state_tax():
    result = gst_invoice_calculator(price=1000, gst_rate=18, intra_state=True)
    assert result["cgst"] == 90.0
    assert result["sgst"] == 90.0
    assert result["igst"] == 0.0
    assert result["total_amount"] == 1180.0

def test_calculator_uses_igst_for_inter_state():
    result = gst_invoice_calculator(price=1000, gst_rate=18, intra_state=False)
    assert result["igst"] == 180.0
    assert result["cgst"] == 0.0
    assert result["sgst"] == 0.0

def test_calculator_rejects_negative_price():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        gst_invoice_calculator(price=-1, gst_rate=18)

def test_agent_selects_calculator_for_calculation_question():
    assert choose_action("Please calculate GST on this invoice") == "calculator"

def test_agent_runs_calculator_tool_when_arguments_are_supplied():
    result = run_agent(
        "calculate GST",
        calculator_args={"price": 1000, "gst_rate": 18, "intra_state": True},
    )
    assert result["action"] == "calculator"
    assert result["status"] == "calculated"
    assert result["tool"] == "gst_invoice_calculator"
