# YOUR BACKEND TESTS HERE
import model
import pytest

DBNAME = "evently_dev"


@pytest.fixture()
def coll():
    c = model.get_collection(DBNAME, "events")
    c.delete_many({})
    return c


def test_create_event(coll):
    model.add_event(coll, "12345", "Orel Birthday at ashkelon 7/2/2020")
    event = model.get_event(coll, "12345")
    assert event['description'] == "Orel Birthday at ashkelon 7/2/2020"
    model.rsvp(coll, "12345", "302488630", "Omer Daniel", 3, ["coke"])
