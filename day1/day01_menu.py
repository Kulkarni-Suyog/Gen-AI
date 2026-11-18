# GSTSaral - Day 01 Menu Driven Application

while True:
    print("\n========== GSTSARAL MENU ==========")
    print("1. About GSTSaral")
    print("2. Sample GST Questions")
    print("3. GST Rule Check")
    print("0. Exit")
    print("===================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n--- About GSTSaral ---")
        print("GSTSaral is a simple GST assistance application.")
        print("It helps small business owners understand GST.")
        print("It provides basic GST information and guidance.")

    elif choice == "2":
        print("\n--- Sample GST Questions ---")
        print("1. What is GST?")
        print("2. What is CGST?")
        print("3. What is SGST?")
        print("4. What is IGST?")
        print("5. What is a GSTIN?")

    elif choice == "3":
        print("\n--- GST Rule Check ---")
        transaction = input(
            "Is the transaction within the same state? (yes/no): "
        ).lower()

        if transaction == "yes":
            print("Applicable taxes: CGST + SGST")

        elif transaction == "no":
            print("Applicable tax: IGST")

        else:
            print("Invalid input! Please enter yes or no.")

    elif choice == "0":
        print("\nThank you for using GSTSaral!")
        print("Exiting application...")
        break

    else:
        print("\nInvalid choice! Please select 1, 2, 3 or 0.")
