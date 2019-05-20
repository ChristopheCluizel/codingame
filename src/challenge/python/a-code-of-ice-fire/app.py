import sys
import math
import json
import uuid
import queue

DEBUG = False


def print_debug(description):
    if DEBUG:
        print(description, file=sys.stderr)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def is_equal(self, that):
        return self.x == that.x and self.y == that.y

    def distance_with(self, that):
        return math.sqrt((that.x - self.x) * (that.x - self.x) + (that.y - self.y) * (that.y - self.y))


class Unit:
    def __init__(self, id, owner, level, position):
        self.id = id
        self.owner = owner
        self.level = level
        self.position = position

    def __str__(self):
        return "id: {}, owner: {}, level: {}, position: {}".format(
            self.id,
            self.owner,
            self.level,
            self.position
        )


class Building:
    def __init__(self, id, owner, type, position):
        self.id = id
        self.owner = owner
        self.type = type
        self.position = position

    def __str__(self):
        return "id: {}, owner: {}, type: {}, position: {}".format(
            self.id,
            self.owner,
            self.type,
            self.position
        )


class Map:
    def __init__(self):
        self.width = 12
        self.height = 12
        self.tiles = None
        self.flush()

    def __str__(self):
        res = ""
        for row_index in range(self.height):
            for column_index in range(self.width):
                res += str(self.tiles[column_index][row_index])
            res += "\n"

        return res[:-1]

    def flush(self):
        self.tiles = [[] for i in range(self.width)]

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            data = file.readlines()

        for row_index, row in enumerate(data):
            row = row.replace("\n", "")
            for column_index, tile_string in enumerate(row):
                self.add_tile(row_index, column_index, tile_string)

    def add_tile(self, row_index, column_index, tile_string):
        self.tiles[column_index].append(tile_string)


class Node:
    def __init__(self, id, owner, state):
        self.id = id
        self.owner = owner
        self.state = state  # 0 inactive, 1 active,


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def __str__(self):
        return "{}".format(self.edges)

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, node_id_1, node_id_2):
        if node_id_1 in self.edges.keys():
            self.edges[node_id_1].append(node_id_2)
        else:
            self.edges[node_id_1] = [node_id_2]

    def get_neighbours(self, node_id):
        """
        Return the ids of the neighbours
        :param node_id:
        :type node_id: list[int]
        :return:
        :rtype:
        """
        return self.edges[node_id]

    def get_path_towards_nearest_targeted_zone(self, start_zone_id, target_zone_ids, empty_node_ids):
        """
        Return first move towards the targeted zone

        :param start_zone_id:
        :type start_zone_id:
        :param target_zone_ids:
        :type target_zone_ids:
        :return: the zone id
        :rtype: int
        """

        def backtrace(parent, start, end):
            path = [end]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.reverse()
            return path[1]

        parent = {}
        seen = {start_zone_id}
        q = queue.Queue()
        q.put(start_zone_id)

        while not q.empty():
            vertex = q.get()
            if vertex in target_zone_ids:
                return backtrace(parent, start_zone_id, vertex)

            for node_id in self.edges[vertex]:
                if node_id not in seen and node_id in empty_node_ids:
                    parent[node_id] = vertex
                    seen.add(node_id)
                    q.put(node_id)

        return None

    def get_node_ids(self, owner, state=None):
        if state is None:
            return [node.id for index, node in self.nodes.items() if node.owner in owner]
        else:
            return [node.id for index, node in self.nodes.items() if node.owner in owner and node.state == state]


