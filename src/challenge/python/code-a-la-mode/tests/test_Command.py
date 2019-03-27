import sys, os
import pytest

sys.path.insert(0, os.path.abspath('..'))
from app import Map, Position, Game, Command, Dessert


@pytest.fixture()
def before():
    print("\r")


def test_get_dessert_from_name():
    command = Command("id1", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 10)

    assert len(command.desserts) == 3
    assert command.get_dessert_from_name("CROISSANT").is_equal(Dessert("CROISSANT"))
    assert command.get_dessert_from_name("ICE_CREAM").is_equal(Dessert("ICE_CREAM"))
    assert command.get_dessert_from_name("CHOPPED_STRAWBERRIES").is_equal(Dessert("CHOPPED_STRAWBERRIES"))
    assert command.get_dessert_from_name("WRONG_NAME") is None


def set_dessert_state():
    command = Command("id1", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 10)

    command.set_dessert_state("CROISSANT", True)
    assert command.desserts_state["CROISSANT"]

    command.set_dessert_state("CROISSANT", False)
    assert not command.desserts_state["CROISSANT"]


def test_get_desserts_from_state():
    command = Command("id1", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 10)

    desserts = command.get_desserts_from_state(False)
    assert len(desserts) == 3

    command.set_dessert_state("CROISSANT", True)
    desserts = command.get_desserts_from_state(True)
    assert len(desserts) == 1


def test_get_desserts_from_level():
    command = Command("id1", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 10)

    desserts = command.get_desserts_from_level("classic")
    assert len(desserts) == 2

    desserts = command.get_desserts_from_level("basic")
    assert len(desserts) == 1


def test_get_desserts_from_state_and_level():
    command = Command("id1", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 10)

    desserts = command.get_desserts_from_state_and_level(False, "classic")
    assert len(desserts) == 2

    desserts = command.get_desserts_from_state_and_level(True, "classic")
    assert len(desserts) == 0
