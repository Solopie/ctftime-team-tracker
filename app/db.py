import pymongo
from config import MONGODB_URL, DATABASE_NAME

def connect():
    client = pymongo.MongoClient(MONGODB_URL, connect=False)
    return client[DATABASE_NAME]

def get_db_data():
    c = connect()
    collection_names = c.list_collection_names()
    if "team" not in collection_names or "aim" not in collection_names:
        return {}

    return {"team": c.team.find_one({}, {"_id": False}), "aim": c.aim.find_one({}, {"_id": False})}

def update_db(data):
    c = connect()
    collection_names = c.list_collection_names()
    if "team" not in collection_names:
        c["team"].insert_one(data["team"])
    else:
        c.team.replace_one({}, data["team"])

    if "aim" not in collection_names:    
        c["aim"].insert_one(data["aim"])
    else:
        c.aim.replace_one({}, data["aim"])




