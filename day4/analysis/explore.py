"""Print three simple facts about the GSTSaral dataset using pandas."""
from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "records.json"


def main() -> None:
    df = pd.read_json(DATA_FILE)
    print("GSTSaral Dataset Exploration")
    print("=" * 32)

    print(f"Fact 1: The dataset contains {len(df)} GST rate-change records.")

    dates = pd.to_datetime(df["effective_from"], errors="coerce")
    valid_dates = dates.dropna()
    if not valid_dates.empty:
        print(f"Fact 2: The effective date covered is {valid_dates.min().date()}.")
    else:
        print("Fact 2: No valid effective dates were found.")

    most_common_new_rule = df["new_rule"].value_counts().idxmax()
    count = int(df["new_rule"].value_counts().max())
    print(f"Fact 3: The most common new GST treatment is '{most_common_new_rule}' ({count} records).")


if __name__ == "__main__":
    main()
