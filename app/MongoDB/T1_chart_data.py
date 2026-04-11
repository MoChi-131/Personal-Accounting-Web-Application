from pymongo import MongoClient
from datetime import datetime
from dateutil.relativedelta import relativedelta

def retrieve_expense_monthly_data(current_date, categories):        
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]
    collection = db["Full_Detail"]

    # Calculate date range
    end_date = current_date.replace(day=1) + relativedelta(months=1, days=-1)  # Last day of current month
    start_date = current_date.replace(day=1) - relativedelta(months=3)  # First day of 3 months ago

    # Generate month labels and keys
    months = []
    month_keys = []
    current = start_date
    while current <= end_date:
        month_keys.append(current.strftime('%Y-%m'))
        months.append(current.strftime('%b'))  # Short month name (e.g., Jan, Feb)
        current += relativedelta(months=1)

    # Initialize data structures for all categories
    category_data = {category: [0] * 4 for category in categories}

    # Aggregation pipeline
    pipeline = [
        {
            "$match": {
                "Date": {
                    "$gte": start_date.strftime('%Y-%m-%d'),
                    "$lte": end_date.strftime('%Y-%m-%d')
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "category": "$Category",
                    "year_month": {
                        "$substr": ["$Date", 0, 7]  # Extract YYYY-MM
                    }
                },
                "total_amount": {
                    "$sum": {
                        "$add": [
                            {"$ifNull": ["$Money Out", 0]},
                            {"$ifNull": ["$Total Amount", 0]}
                        ]}
                    }

            }
        }
    ]

    # Execute pipeline
    results = collection.aggregate(pipeline)

    # Process results
    for result in results:
        category = result['_id']['category']
        year_month = result['_id']['year_month']
        total_amount = result['total_amount']
        print(category, year_month, total_amount)
        
        # Find month index
        if year_month in month_keys:
            month_idx = month_keys.index(year_month)
            category_data[category][month_idx] = total_amount

    # Round amounts to 2 decimal places
    for category in category_data:
        category_data[category] = [round(x, 2) for x in category_data[category]]

    # Calculate total amount for each month
    stack_totals = [0] * 4
    for category in categories:
        for i in range(4):
            stack_totals[i] += category_data[category][i]
    stack_totals = [round(x, 2) for x in stack_totals]

    # Close MongoDB connection
    client.close()

    # Return data
    return {
        'category_data': category_data,
        'categories': categories,
        'months': months,
        'month_keys': month_keys,
        'stack_totals': stack_totals,
        'start_date': start_date,
        'end_date': end_date
    }