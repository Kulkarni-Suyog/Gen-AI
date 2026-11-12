"""Day 1: print the GSTSaral project card using variables and f-strings."""

product = "GSTSaral"
tagline = "GST made simple for small Indian shopkeepers"
user = "Small shop owner / kirana trader in India"
problem = (
    "GST FAQs and press releases are long, and old 2017-18 rules sit next to "
    "2025-26 changes, so a shopkeeper cannot tell which rule is current."
)
data_source = "GST Council FAQ + 56th Council press release (PIB, 3 Sep 2025)"
source_url = "https://gstcouncil.gov.in/en/faq"

print("=" * 60)
print(f"{product}: {tagline}")
print("=" * 60)
print(f"Product     : {product}")
print(f"User        : {user}")
print(f"Problem     : {problem}")
print(f"Data source : {data_source}")
print(f"URL         : {source_url}")
print("-" * 60)

name = input("What is your name? ").strip()
question = input("What is your GST question? ").strip()

print()
print(f"Namaste {name}!")
print(f"You asked: '{question}'")
print(f"({len(question)} characters). {product} will answer questions like this from official sources soon.")
