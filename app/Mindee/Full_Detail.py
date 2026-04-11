from pymongo import MongoClient

def Embed_Reciept():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]  # Your database
    collection = db["Receipt"]  # Replace with your collection

    # Define Aggregation Pipeline
    pipeline = [
        {
            "$lookup": {
                "from": "Receipt_Items",  # Collection to join
                "let": {  # Define local variables to use in the sub-pipeline
                    "date": "$Date",
                    "supplier_name": "$Supplier Name"
                },
                "pipeline": [
                    {
                        "$match": {  # Match documents where both Receipt Number and Supplier Name are equal
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$Date", "$$date"]},
                                    {"$eq": ["$Supplier Name", "$$supplier_name"]}
                                ]
                            }
                        }
                    },
                    {
                        "$project": {  # Include Receipt Number in the output, while excluding other unnecessary fields
                            "Receipt Number": 0,  # Include Receipt Number
                            "Supplier Name": 0,  # Include Supplier Name if needed
                        }
                    }
                ],
                "as": "items"  # Name for the array field where the matched documents will be stored
            }
        },
        {
            "$out": "Receipt_Full_Detail"  # Output the result to the Full_Detail collection
        }
    ]

    # Execute the aggregation
    collection.aggregate(pipeline)

    print("Aggregation complete and result saved to Full_Detail collection.")

