# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
from pymongo import MongoClient


def create_connection():
    client = MongoClient()
    db = client.get_database("evently")
    coll = db.get_collection("events")
    return coll


def add_event(uuid, text):
    coll = create_connection()
    coll.insert_one({
        "id": uuid,
        "description": text
    })


def get_event(args):
    coll = create_connection()
    res = coll.find_one({"id":args})
    return res
