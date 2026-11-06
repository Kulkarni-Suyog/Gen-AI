while True:
    print("GSTSaral menu for the Users")
    print("1.About GStSaral")
    print("2. samole Questions")
    print("3. GST rules to check")
    print("0.exit")


    choice=input("enter your choice of number:")
    if choice =="git status
git add day01_intro.py
git commit -m "Add day01 intro Python file"
git push origin main":
        print("GSTSaral is platform where you can find or read the upadtes of the rules and regulations of the gst also finding the tax which as per the product how much it will taking.")

    elif choice =="2":
        print("\n sample gst questions are:")
        print("1. What is GST?")
        print("2. What is the GST rate for a specific product?")
        print("3. How to file GST returns?")
    elif choice =="3":
       turnover = float(input("Enter your turnover:"))

       if turnover <=100000:
           print("you are within the geneeral ")
           print("you are eligile for the small business schemes.")
       else:
              print("you are not eligible for the small business schemes.")
    elif choice =="0":
        print("Thank you for using GSTSaral. Goodbye!")
    else:
        print("enter the valid choice.")          