from faker import Faker
import random
import datetime
import json
from bson import ObjectId  # Importing ObjectId from bson

fake = Faker()

# Categories for the generated data
categories = ["toll", "food", "parking", "transport", "shopping", "telecom", "miscellaneous"]

# Generate fake data
fake_data = []

for _ in range(10):  # Adjust the number of records here
    category = random.choice(categories)
    
    data = {
        "_id": {"$oid": str(ObjectId())},  # Generate a valid ObjectId
        "Supplier Name": fake.company(),
        "Receipt Number": random.randint(1000000, 9999999),
        "Date": datetime.date(2025, 2, random.randint(1, 28)).strftime("%Y-%m-%d"),
        "Time": fake.time(),
        "Category": category.lower(),
        "Document Type": "EXPENSE RECEIPT",
        "Supplier Address": fake.address(),
        "Supplier Phone Number": fake.phone_number(),
        "Locale": "en-US",
        "Total Amount": round(random.uniform(10.00, 80.00), 2),
        "Total Net": round(random.uniform(10.00, 500.00), 2),
        "Total Tax": round(random.uniform(0.00, 20.00), 2),
        "Tip and Gratuity": random.choice([None, round(random.uniform(1.00, 20.00), 2)]),
        #"items": [
        #    {
        #        "_id": {"$oid": str(ObjectId())},  # Generate a valid ObjectId
        #       "Description": fake.bs(),
        #        "Quantity": random.randint(1, 5),
        #        "Unit Price": round(random.uniform(5.00, 150.00), 2),
        #        "Total Price": round(random.uniform(10.00, 500.00), 2)
        #    }
        #]
    }
    
    fake_data.append(data)

# Save the generated data as a JSON file
output_file = 'fake_expense_data.json'
with open(output_file, 'w') as json_file:
    json.dump(fake_data, json_file, indent=4)

print(f"Data saved to {output_file}")
