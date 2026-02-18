from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

# Read environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "pythondb")

# Mongo connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["items"]

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/items")
def create_item():
    item = {
        "name": "Python Service",
        "createdAt": datetime.utcnow()
    }
    result = collection.insert_one(item)
    item["_id"] = str(result.inserted_id)
    return item

@app.get("/items")
def get_items():
    items = []
    for doc in collection.find():
        doc["_id"] = str(doc["_id"])
        items.append(doc)
    return items
