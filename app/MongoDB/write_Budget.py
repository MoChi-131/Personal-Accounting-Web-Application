import json
import os
from .upload_Budget import upload_Budget

def write_Budget(date, budget, output_path):
    
    budget_dict = {
    "Wadge": 0,
    "Other_Income": 0,
    "Toll": 0,
    "Food": 0,
    "Parking": 0,
    "Transport": 0,
    "Accommodation": 0,
    "Shopping": 0,
    "Telecom": 0,
    "Miscellaneous": 0,
    "Other": 0,
    "Saving": 0}
    
    i = 0
    for category in budget_dict.keys():
        budget_dict[category] = budget[i]
        i = i +1
    
    content = {
    "month": date,
    "categories":budget_dict
    }
        
    with open(output_path, "w") as file:
        json.dump(content, file, indent=4)
        
    upload_Budget(output_path)
    
    return