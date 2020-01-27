# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
from pymongo import MongoClient


def get_collection(dbname, coll):
    client = MongoClient()
    db = client.get_database(dbname)
    coll = db.get_collection(coll)
    return coll


def add_event(coll, event_id, text):
    coll.update_one({},
                    {"$set":
                         {"id": event_id,
                          "description": text,
                          "participants": []
                          }}, upsert=True)


def add_event_to_user(coll, user_id, event_id):
    coll.update_one({},
                    {"$set":
                         {"user_id": user_id,
                          "event_id": event_id
                          }}, upsert=True)


def get_event(coll, event_id):
    res = coll.find_one({"id": event_id})
    return res


def get_last_event(coll, user_id):
    event_id = coll.find_one({"user_id": user_id})
    return event_id["event_id"]


def get_participants(coll, event_id):
    res = coll.find_one({"id": event_id})
    return res['participants']



def rsvp(coll, event_id, user_id, name, num_of_participants, brings):
    coll.update_one({"id": event_id},
                    {"$push": {
                        'participants': {
                            "user_id": user_id,
                            "name": name,
                            "rsvp": num_of_participants,
                            "brings": brings
                        }
                    }
                    })
