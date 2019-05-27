import sys
import math
import json
import uuid
import queue
import random

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
        self.type = type  # 0: HQ, 1: mine, 2: tower
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
        self.owner = owner  # 0: me, 1: enemy
        self.state = state  # 0 inactive, 1 active
        self.unit = None
        self.building = None


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

    def get_node_ids(self, owners, state=None):
        if state is None:
            return [node.id for index, node in self.nodes.items() if node.owner in owners]
        else:
            return [node.id for index, node in self.nodes.items() if node.owner in owners and node.state == state]


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

    def update_graph(self):
        # update nodes with units
        units = game.units

        for unit in units:
            node_id = self.position_to_node_id(unit.position, self.map.width)
            game.graph.nodes[node_id].unit = unit

        # update nodes with buildings
        mine_spots = self.mines
        buildings = self.buildings

        for mine_spot_position in mine_spots:
            node_id = self.position_to_node_id(mine_spot_position, self.map.width)
            self.graph.nodes[node_id].building = "mine_spot"

        for building in buildings:
            node_id = self.position_to_node_id(building.position, self.map.width)
            if building.type == 0:
                self.graph.nodes[node_id].building = "hq"
            elif building.type == 1:
                self.graph.nodes[node_id].building = "mine"
            elif building.type == 2:
                self.graph.nodes[node_id].building = "tower"
            else:
                self.graph.nodes[node_id].building = None

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

    def get_spawn_node_ids(self):
        all_my_node_ids = list(self.graph.get_node_ids([0]))
        my_occupied_node_ids = [self.position_to_node_id(building.position, self.map.width) for building in self.get_my_buildings()] + [
            self.position_to_node_id(unit.position, self.map.width) for unit in self.get_my_units()]
        adjacent_ids = []

        for node_id in all_my_node_ids:
            node_neighbour_ids = self.graph.get_neighbours(node_id)

            for node_neighbour_id in node_neighbour_ids:
                if self.graph.nodes[node_neighbour_id].owner in [-1, 1]:
                    adjacent_ids.append(node_neighbour_id)

        if len(adjacent_ids) > 0:
            return adjacent_ids
        else:
            return list((set(all_my_node_ids) - set(my_occupied_node_ids)))

    def get_spawn_position(self, targeted_move_positions):
        my_node_ids = self.get_spawn_node_ids()
        targeted_node_ids = [self.position_to_node_id(position, self.map.width) for position in targeted_move_positions]

        # print_debug(my_node_ids)
        # print_debug(targeted_node_ids)

        available_ids = list(set(my_node_ids) - set(targeted_node_ids))

        if len(available_ids) > 0:
            return self.node_id_to_position(random.choice(available_ids), self.map.width)
        else:
            return self.node_id_to_position(random.choice(my_node_ids), self.map.width)

    def get_train_orders(self, targeted_positions):
        res = []
        train_positions = []
        income = self.my_income
        gold = self.my_gold
        end_train = False

        level_one_units_count = len([unit for unit in self.units if unit.owner == 0 and unit.level == 1])
        level_two_units_count = len([unit for unit in self.units if unit.owner == 0 and unit.level == 2])
        no_neutral_nodes = True if len(self.graph.get_node_ids([-1])) == 0 else False

        while income > 0 and gold > 0 and not end_train:
            if gold >= 10 and (income - 1 >= 0 and income <= 20) and level_one_units_count < 10 and not no_neutral_nodes:
                spawn_position = self.get_spawn_position(targeted_positions)
                income -= 1
                gold -= 10
                train_positions.append(spawn_position)
                res.append("TRAIN {} {} {}".format(1, spawn_position.x, spawn_position.y))
            elif gold >= 20 and income - 4 >= 0 and level_two_units_count < 8:
                spawn_position = self.get_spawn_position(targeted_positions)
                income -= 4
                gold -= 20
                res.append("TRAIN {} {} {}".format(2, spawn_position.x, spawn_position.y))
                train_positions.append(spawn_position)
            elif gold >= 30 and (income - 20 >= 0):
                spawn_position = self.get_spawn_position(targeted_positions)
                income -= 20
                gold -= 30
                res.append("TRAIN {} {} {}".format(3, spawn_position.x, spawn_position.y))
                train_positions.append(spawn_position)
            else:
                end_train = True
        return res, train_positions

    def get_move_orders(self):
        res = []
        my_units = self.get_my_units()
        target_ids = self.graph.get_node_ids([-1, 1])
        already_targeted_id = []
        move_positions = []
        # spawn_ids = [self.position_to_node_id(spawn_position, self.map.width) for spawn_position in spawn_positions]

        all_node_ids = list(self.graph.nodes.keys())
        occupied_node_ids = [self.position_to_node_id(building.position, self.map.width) for building in self.buildings if (building.owner == 0)] + [
            self.position_to_node_id(unit.position, self.map.width) for unit in self.units]
        empty_node_ids = set(all_node_ids) - set(occupied_node_ids)

        for unit in my_units:
            position = unit.position
            node_id = self.position_to_node_id(position, self.map.width)

            if unit.level == 1:
                targeted_node_id = self.graph.get_path_towards_nearest_targeted_zone(node_id, set(target_ids) - set(already_targeted_id), all_node_ids)
            else:
                targeted_node_id = self.graph.get_path_towards_nearest_targeted_zone(node_id, set(target_ids) - set(already_targeted_id), all_node_ids)

            already_targeted_id.append(targeted_node_id)

            if targeted_node_id is not None:
                targeted_position = self.node_id_to_position(targeted_node_id, self.map.width)
                move_positions.append(targeted_position)
                res.append("MOVE {} {} {}".format(unit.id, targeted_position.x, targeted_position.y))
                # print_debug("unit {} targets {}".format(unit.id, targeted_position))

        return res, move_positions

    def get_build_orders(self):
        build_orders = []

        # build mines
        mines = [building for building in self.get_buildings(0, 1)]
        nb_of_mines = len(mines)
        my_qg_position = [building for building in self.buildings if building.type == 0 and building.owner == 0][0].position
        mine_spot_nodes = [node for index, node in self.graph.nodes.items() if node.building == "mine_spot"]
        mine_spot_distances = [
            (self.node_id_to_position(node.id, self.map.width), my_qg_position.distance_with(self.node_id_to_position(node.id, self.map.width))) for node in mine_spot_nodes
        ]
        closest_mine_spot_position = sorted(mine_spot_distances, key=lambda tuple: tuple[1])[0][0]

        if nb_of_mines == 0 and self.my_gold >= 20:
            build_orders.append("BUILD MINE {} {}".format(closest_mine_spot_position.x, closest_mine_spot_position.y))

        # build towers
        return build_orders

    def get_orders(self):
        move_orders, move_positions = self.get_move_orders()
        train_orders, spawn_positions = self.get_train_orders(move_positions)
        build_orders = self.get_build_orders()

        all_orders = move_orders + train_orders + build_orders

        if len(all_orders) > 0:
            return ";".join(all_orders)
        else:
            return "WAIT"


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

        game.update_graph()

        # print_debug(game)
        # print_debug(game.graph)

        orders = game.get_orders()
        print(orders)
