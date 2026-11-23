from pathlib import Path
from app.exports import records_csv

output = Path("data/processed/gstsaral_records_export.csv")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(records_csv(), encoding="utf-8-sig")
print(f"CSV exported to {output}")
