import sys, os
import pytest

sys.path.insert(0, os.path.abspath('..'))
from app import Graph, Map, Position


@pytest.fixture()
def get_map():
    my_map = Map(4)
    my_map.load_from_file("resources/map1.txt")
    return my_map


def test_add_edge():
    graph = Graph()
    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(5, 6)

    assert 1 in graph.nodes[0]
    assert 3 in graph.nodes[0]
    assert 0 in graph.nodes[1]
    assert 0 in graph.nodes[3]
    assert 6 in graph.nodes[5]
    assert 5 in graph.nodes[6]


def test_remove_edge():
    graph = Graph()
    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(5, 6)

    assert 1 in graph.nodes[0]
    assert 3 in graph.nodes[0]
    assert 0 in graph.nodes[1]
    assert 0 in graph.nodes[3]
    assert 6 in graph.nodes[5]
    assert 5 in graph.nodes[6]

    graph.remove_edge(0, 3)

    assert 3 not in graph.nodes[0]
    assert 0 not in graph.nodes[3]
    assert 1 in graph.nodes[0]
    assert 0 in graph.nodes[1]
    assert 6 in graph.nodes[5]
    assert 5 in graph.nodes[6]


def test_get_neighbours():
    graph = Graph()
    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(0, 5)
    graph.add_edge(5, 6)

    neighbours = graph.get_neighbours(0)

    assert set(neighbours) == {1, 3, 5}


def test_position_to_node_index():
    graph = Graph()

    assert graph.position_to_node_index(Position(0, 0), 4) == 0
    assert graph.position_to_node_index(Position(1, 0), 4) == 1
    assert graph.position_to_node_index(Position(3, 3), 4) == 15
    assert graph.position_to_node_index(Position(2, 2), 4) == 10


def test_node_index_to_position():
    graph = Graph()

    assert graph.node_index_to_position(0, 4).is_equal(Position(0, 0))
    assert graph.node_index_to_position(1, 4).is_equal(Position(1, 0))
    assert graph.node_index_to_position(10, 4).is_equal(Position(2, 2))
    assert graph.node_index_to_position(12, 4).is_equal(Position(0, 3))
    assert graph.node_index_to_position(15, 4).is_equal(Position(3, 3))


def test_map_to_graph(get_map):
    map = get_map
    graph = Graph()

    graph.map_to_graph(map)

    assert graph.are_connected(0, 1)
    assert graph.are_connected(1, 0)
    assert graph.are_connected(1, 5)
    assert graph.are_connected(5, 1)
    assert graph.are_connected(9, 10)
    assert graph.are_connected(10, 9)

    assert not graph.are_connected(0, 4)
    assert not graph.are_connected(15, 11)
