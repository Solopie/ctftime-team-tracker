import pymongo
from .config import MONGODB_URL

def connect():
    client = pymongo.MongoClient(MONGODB_URL)
    return client

def get_db_data():
    pass

def update_db(data):
    pass



