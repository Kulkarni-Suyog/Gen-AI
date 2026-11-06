
from data.sample_records import records


def load_records():
    return records


def search(keyword):
    keyword = keyword.lower()
    results = []

    for record in records:
        text = " ".join(str(v) for v in record.values()).lower()

        if keyword in text:
            results.append(record)

    return results


def count_by(field):
    counts = {}

    for record in records:
        value = record.get(field)

        if value is not None:
            counts[value] = counts.get(value, 0) + 1

    return counts


def get_by_id(record_id):
    for record in records:
        if record["id"] == record_id:
            return record

    return None
