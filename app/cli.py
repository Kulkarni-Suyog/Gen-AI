
import argparse
from pprint import pprint

from app.records import (
    load_records,
    search,
    count_by,
    get_by_id
)


def main():

    parser = argparse.ArgumentParser(
        description="GST Council Records Application"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    subparsers.add_parser("list")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("keyword")

    count_parser = subparsers.add_parser("count")
    count_parser.add_argument("--by", default="category")

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "list":
        pprint(load_records(), sort_dicts=False)

    elif args.command == "search":
        results = search(args.keyword)
        pprint(results, sort_dicts=False)
        print("Records Found:", len(results))

    elif args.command == "count":
        pprint(count_by(args.by))

    elif args.command == "get":
        result = get_by_id(args.id)

        if result:
            pprint(result, sort_dicts=False)
        else:
            print("Record not found!")


if __name__ == "__main__":
    main()
