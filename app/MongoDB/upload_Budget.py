from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["Personal_Accounting"] 
collection = db["Budget"] 

def upload_Budget(file_path):
    
    with open(file_path, "r") as file:
        file_data = json.load(file)
        
    collection.insert_one(file_data)
    
    print("Budget is uploaded")
    
    return

def update_Budget(date, new_budget, file_path):
    from .write_Budget import write_Budget       
    write_Budget(date, new_budget,file_path)
    
    with open(file_path, "r") as file:
        file_data = json.load(file)
    

    new = file_data["categories"]
    
    collection.delete_one({"month": date})
    
    collection.update_one(
            {"month": date}, 
            {"$set" :{"categories" : new}}    
        )
    return 
    