from pymongo import MongoClient

def fetch_category_data(date, categories):
    data = []

    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]
    collection = db["Full_Detail"]

    for category in categories:
        pipeline = [
            {
                "$match": {
                    "Category": category,
                    "Date": {
                        "$regex": date
                    }
                }
            },
            {
                "$group": {
                    "_id": "$Category",
                    "total_amount": {
                            "$sum": {
                                "$add": [
                                    {"$ifNull": ["$Money Out", 0]},
                                    {"$ifNull": ["$Total Amount", 0]}
                                ]
                            }
                        }
                }
            }
        ]

        result = list(collection.aggregate(pipeline))
        amount = result[0]["total_amount"] if result else 0
        data.append(amount)
    return data, categories
