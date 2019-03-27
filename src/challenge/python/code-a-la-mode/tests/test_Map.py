import sys, os
import pytest

sys.path.insert(0, os.path.abspath('..'))
from app import Map, Position, Game, Command


@pytest.fixture()
def before():
    print("\r")


def test_load_from_file():
    map = Map(11, 7)
    map.load_from_file("resources/map1.txt")

    expected_res = """#####D#####
#.......1.#
#.####.##.#
B.#..#..#.#
#.##.####.#
#.0.......#
##I##W#####"""

    assert str(map) == expected_res


def test_find_position1():
    map = Map(11, 7)
    map.load_from_file("resources/map1.txt")

    assert map.find_stable_position("DISH").is_equal(Position(5, 0))
    assert map.find_stable_position("window").is_equal(Position(5, 6))
    assert map.find_stable_position("BLUEBERRIES").is_equal(Position(0, 3))
    assert map.find_stable_position("ICE_CREAM").is_equal(Position(2, 6))


def test_find_position2():
    map = Map(11, 7)
    map.load_from_file("resources/map2.txt")

    assert map.find_stable_position("DISH").is_equal(Position(5, 0))
    assert map.find_stable_position("window").is_equal(Position(5, 6))
    assert map.find_stable_position("BLUEBERRIES").is_equal(Position(6, 0))
    assert map.find_stable_position("ICE_CREAM").is_equal(Position(0, 1))
    assert map.find_stable_position("STRAWBERRIES").is_equal(Position(0, 4))
    assert map.find_stable_position("chopping_board").is_equal(Position(6, 4))


def test_find_position3():
    map = Map(11, 7)
    map.load_from_file("resources/map3.txt")

    assert map.find_stable_position("DISH").is_equal(Position(5, 0))
    assert map.find_stable_position("window").is_equal(Position(5, 6))
    assert map.find_stable_position("BLUEBERRIES").is_equal(Position(7, 6))
    assert map.find_stable_position("ICE_CREAM").is_equal(Position(5, 3))
    assert map.find_stable_position("STRAWBERRIES").is_equal(Position(10, 6))
    assert map.find_stable_position("chopping_board").is_equal(Position(10, 0))
    assert map.find_stable_position("oven").is_equal(Position(1, 0))
    assert map.find_stable_position("DOUGH").is_equal(Position(4, 2))


def test_get_better_command():
    commands = [
        Command("id1", "DISH-BLUEBERRIES-ICE_CREAM", 10),
        Command("id2", "DISH-BLUEBERRIES-ICE_CREAM", 5),
        Command("id3", "DISH-BLUEBERRIES-ICE_CREAM", 20),
        Command("id4", "DISH-BLUEBERRIES-ICE_CREAM", 3),
        Command("id5", "DISH-BLUEBERRIES-ICE_CREAM", 15),
    ]
    game = Game(None, 5, commands)
    game.current_commands = commands[0:3]

    better_command = game.get_better_command()

    assert better_command.id == "id3"


# def test_set_orders():
#     commands = [
#         Command("id1", "DISH-BLUEBERRIES-ICE_CREAM", 10),
#         Command("id2", "DISH-BLUEBERRIES-ICE_CREAM", 5),
#         Command("id3", "DISH-BLUEBERRIES-ICE_CREAM", 20),
#         Command("id4", "DISH-BLUEBERRIES-ICE_CREAM", 3),
#         Command("id5", "DISH-BLUEBERRIES-ICE_CREAM", 15),
#     ]
#     game = Game(None, 5, commands)
#     game.current_commands = commands[0:3]
#     game.get_better_command()
#
#     game.set_orders()
#
#     assert game.orders == [
#         {"priority": 0, "action": "take", "item": "dish", "location": "dish_washer", "validation": "DISH"},
#         {"priority": 1, "action": "take", "item": "blueberry", "location": "blueberry_crate", "validation": "BLUEBERRIES"},
#         {"priority": 1, "action": "take", "item": "ice_cream", "location": "ice_cream_crate", "validation": "ICE_CREAM"},
#         {"priority": 2, "action": "drop", "item": "window", "location": "window", "validation": "NONE"}
#     ]
