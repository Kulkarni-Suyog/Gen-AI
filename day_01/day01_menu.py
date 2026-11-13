while True:

    print("\n========== GSTSARAL MENU ==========")
    print("1. About GSTSaral")
    print("2. Sample GST Questions")
    print("3. GST Domain Rule Check")
    print("0. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        print("\nGSTSaral is a Generative AI GST Assistant.")
        print("It helps users understand GST information.")

    elif choice == "2":

        print("\nSample GST Questions:")
        print("1. What is GST?")
        print("2. What is the difference between CGST and SGST?")
        print("3. What is an Input Tax Credit (ITC)?")

    elif choice == "3":

        print("\nBasic GST Domain Rule Check")

        question = input("Enter your GST question: ")

        if "gst" in question.lower():
            print("Your question is related to GST.")
        else:
            print("Your question may not be GST-related.")

    elif choice == "0":

        print("\nThank you for using GSTSaral!")
        print("Exiting the application...")
        break

    else:

        print("\nInvalid choice! Please try again.")
