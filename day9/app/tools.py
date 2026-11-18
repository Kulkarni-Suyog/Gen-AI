"""GST invoice calculator tool for GSTSaral Day 9."""
from typing import Dict, Any


def gst_invoice_calculator(
    price: float,
    gst_rate: float,
    intra_state: bool = True,
    inclusive: bool = False,
) -> Dict[str, Any]:
    """Calculate GST for an item price.

    Args:
        price: Amount in INR. Inclusive price if inclusive=True; otherwise taxable value.
        gst_rate: GST rate as percentage, e.g. 5, 12, 18, or 28.
        intra_state: True for Maharashtra/intra-state sale; False for inter-state.
        inclusive: True when price already includes GST.
    """
    if price < 0:
        raise ValueError("Price cannot be negative.")
    if not 0 <= gst_rate <= 100:
        raise ValueError("GST rate must be between 0 and 100.")

    rate = gst_rate / 100.0
    if inclusive:
        taxable_value = price / (1 + rate) if rate else price
        gst_amount = price - taxable_value
        total = price
    else:
        taxable_value = price
        gst_amount = taxable_value * rate
        total = taxable_value + gst_amount

    if intra_state:
        cgst = gst_amount / 2
        sgst = gst_amount / 2
        igst = 0.0
        tax_type = "CGST + SGST"
    else:
        cgst = 0.0
        sgst = 0.0
        igst = gst_amount
        tax_type = "IGST"

    return {
        "price_input": round(price, 2),
        "price_inclusive_of_gst": inclusive,
        "taxable_value": round(taxable_value, 2),
        "gst_rate_percent": round(gst_rate, 2),
        "cgst": round(cgst, 2),
        "sgst": round(sgst, 2),
        "igst": round(igst, 2),
        "total_gst": round(gst_amount, 2),
        "total_amount": round(total, 2),
        "tax_type": tax_type,
        "place_of_supply_type": "intra-state (Maharashtra)" if intra_state else "inter-state",
        "calculation_note": "GST was backed out of the inclusive price." if inclusive else "GST was added to the taxable value.",
    }
