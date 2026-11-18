
project_name = "GSTSaral"
product = "Simple GST Assistance Application"
target_user = "Small Business Owners and GST Taxpayers"

problem = (
    "Understanding GST rules, tax calculations, "
    "and GST procedures can be difficult for beginners."
)

data_source = "Official GST Portal (https://www.gst.gov.in/)"

# Display project card
print("=" * 50)
print("             WELCOME TO GSTSARAL")
print("=" * 50)

print(f"Project Name : {project_name}")

print(f"Product      : {product}")
print(f"Target Users : {target_user}")
print(f"Problem      : {problem}")
print(f"Data Source  : {data_source}")

print("=" * 50)

# Get user information
user_name = input("\nEnter your name: ")
question = input("Enter your GST-related question: ")

# Display user details
print("\nThank you for using GSTSaral!")
print(f"Hello, {user_name}!")
print(f"Your question is: {question}")
print("\nGSTSaral is here to help you understand GST.")
