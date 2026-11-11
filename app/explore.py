"""Day 4 S2 - 3 facts about GSTSaral records with pandas.

Run from inside the day04 folder:  python analysis/explore.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.records import load_records  # noqa: E402


def to_percent(rule):
    """'GST 18%' -> 18.0 ; 'NIL (exempt)' -> 0.0 ; anything else -> NaN."""
    text = str(rule).upper()
    if "NIL" in text or "EXEMPT" in text:
        return 0.0
    digits = "".join(c for c in text.split("%")[0].split()[-1] if c.isdigit() or c == ".") \
        if "%" in text else ""
    return float(digits) if digits else float("nan")


def main():
    df = pd.DataFrame(load_records())
    if df.empty:
        print("No records found - run day03 ingest first.")
        return
    df["old_pct"] = df["old_rule"].map(to_percent)
    df["new_pct"] = df["new_rule"].map(to_percent)
    rated = df.dropna(subset=["old_pct", "new_pct"]).copy()
    rated["cut"] = rated["old_pct"] - rated["new_pct"]

    print(f"Records: {len(df)}  |  with clear old/new % rates: {len(rated)}\n")

    top = rated.loc[rated["cut"].idxmax()]
    print(f"Fact 1: Biggest cut is '{top['item_or_topic']}': "
          f"{top['old_pct']:.0f}% -> {top['new_pct']:.0f}% ({top['cut']:.0f} points).")

    exempt = rated[rated["new_pct"] == 0]
    print(f"Fact 2: {len(exempt)} of {len(rated)} items became NIL/exempt, e.g. "
          f"{', '.join(exempt['item_or_topic'].head(3))}.")

    by_cat = rated.groupby("category")["cut"].mean().sort_values(ascending=False)
    print(f"Fact 3: Category with the biggest average cut: '{by_cat.index[0]}' "
          f"({by_cat.iloc[0]:.1f} points). Most common new rate: "
          f"{rated['new_pct'].mode().iloc[0]:.0f}%.")


if __name__ == "__main__":
    main()
