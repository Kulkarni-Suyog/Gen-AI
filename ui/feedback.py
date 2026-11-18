import json
from pathlib import Path
from datetime import datetime, timezone

# --------------------------------------------------
# FILE LOCATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

FEEDBACK_FILE = (
    BASE_DIR
    / "ui"
    / "feedback.jsonl"
)

# --------------------------------------------------
# SAVE FEEDBACK
# --------------------------------------------------

def save_feedback(
    question,
    answer,
    rating,
    endpoint,
):

    # Create UI folder if not present.

    FEEDBACK_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Feedback entry.

    entry = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "question": question,

        "answer": answer,

        "rating": rating,

        "endpoint": endpoint,
    }

    # Append feedback to JSONL file.

    with open(
        FEEDBACK_FILE,
        "a",
        encoding="utf-8",
    ) as file:

        file.write(
            json.dumps(
                entry,
                ensure_ascii=False,
            )
            + "\n"
        )

    print(
        "Feedback saved successfully!"
    )