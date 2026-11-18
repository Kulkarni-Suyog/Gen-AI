"""Command-line interface for GSTSaral Day 2."""

from app.records import load_records, search, count_by, get_by_id


def print_record(record):
    """Display one record in a readable format."""
    print("\n" + "-" * 72)
    print(f"ID            : {record['id']}")
    print(f"Category      : {record['category']}")
    print(f"Item / Topic  : {record['item_or_topic']}")
    print(f"Old rule      : {record['old_rule']}")
    print(f"New rule      : {record['new_rule']}")
    print(f"Effective from: {record['effective_from']}")
    print(f"Document      : {record['document']}")
    print(f"Source URL    : {record['source_url']}")
    print("-" * 72)


def main():
    records = load_records()
    print(f"GSTSaral Day 2 loaded {len(records)} sample records.")

    while True:
        print("\n========== GSTSARAL DAY 2 ==========")
        print("1. Print all records")
        print("2. Search records by keyword")
        print("3. Count records by category")
        print("4. Find a record by ID")
        print("0. Exit")
        print("====================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            for record in records:
                print_record(record)

        elif choice == "2":
            keyword = input("Enter a keyword (e.g. soap, notebook, 5%): ")
            results = search(records, keyword)
            print(f"\nFound {len(results)} matching record(s).")
            for record in results:
                print_record(record)

        elif choice == "3":
            print("\nRecord count by category:")
            for category, total in count_by(records).items():
                print(f"- {category}: {total}")

        elif choice == "4":
            record_id = input("Enter record ID (e.g. shampoo): ")
            record = get_by_id(records, record_id)
            if record:
                print_record(record)
            else:
                print("No record found with that ID.")

        elif choice == "0":
            print("Thank you for using GSTSaral. Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3, 4 or 0.")


if __name__ == "__main__":
    main()
