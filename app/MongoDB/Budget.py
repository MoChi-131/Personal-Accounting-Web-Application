from pymongo import MongoClient

def budget_data(date):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]  
    collection = db["Budget"]  

    # Define Aggregation Pipeline
    pipeline = [
            {
            "$match": {
                "month": { "$regex": date } 
            }
        },
        {
            "$project": {"_id": 0}
        }
    ]

    # Execute Aggregation
    result = list(collection.aggregate(pipeline))

    if not result:
            return 0  

    return result[0]["categories"]  

if __name__ == "__main__":
    print(budget_data("2025-02"))
        
