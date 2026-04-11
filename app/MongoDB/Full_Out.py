from pymongo import MongoClient

def Full_Out():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]  # Your database
    collection = db["Money_Out"]  # Replace with your collection

    pipeline = [
        {
            "$lookup": {
                "from": "Receipt_Full_Detail",
                "let": {
                    "desc": "$Description",
                    "money_out": "$Money Out"
                },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {
                                        "$regexMatch": {
                                            "input": "$Supplier Name",
                                            "regex": { "$concat": [".*", { "$trim": { "input": "$$desc" } }, ".*"] },
                                            "options": "i"
                                        }
                                    },
                                    {
                                        "$eq": ["$Total Amount", "$$money_out"]
                                    }
                                ]
                            }
                        }
                    }
                ],
                "as": "Receipt"
            }
        },
        {
            "$addFields": {
                "Category": {
                    "$cond": {
                        "if": {"$gt": [{"$size": "$Receipt"}, 0]},
                        "then": {"$arrayElemAt": ["$Receipt.Category", 0]},
                        "else": "other"
                    }
                }
            }
        },
        {
            "$out": {
                "db": "Personal_Accounting",
                "coll": "Full_Detail"
            }
        }
    ]
    
    print("Saved in Full_Detail")
    
    return collection.aggregate(pipeline)