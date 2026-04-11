from pymongo import MongoClient
from datetime import datetime
from dateutil.relativedelta import relativedelta

def retrieve_expense_data(current_date, categories):        
    # Calculate date range for last month
    last_month_end = current_date.replace(day=1) - relativedelta(days=1)  # Last day of last month
    last_month_start = last_month_end.replace(day=1)  # First day of last month
    
    # Initialize category totals
    category_totals = {category: 0.0 for category in categories}
    
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["Personal_Accounting"]
        collection = db["Full_Detail"]
        
        # Aggregation pipeline for last month
        pipeline = [
            {
                "$match": {
                    "Date": {
                        "$gte": last_month_start.strftime('%Y-%m-%d'),
                        "$lte": last_month_end.strftime('%Y-%m-%d')
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
        
        # Execute pipeline
        results = collection.aggregate(pipeline)
        
        # Process results
        for result in results:
            category = result['_id']
            category_totals[category] = round(result['total_amount'], 2)
        
        # Close MongoDB connection
        client.close()
        
    except Exception as e:
        print(f"Error connecting to MongoDB or processing data: {e}")
        return None
    
    # Return data
    # Convert category totals to ordered list
    data = [category_totals[category] for category in categories]
    print(data)
    return data
    
if __name__== "__main__":
    categories = ["Toll", "Food", "Parking", "Transport", "Accommodation", "Gasoline", "Telecom", "Miscellaneous", "Other"]
    print(retrieve_expense_data(datetime.now(), categories))