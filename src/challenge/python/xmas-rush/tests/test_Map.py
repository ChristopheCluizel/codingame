import sys, os
import pytest

sys.path.insert(0, os.path.abspath('..'))
from app import Map


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
