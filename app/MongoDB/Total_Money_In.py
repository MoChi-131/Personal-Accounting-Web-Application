from pymongo import MongoClient

def In_monthly(date):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"] 
    collection = db["Money_In"]  

    # Define Aggregation Pipeline
    pipeline = [
            {
            "$match": {
                "Date": { "$regex": date }  # Match dates starting with "2025-01-"
            }
        },
        {
            "$group": {
                "_id": None,
                "Total": {"$sum": "$Money In"},
            }
        },
        {
            "$project": {"_id": 0}
        }
    ]

    # Execute Aggregation
    result = list(collection.aggregate(pipeline))

    if not result:
            return 0  # If no documents matched, return 0

    return result[0]["Total"]  # Just return the total number
        
