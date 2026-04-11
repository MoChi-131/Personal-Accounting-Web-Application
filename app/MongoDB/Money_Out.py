from pymongo import MongoClient

def agg_money_out():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]  # Your database
    collection = db["Bank_Statement"]  # Replace with your collection

    # Define Aggregation Pipeline
    pipeline = [
        {"$match": {"Money In": 0}},  # Filter transactions with Money In = 0
        {"$sort": {"Date": 1}},  # Sort by Date in ascending order
        {"$out": "Money_Out"}  # Output to a new collection
    ]

    # Execute Aggregation
    collection.aggregate(pipeline)

    print("Aggregation completed. Data saved in 'Money_Out' collection.")
    
    return
