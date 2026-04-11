from pymongo import MongoClient

def Reciept_Link_BS():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]  # Your database
    collection = db["Receipt_Full_Detail"]  # Replace with your collection

    pipeline = [
        {
            "$lookup": {
                "from": "Bank_Statement",
                "localField": "Supplier Name",
                "foreignField": "Description",
                "as": "Bank Statement"
            }
        },
        {
            "$match": {
                "Bank Statement": {
                    "$size": 0
                }
            }
        },
        {
            "$merge": {
                "into": {
                    "db": "Personal_Accounting",
                    "coll": "Full_Detail"
                },
                "whenMatched": "merge",
                "whenNotMatched": "insert"
            }
        }
    ]

    print("All reciepts saved in Full_Detail")
    
    return collection.aggregate(pipeline)