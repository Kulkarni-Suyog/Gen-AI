Decide how to handle the shopkeeper's message. Choose one tool:
- "gst_invoice_calculator": they give a price and a GST rate and want tax split or total. args: price, rate, within_maharashtra (bool), price_includes_gst (bool)
- "rag_search": they ask about a rule, rate, limit or date.

Reply with JSON only: {{"tool": "...", "args": {{...}}}}

Message: {question}
