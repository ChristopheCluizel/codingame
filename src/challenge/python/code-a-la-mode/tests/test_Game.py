import sys
import os
import pytest

sys.path.insert(0, os.path.abspath('..'))
from app import Map, Position, Game, Command, Dessert, Oven


@pytest.fixture()
def before():
    print("\r")


def test_get_better_command():
    map = Map(11, 7)
    map.load_from_file("resources/map3.txt")

    commands = [
        Command("id1", "DISH-BLUEBERRIES-ICE_CREAM", 10),
        Command("id2", "DISH-ICE_CREAM-CHOPPED_STRAWBERRIES", 20),
        Command("id3", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 100),
        Command("id4", "DISH-BLUEBERRIES-CROISSANT", 30),
        Command("id5", "DISH-CROISSANT-CHOPPED_STRAWBERRIES", 50),
        Command("id6", "DISH-TART-CHOPPED_STRAWBERRIES", 300)
    ]
    game = Game(map, 6, commands)
    game.current_commands = [
        Command("id1", "DISH-BLUEBERRIES-ICE_CREAM", 10),
        Command("id3", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 100),
        Command("id6", "DISH-TART-CHOPPED_STRAWBERRIES", 300)
    ]

    better_command = game.get_better_command()

    assert better_command.is_equal(Command("id3", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 100))


def test_is_command_validated():
    map = Map(11, 7)
    map.load_from_file("resources/map3.txt")

    commands = [
        Command("id1", "DISH-BLUEBERRIES-ICE_CREAM", 10),
        Command("id2", "DISH-ICE_CREAM-CHOPPED_STRAWBERRIES", 20),
        Command("id3", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 100),
        Command("id4", "DISH-BLUEBERRIES-CROISSANT", 30),
        Command("id5", "DISH-CROISSANT-CHOPPED_STRAWBERRIES", 50),
        Command("id6", "DISH-TART-CHOPPED_STRAWBERRIES", 300)
    ]
    game = Game(map, 6, commands)
    game.current_commands = [
        Command("id1", "DISH-BLUEBERRIES-ICE_CREAM", 10),
        Command("id3", "DISH-CROISSANT-ICE_CREAM-CHOPPED_STRAWBERRIES", 100),
        Command("id5", "DISH-CROISSANT-CHOPPED_STRAWBERRIES", 50)
    ]

    game.get_better_command()
    assert not game.is_command_validated()

    game.current_commands = [
        Command("id1", "DISH-BLUEBERRIES-ICE_CREAM", 10),
        Command("id5", "DISH-CROISSANT-CHOPPED_STRAWBERRIES", 50)
    ]

    assert game.is_command_validated()


def test_make():
    map = Map(11, 7)
    map.load_from_file("resources/map3.txt")

    commands = [
        Command("id1", "DISH-BLUEBERRIES-ICE_CREAM", 10)
    ]
    game = Game(map, 1, commands)

    orders = game.make(Dessert("CROISSANT"))
    assert len(orders) == 5

    orders = game.make(Dessert("CHOPPED_STRAWBERRIES"))
    assert len(orders) == 3


def test_find_or_make():
    map = Map(11, 7)
    map.load_from_file("resources/map3.txt")

    commands = [
        Command("id1", "DISH-BLUEBERRIES-ICE_CREAM-CROISSANT", 10),
        Command("id5", "DISH-CROISSANT-CHOPPED_STRAWBERRIES", 50)
    ]
    game = Game(map, 1, commands)
    game.oven = Oven(12, "NONE")
    game.current_commands = [
        Command("id5", "DISH-CROISSANT-CHOPPED_STRAWBERRIES", 50)
    ]
    game.get_better_command()

    orders = game.find_or_make(Dessert("CROISSANT"))
    assert len(orders) == 5

    game.oven = Oven(12, "CROISSANT")

    orders = game.find_or_make(Dessert("CROISSANT"))
    assert len(orders) == 0
    assert game.current_command.desserts_state["CROISSANT"]
