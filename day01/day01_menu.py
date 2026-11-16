"""Day 1: while-loop menu for GSTSaral."""

SAMPLE_QUESTIONS = [
    "What is the GST rate on toilet soap now?",
    "Is paneer still taxed after September 2025?",
    "Up to what turnover can I use the composition scheme?",
    "What is the CGST + SGST split for a Rs 1,000 sale at 5% inside Maharashtra?",
]


def about():
    print("\nGSTSaral helps small shopkeepers understand GST in plain language,")
    print("using the GST Council FAQs and the 56th Council press release (3 Sep 2025).")


def sample_questions():
    print("\nSample questions:")
    for i, q in enumerate(SAMPLE_QUESTIONS, start=1):
        print(f"  {i}. {q}")


def rule_check():
    """One if/elif rule check: composition scheme eligibility for a goods trader."""
    raw = input("\nYearly turnover in lakh rupees (goods trader): ").strip()
    try:
        turnover = float(raw)
    except ValueError:
        print("Please enter a number, for example 90.")
        return

    if turnover <= 0:
        print("Turnover must be more than zero.")
    elif turnover <= 75:
        print("Eligible. Within both the old 2017-18 limit (Rs 75 lakh) and the current limit.")
    elif turnover <= 150:
        print("Eligible under the current limit (Rs 1.5 crore).")
        print("Warning: an old 2017-18 FAQ says Rs 75 lakh. The newer rule wins.")
    else:
        print("Not eligible for the composition scheme (above Rs 1.5 crore).")
    print("(Learning example. Confirm on the official GST portal.)")


def main():
    while True:
        print("\n--- GSTSaral menu ---")
        print("1. About GSTSaral")
        print("2. Sample questions")
        print("3. Composition scheme rule check")
        print("0. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            about()
        elif choice == "2":
            sample_questions()
        elif choice == "3":
            rule_check()
        elif choice == "0":
            print("Dhanyavaad! Goodbye.")
            break
        else:
            print("Invalid choice. Enter 0, 1, 2 or 3.")


if __name__ == "__main__":
    main()