class Game:
    def __init__(self):
        self.my_gold = 0
        self.my_income = 0
        self.enemy_gold = 0
        self.enemy_income = 0
        self.map = None,
        self.buildings = []
        self.units = []
        self.mines = []
        self.graph = Graph()

    def __str__(self):
        return "====\nmy_gold: {}, my_income: {}, enemy_gold: {}, enemy_income: {}\n{}\n----\n{}\n{}".format(
            self.my_gold,
            self.my_income,
            self.enemy_gold,
            self.enemy_income,
            "\n".join([str(unit) for unit in self.units]),
            "\n".join([str(building) for building in self.buildings]),
            self.map
        )

    def map_to_graph(self, map):
        graph = Graph()

        for y in range(0, map.height):
            for x in range(0, map.width):
                character = map.tiles[x][y]
                node_id = x + y * map.width

                if character == '.':
                    owner = -1
                    state = 0
                elif character == "O":
                    owner = 0
                    state = 1
                elif character == "o":
                    owner = 0
                    state = 0
                elif character == "X":
                    owner = 1
                    state = 1
                elif character == "x":
                    owner = 1
                    state = 0
                else:
                    owner = None
                    state = None

                if character != '#':
                    node = Node(node_id, owner, state)
                    graph.add_node(node)

                if x + 1 < map.width and map.tiles[x + 1][y] != '#':
                    graph.add_edge(node_id, self.position_to_node_id(Position(x + 1, y), map.width))
                if x - 1 >= 0 and map.tiles[x - 1][y] != '#':
                    graph.add_edge(node_id, self.position_to_node_id(Position(x - 1, y), map.width))
                if y + 1 < map.height and map.tiles[x][y + 1] != '#':
                    graph.add_edge(node_id, self.position_to_node_id(Position(x, y + 1), map.width))
                if y - 1 >= 0 and map.tiles[x][y - 1] != '#':
                    graph.add_edge(node_id, self.position_to_node_id(Position(x, y - 1), map.width))

        return graph

    def position_to_node_id(self, position, map_width):
        return position.x + position.y * map_width

    def node_id_to_position(self, id, map_width):
        x = id % map_width
        y = id // map_width

        return Position(x, y)

    def get_buildings(self, owner, type=None):
        if type is None:
            return [building for building in self.buildings if building.owner == owner]
        else:
            return [building for building in self.buildings if building.owner == owner and building.type == type]

    def get_my_buildings(self):
        return self.get_buildings(0)

    def get_enemy_buildings(self):
        return self.get_buildings(1)

    def get_units(self, owner):
        return [unit for unit in self.units if unit.owner == owner]

    def get_my_units(self):
        return self.get_units(0)

    def get_enemy_units(self):
        return self.get_units(1)

    def get_spawn_position(self):
        my_hq = self.get_buildings(0, 0)[0]

        if my_hq.position.x == 0:
            return Position(1, 0)
        else:
            return Position(self.map.width - 2, self.map.height - 1)

    def get_train_orders(self):
        res = []

        if self.my_gold > 10 and (self.my_income - 1 >= 0):
            spawn_position = self.get_spawn_position()
            res.append("TRAIN {} {} {}".format(1, spawn_position.x, spawn_position.y))

        return res

    def get_move_orders(self):
        res = []
        my_units = self.get_my_units()
        target_ids = self.graph.get_node_ids([-1, 1])
        all_node_ids = list(self.graph.nodes.keys())
        occupied_node_ids = [self.position_to_node_id(building.position, self.map.width) for building in self.buildings if (building.owner == 0)] + [
            self.position_to_node_id(unit.position, self.map.width) for unit in self.units]
        empty_node_ids = set(all_node_ids) - set(occupied_node_ids)

        # print_debug(empty_node_ids)

        for unit in my_units:
            position = unit.position
            node_id = self.position_to_node_id(position, self.map.width)
            targeted_node_id = self.graph.get_path_towards_nearest_targeted_zone(node_id, target_ids, empty_node_ids)

            print_debug("unit_id: {}".format(unit.id))
            print_debug(targeted_node_id)

            if targeted_node_id is not None:
                targeted_position = self.node_id_to_position(targeted_node_id, self.map.width)
                res.append("MOVE {} {} {}".format(unit.id, targeted_position.x, targeted_position.y))

        return res

    def get_orders(self):
        train_orders = self.get_train_orders()
        move_orders = self.get_move_orders()

        train_orders_string = ";".join(train_orders)
        move_orders_string = ";".join(move_orders)

        if len(train_orders_string) > 0 and len(move_orders_string) > 0:
            final_orders_string = "{};{}".format(move_orders_string, train_orders_string)
        elif len(train_orders_string) > 0 and len(move_orders_string) == 0:
            final_orders_string = "{}".format(train_orders_string)
        elif len(train_orders_string) == 0 and len(move_orders_string) > 0:
            final_orders_string = "{}".format(move_orders_string)
        else:
            final_orders_string = "WAIT"
        return final_orders_string


if __name__ == '__main__':
    game = Game()

    number_mine_spots = int(input())
    for i in range(number_mine_spots):
        x, y = [int(j) for j in input().split()]
        position = Position(x, y)
        game.mines.append(position)

    # game loop
    while True:
        game.my_gold = int(input())  # gold
        game.my_income = int(input())  # income
        game.enemy_gold = int(input())  # opponent_gold
        game.enemy_income = int(input())  # opponent_income

        # get map
        map = Map()
        for i in range(12):
            for column_index, tile in enumerate(input()):
                map.add_tile(i, column_index, tile)
        game.map = map

        # update graph with map
        game.graph = game.map_to_graph(map)

        # print_debug(game.graph)

        # get buildings
        building_count = int(input())
        buildings = []
        for i in range(building_count):
            owner, building_type, x, y = [int(j) for j in input().split()]
            building = Building(None, owner, building_type, Position(x, y))
            buildings.append(building)
        game.buildings = buildings

        # get units
        unit_count = int(input())
        units = []
        for i in range(unit_count):
            owner, unit_id, level, x, y = [int(j) for j in input().split()]
            unit = Unit(unit_id, owner, level, Position(x, y))
            units.append(unit)
        game.units = units

        print_debug(game)

        orders = game.get_orders()
        print(orders)
