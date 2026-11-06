
# GSTSaral - Day 02: Sample GST Records

SOURCE_URL = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2163555"
DOCUMENT = "56th GST Council Press Release - 03 September 2025"
EFFECTIVE_DATE = "2025-09-22"

records = [
    {
        "item_or_topic": "UHT milk",
        "category": "Dairy",
        "old_rule": "5% GST",
        "new_rule": "0% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Condensed milk",
        "category": "Dairy",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Butter and ghee",
        "category": "Dairy",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Cheese",
        "category": "Dairy",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Pre-packaged paneer",
        "category": "Dairy",
        "old_rule": "5% GST",
        "new_rule": "0% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Almonds",
        "category": "Food",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Dates",
        "category": "Food",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Pasta",
        "category": "Food",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Cornflakes",
        "category": "Food",
        "old_rule": "18% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Chocolates",
        "category": "Food",
        "old_rule": "18% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Packaged namkeens",
        "category": "Food",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Drinking water in 20-litre bottles",
        "category": "Beverages",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Hair oil and shampoo",
        "category": "Personal Care",
        "old_rule": "18% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Toothpaste",
        "category": "Personal Care",
        "old_rule": "18% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Toilet soap bars",
        "category": "Personal Care",
        "old_rule": "18% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Toothbrushes",
        "category": "Personal Care",
        "old_rule": "18% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Bicycles",
        "category": "Transport",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Exercise books and notebooks",
        "category": "Stationery",
        "old_rule": "12% GST",
        "new_rule": "0% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Pencils",
        "category": "Stationery",
        "old_rule": "12% GST",
        "new_rule": "0% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    },
    {
        "item_or_topic": "Geometry boxes",
        "category": "Stationery",
        "old_rule": "12% GST",
        "new_rule": "5% GST",
        "effective_from": EFFECTIVE_DATE,
        "document": DOCUMENT,
        "source_url": SOURCE_URL
    }
]

# 1. Print all records
print("========== ALL GST RECORDS ==========")

for record in records:
    print(record)

# 2. Search records by keyword
keyword = input("\nEnter product name to search: ").lower()

print("\n========== SEARCH RESULTS ==========")

for record in records:
    if keyword in record["item_or_topic"].lower():
        print(record)

# 3. Count records per category
print("\n========== CATEGORY COUNTS ==========")

category_count = {}

for record in records:
    category = record["category"]
    category_count[category] = category_count.get(category, 0) + 1

for category, count in category_count.items():
    print(f"{category}: {count}")
