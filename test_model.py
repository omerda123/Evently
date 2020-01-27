# YOUR BACKEND TESTS HERE
import model
import pytest

DBNAME = "evently_dev"


@pytest.fixture()
def events():
    c = model.get_collection(DBNAME, "events")
    c.delete_many({})
    return c


@pytest.fixture()
def user_events():
    c = model.get_collection(DBNAME, "user_events")
    c.delete_many({})
    return c


def test_create_event(events):
    model.add_event(events, "12345", "Orel Birthday at ashkelon 7/2/2020", "Omer Daniel")
    event = model.get_event(events, "12345")
    assert event['description'] == "Orel Birthday at ashkelon 7/2/2020"


def test_add_items_to_event(events):
    model.add_items_to_event(events, "12345", "bamba")
    model.add_items_to_event(events, "12345", "bisli")
    model.add_items_to_event(events, "12345", "cola")
    res = model.get_event(events, "12345")
    assert len(res['items']) == 3


def test_add_event_to_user(user_events):
    model.add_event_to_user(user_events, "1111", "12345")
    res = user_events.find_one({"user_id": "1111"})
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(res)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    assert type(res) == dict


def test_get_event(events):
    model.add_event(events, "12345", "Orel Birthday at ashkelon 7/2/2020", "Omer Daniel")
    res1 = model.get_event(events, "12345")
    assert type(res1) == dict
    res2 = model.get_event(events, "6789")
    assert res2 is None

def test_get_last_event(user_events):
    model.add_event(events, "12345", "Orel Birthday at ashkelon 7/2/2020", "Omer Daniel")
    model.add_event_to_user(user_events, "1111", "12345")

