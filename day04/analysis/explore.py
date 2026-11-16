"""Print 3 facts about the GSTSaral records with pandas.   python -m analysis.explore"""

import pandas as pd

from app.records import load_records

df = pd.DataFrame(load_records())

# Fact 1: how many items per category
print("Fact 1 - records per category:")
print(df["category"].value_counts().to_string(), "\n")

# Fact 2: which rate transitions are most common (old -> new)
pairs = (df["old_rule"] + "  ->  " + df["new_rule"]).value_counts()
print("Fact 2 - most common rate change:")
print(f"{pairs.index[0]}  ({pairs.iloc[0]} records)\n")

# Fact 3: how many records are unverified or older than 2025 (need the 'latest rule wins' check)
old_docs = df[df["doc_year"] < 2025]
print(f"Fact 3 - {len(old_docs)} records come from documents before 2025 and {int((~df['verified']).sum())} are not yet verified:")
print(old_docs[["id", "item_or_topic", "effective_from"]].to_string(index=False))
