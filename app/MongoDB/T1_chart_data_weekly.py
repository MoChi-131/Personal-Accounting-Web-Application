from pymongo import MongoClient
from datetime import datetime, timedelta

def retrieve_expense_data_weekly(current_date, categories):
    # Get Sunday of current week (start of week)
    start_date = current_date - timedelta(days=current_date.weekday())  # Sunday
    end_date = start_date + timedelta(days=6)  # Saturday

    # Initialize labels for Sunday to Saturday
    days_of_week = [start_date + timedelta(days=i) for i in range(7)]  # List from Sunday to Saturday
    week_labels = [day.strftime('%a') for day in days_of_week]  

    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Personal_Accounting"]
    collection = db["Full_Detail"]

    # Initialize category data for each day of the week
    category_data = {category: [0] * 7 for category in categories}  # One slot for each day of the week

    # Aggregation pipeline for this week only
    pipeline = [
                {
                    "$match": {
                        "Category": {"$in": categories},
                        "Date": {
                            "$gte": start_date.strftime('%Y-%m-%d'),
                            "$lte": end_date.strftime('%Y-%m-%d')
                        }
                    }
                },
                {
                    "$addFields": {
                        "parsed_date": {
                            "$dateFromString": {"dateString": "$Date"}
                        }
                    }
                },
                {
                    "$addFields": {
                        "day_of_week": {
                            "$dayOfWeek": "$parsed_date"
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "category": "$Category",
                            "day_of_week": "$day_of_week"
                        },
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

    results = collection.aggregate(pipeline)

    for result in results:
        category = result['_id']['category']
        day_of_week = result['_id']['day_of_week']  # Day of the week (1=Sunday, 7=Saturday)
        total_amount = round(result['total_amount'], 2)

        # Place data into the correct day index (0 for Sunday, 6 for Saturday)
        category_data[category][day_of_week - 1] = total_amount

    # Stack totals per day of the week
    stack_totals = [round(sum(category_data[cat][i] for cat in categories), 2) for i in range(7)]

    client.close()

    return {
        'category_data': category_data,
        'categories': categories,
        'week_labels': week_labels,  # Sunday to Saturday labels
        'stack_totals': stack_totals,
        'start_date': start_date,
        'end_date': end_date
    }