from pymongo import MongoClient

def Out_monthly(date):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]  
    collection = db["Full_Detail"]  

    # Define Aggregation Pipeline
    pipeline = [
            {
            "$match": {
                "Date": { "$regex": date } 
            }
        },
        {
            "$group": {
                "_id": None,
                "total_amount": {
                            "$sum": {
                                "$add": [
                                    {"$ifNull": ["$Money Out", 0]},
                                    {"$ifNull": ["$Total Amount", 0]}
                                ]
                            }
                        }
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
    else: 
        total = result[0]["total_amount"]

    return total
        
