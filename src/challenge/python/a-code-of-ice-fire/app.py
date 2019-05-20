import sys
import math
import json
import uuid

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
            return Position(self.map.width - 2, self.map.height -1)

    def get_train_orders(self):
        res = []

        if self.my_gold > 10 and (self.my_income - 1 >= 0):
            spawn_position = self.get_spawn_position()
            res.append("TRAIN {} {} {}".format(1, spawn_position.x, spawn_position.y))

        return res

    def get_move_orders(self):
        res = []
        my_units = self.get_my_units()
        enemy_hq = self.get_buildings(1, 0)[0]

        for unit in my_units:
            res.append("MOVE {} {} {}".format(unit.id, enemy_hq.position.x, enemy_hq.position.y))

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
