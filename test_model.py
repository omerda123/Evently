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
    assert type(res) == dict


def test_get_event(events):
    model.add_event(events, "12345", "Orel Birthday at ashkelon 7/2/2020", "Omer Daniel")
    res1 = model.get_event(events, "12345")
    assert type(res1) == dict
    res2 = model.get_event(events, "6789")
    assert res2 is None


def test_get_last_event(user_events):
    model.add_event(user_events, "12345", "Orel Birthday at ashkelon 7/2/2020", "Omer Daniel")
    model.add_event_to_user(user_events, "1111", "12345")
    res = model.get_last_event(user_events, "1111")
    assert res == "12345"


def test_get_items(events):
    model.add_event(events, "12345", "Orel Birthday at ashkelon 7/2/2020", "Omer Daniel")
    model.add_items_to_event(events, "12345", "bamba")
    model.add_items_to_event(events, "12345", "bisli")
    model.add_items_to_event(events, "12345", "cola")
    res = model.get_items(events, "12345")
    assert len(res[0]) == 0
    assert len(res[1]) == 3


def test_get_participants(events):
    model.add_event(events, "12345", "Orel Birthday at ashkelon 7/2/2020", "Omer Daniel")
    model.rsvp(events, "12345", "1111", "Omer Daniel", 1)
    res = model.get_participants(events, "12345")
    assert res[0]['user_id'] == "1111"


def test_rsvp(events):
    model.add_event(events, "12345", "Orel Birthday at ashkelon 7/2/2020", "Omer Daniel")
    model.rsvp(events, "12345", "1111", "Omer Daniel", 2)
    res = model.get_event(events, "12345")
    print(res['participants'])
    assert len(res['participants']) == 1


def test_friend_brings_item(events):
    model.add_event(events, "12345", "Orel Birthday at ashkelon 7/2/2020", "Omer Daniel")
    model.rsvp(events, "12345", "1111", "Omer Daniel", 2)
    model.add_items_to_event(events, "12345", "bamba")
    model.friend_brings_item(events, "12345", "1111", "bamba")
    res = model.get_event(events, "12345")
    assert res['participants'][0]['brings'][0] == "bamba"
