import pandas as pd
import pymongo
import os


# Function to load CSV into MongoDB
def load_csv_to_mongo(csv_file, collection_name):
    # MongoDB Connection
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Change to your MongoDB URI
    db = client["Personal_Accounting"] # Database Name
    
    # Load CSV into DataFrame
    df = pd.read_csv(csv_file)

    # Convert DataFrame to Dictionary for MongoDB
    records = df.to_dict(orient="records")

    # Get collection and insert data
    collection = db[collection_name]
    collection.insert_many(records)

    print(f"Data from {csv_file} successfully inserted into {collection_name}!")

def Upload_Reciept():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Insert data into Raw_Data_Details collection
    load_csv_to_mongo(os.path.join(current_dir, "Receipt_Detail.csv"), 'Receipt')

    # Insert data into Raw_Data_Items collection
    load_csv_to_mongo(os.path.join(current_dir, "Receipt_Items.csv"), 'Receipt_Items')
