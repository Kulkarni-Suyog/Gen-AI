product = "GSTSaral"
gst_rate = 18
price = 1000
is_active = True

print("PRODUCT:", product)
print("GST Rate:", gst_rate)
print("Price:", price)
print("Active:", is_active)


# 2. Conditional Statements

print("\n--- GST Eligibility Check ---")

amount = 1000

if amount > 0:
    print("Valid transaction amount")
else:
    print("Invalid transaction amount")


# 3. For Loop

print("\n--- GST Rates ---")

gst_rates = [5, 12, 18, 28]

for rate in gst_rates:
    print("GST Rate:", rate, "%")


# 4. Functions

def calculate_gst(price, rate):

    gst = price * rate / 100
    total = price + gst

    return gst, total


gst_amount, total_amount = calculate_gst(1000, 18)

print("\n--- GST Calculation ---")
print("GST Amount:", gst_amount)
print("Total Amount:", total_amount)


# 5. Lists

products = ["Laptop", "Mobile", "Keyboard"]

print("\n--- Product List ---")

for item in products:
    print(item)


# 6. Dictionaries

product_details = {
    "name": "Laptop",
    "price": 50000,
    "gst_rate": 18
}

print("\n--- Product Details ---")
print("Name:", product_details["name"])
print("Price:", product_details["price"])
print("GST:", product_details["gst_rate"])


# 7. User Input

print("\n--- User GST Calculator ---")

user_price = float(input("Enter product price: "))
user_rate = float(input("Enter GST rate: "))

gst, total = calculate_gst(user_price, user_rate)

print("GST Amount:", gst)
print("Final Price:", total)

print("\nDay 02 Completed!")
