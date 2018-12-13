import sys, os
import pytest

sys.path.insert(0, os.path.abspath('..'))
from app import Map, Position


@pytest.fixture()
def before():
    print("\r")


def test_load_from_file():
    map = Map(4)
    map.load_from_file("resources/map1.txt")

    first_tile = map.tiles[0][0]
    assert str(first_tile) == "0110"
    assert not first_tile.up
    assert first_tile.right
    assert first_tile.down
    assert not first_tile.left

    assert str(map.tiles[1][0]) == "0011"
    assert str(map.tiles[3][0]) == "1101"
    assert str(map.tiles[1][2]) == "0110"


def test_simulate_move():
    map = Map(4)
    map.load_from_file("resources/map1.txt")
    tile = "1111"

    simulated_map, item_position, my_player_position = map.simulate_move(Position(0, 0), tile, 0, "RIGHT")
    assert [str(tile) for tile in simulated_map.tiles[0]] == ["1111", "0101", "0111", "0011"]
    assert [str(tile) for tile in simulated_map.tiles[1]] == ["0110", "1010", "0110", "0101"]
    assert [str(tile) for tile in simulated_map.tiles[2]] == ["0011", "1101", "1001", "0111"]
    assert [str(tile) for tile in simulated_map.tiles[3]] == ["1001", "1110", "1101", "0101"]

    simulated_map, item_position, my_player_position = map.simulate_move(Position(0, 0), tile, 2, "LEFT")
    assert [str(tile) for tile in simulated_map.tiles[0]] == ["0110", "0101", "0110", "0011"]
    assert [str(tile) for tile in simulated_map.tiles[1]] == ["0011", "1010", "1001", "0101"]
    assert [str(tile) for tile in simulated_map.tiles[2]] == ["1001", "1101", "1101", "0111"]
    assert [str(tile) for tile in simulated_map.tiles[3]] == ["1101", "1110", "1111", "0101"]

    simulated_map, item_position, my_player_position = map.simulate_move(Position(0, 0), tile, 1, "UP")
    assert [str(tile) for tile in simulated_map.tiles[0]] == ["0110", "0101", "0111", "0011"]
    assert [str(tile) for tile in simulated_map.tiles[1]] == ["1010", "0110", "0101", "1111"]
    assert [str(tile) for tile in simulated_map.tiles[2]] == ["1001", "1101", "1001", "0111"]
    assert [str(tile) for tile in simulated_map.tiles[3]] == ["1101", "1110", "1101", "0101"]

    simulated_map, item_position, my_player_position = map.simulate_move(Position(0, 0), tile, 2, "DOWN")
    assert [str(tile) for tile in simulated_map.tiles[0]] == ["0110", "0101", "0111", "0011"]
    assert [str(tile) for tile in simulated_map.tiles[1]] == ["0011", "1010", "0110", "0101"]
    assert [str(tile) for tile in simulated_map.tiles[2]] == ["1111", "1001", "1101", "1001"]
    assert [str(tile) for tile in simulated_map.tiles[3]] == ["1101", "1110", "1101", "0101"]
