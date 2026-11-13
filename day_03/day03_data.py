import json
from pathlib import Path

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# JSON dataset location
DATA_FILE = BASE_DIR / "data" / "gst_faq.json"


# Function to load GST data
def load_gst_data():

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


# Function to display all questions
def display_questions(data):

    print("\n===== GST FAQ DATASET =====")

    for item in data:
        print(f"\nID: {item['id']}")
        print(f"Category: {item['category']}")
        print(f"Question: {item['question']}")
        print(f"Answer: {item['answer']}")


# Function to search questions
def search_question(data, keyword):

    results = []

    for item in data:

        question = item["question"].lower()
        answer = item["answer"].lower()
        category = item["category"].lower()

        if (keyword.lower() in question
                or keyword.lower() in answer
                or keyword.lower() in category):

            results.append(item)

    return results


# Main program
if __name__ == "__main__":

    gst_data = load_gst_data()

    print("Welcome to GSTSaral")
    print("Total GST Records:", len(gst_data))

    display_questions(gst_data)

    print("\n===== SEARCH GST INFORMATION =====")

    keyword = input("Enter GST keyword: ")

    results = search_question(gst_data, keyword)

    if results:

        for item in results:
            print("\nQuestion:", item["question"])
            print("Answer:", item["answer"])
            print("Source:", item["source"])
            print("Source URL:", item["source_url"])

    else:
        print("\nNo matching information found.")

    print("\nDay 03 Completed!")
