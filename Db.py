from pymongo import MongoClient
import os
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

# Choose a database
db = client["flaskdb"]

# Choose a collection
collection = db["calenderTokens"]


def add_tokens(credentials):
    collection.insert_one(credentials)
    print("details stored")
    return "Succesfully Connected to Calendar"

def get_db():
    return collection