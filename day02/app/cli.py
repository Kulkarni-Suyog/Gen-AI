"""Command-line interface for GSTSaral records.

Run from the day02 folder:
    python -m app.cli list
    python -m app.cli search soap
    python -m app.cli count
    python -m app.cli get 7
"""

import argparse

from app.records import count_by, get_by_id, load_records, search


def show(r):
    print(f"[{r['id']:>2}] {r['item_or_topic']} ({r['category']})")
    print(f"     {r['old_rule']}  ->  {r['new_rule']}   effective {r['effective_from']}")
    print(f"     {r['document']}")


def main():
    parser = argparse.ArgumentParser(description="GSTSaral records")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="print all records")
    p_search = sub.add_parser("search", help="search by keyword")
    p_search.add_argument("keyword")
    p_count = sub.add_parser("count", help="count records per field")
    p_count.add_argument("--field", default="category")
    p_get = sub.add_parser("get", help="show one record by id")
    p_get.add_argument("id", type=int)
    args = parser.parse_args()

    if args.cmd == "list":
        records = load_records()
        for r in records:
            show(r)
        print(f"\nTotal: {len(records)} records")
    elif args.cmd == "search":
        hits = search(args.keyword)
        for r in hits:
            show(r)
        print(f"\n{len(hits)} match(es) for '{args.keyword}'")
    elif args.cmd == "count":
        for value, n in sorted(count_by(args.field).items()):
            print(f"{value:<22} {n}")
    elif args.cmd == "get":
        r = get_by_id(args.id)
        if r is None:
            print(f"No record with id {args.id}")
        else:
            show(r)


if __name__ == "__main__":
    main()
