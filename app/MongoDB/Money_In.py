from pymongo import MongoClient

def agg_money_in():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]  # database
    collection = db["Bank_Statement"]  # collection

    # Define Aggregation Pipeline
    pipeline = [
        {"$match": {"Money Out": 0}},  # Filter transactions with Money In = 0
        {"$sort": {"Date": 1}},  # Sort by Date in ascending order
        {"$out": "Money_In"}  # Output to a new collection
    ]

    # Execute Aggregation
    collection.aggregate(pipeline)

    print("Aggregation completed. Data saved in 'Money_In' collection.")

    return

