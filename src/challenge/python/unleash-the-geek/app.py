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


class Tile:
    def __init__(self, ore, is_hole):
        self.ore = ore
        self.is_hole = is_hole

    def __str__(self):
        return "ore: {}, is_hole: {}".format(self.ore, self.is_hole)


class Unit:
    def __init__(self, id, type, position, item):
        self.id = id
        self.type = type
        self.position = position
        self.item = item
        self.status = "IDLE"
        self.target = None

    def __str__(self):
        return "id: {}, type: {}, position: {}, item: {}, status: {}, target: {}".format(
            self.id,
            self.type,
            self.position,
            self.item,
            self.status,
            self.target
        )

    def is_carrying_ore(self):
        return self.item == 4


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = None
        self.flush()

    def __str__(self):
        res = ""
        for row_index in range(self.height):
            for column_index in range(self.width):
                tile = self.tiles[column_index][row_index]
                res += '0' if tile.is_hole else '#'
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

    def add_tile(self, row_index, column_index, tile):
        self.tiles[column_index].append(tile)

    def is_hole(self, position):
        tile = self.tiles[position.x][position.y]
        return tile.is_hole

    def get_ore_positions_without_hole(self):
        res = []

        for row_index in range(self.height):
            for column_index in range(self.width):
                tile = self.tiles[column_index][row_index]
                if tile.ore != "?":
                    if int(tile.ore) > 0 and not tile.is_hole:
                        res.append(Position(column_index, row_index))

        return res

    def get_ore_positions(self):
        res = []

        for row_index in range(self.height):
            for column_index in range(self.width):
                tile = self.tiles[column_index][row_index]
                if tile.ore != "?":
                    if int(tile.ore) > 0:
                        res.append(Position(column_index, row_index))

        return res

    def get_random_position_without_hole(self):
        res = []

        for row_index in range(self.height):
            for column_index in range(self.width):
                tile = self.tiles[column_index][row_index]
                if not tile.is_hole and column_index != 0:
                    res.append(Position(column_index, row_index))

        return res[random.randint(0, len(res) - 1)]


class Game:
    def __init__(self):
        self.map = Map(30, 15)
        self.units = []
        self.my_robots = []
        self.radar_points = [
            Position(5, 4),
            Position(14, 4),
            Position(23, 4),
            Position(5, 9),
            Position(14, 9),
            Position(23, 9)
        ]
        self.target_queue = []

    def __str__(self):
        return "====\n---- units\n{}\n---- my robots\n{}".format(
            "\n".join([str(unit) for unit in self.units]),
            "\n".join([str(my_robot) for my_robot in self.my_robots])
        )

    def get_my_robot(self, id):
        res = [robot for robot in self.my_robots if robot.id == id]

        if len(res) == 0:
            return None
        else:
            return res[0]

    def get_orders(self):
        return "WAIT"

    def get_random_target(self):
        x = random.randint(1, map.width - 1)
        y = random.randint(0, map.height - 1)

        return Position(x, y)

    def get_best_radar_position(self):
        res = self.radar_points.pop(0)
        return res

    def get_best_target(self, my_robot_position):
        ore_positions_without_hole = self.map.get_ore_positions_without_hole()

        if len(ore_positions_without_hole) > 0:
            distances_tuples = [(ore_position, ore_position.distance_with(my_robot_position)) for ore_position in ore_positions_without_hole]
            res = sorted(distances_tuples, key=lambda tuple: tuple[1])
            return res[0][0]
        else:
            ore_positions = self.map.get_ore_positions()

            if len(ore_positions) > 0:
                distances_tuples = [(ore_position, ore_position.distance_with(my_robot_position)) for ore_position in ore_positions]
                res = sorted(distances_tuples, key=lambda tuple: tuple[1])
                return res[0][0]
            else:
                return self.map.get_random_position_without_hole()


if __name__ == '__main__':
    # height: size of the map
    width, height = [int(i) for i in input().split()]
    game = Game()

    # game loop
    while True:
        # my_score: Amount of ore delivered
        my_score, opponent_score = [int(i) for i in input().split()]

        map = Map(width, height)
        for i in range(height):
            inputs = input().split()

            for j in range(width):
                # ore: amount of ore or "?" if unknown
                # hole: 1 if cell has a hole
                ore = inputs[2 * j]
                hole = int(inputs[2 * j + 1])
                tile = Tile(ore, True if hole == 1 else False)
                map.add_tile(i, j, tile)

        game.map = map

        # entity_count: number of entities visible to you
        # radar_cooldown: turns left until a new radar can be requested
        # trap_cooldown: turns left until a new trap can be requested
        entity_count, radar_cooldown, trap_cooldown = [int(i) for i in input().split()]
        units = []
        for i in range(entity_count):
            # id: unique id of the entity
            # type 0 for your robot, 1 for other robot, 2 for radar, 3 for trap
            # y: position of the entity
            # item: if this entity is a robot, the item it is carrying (-1 for NONE, 2 for RADAR, 3 for TRAP, 4 for ORE)
            id, type, x, y, item = [int(j) for j in input().split()]
            unit = Unit(id, type, Position(x, y), item)

            if type == 0:
                my_robot = game.get_my_robot(id)

                if my_robot is None:
                    game.my_robots.append(unit)
                else:
                    my_robot.position = Position(x, y)
                    my_robot.item = item
            else:
                units.append(unit)

        game.units = units

        print_debug(game)

        new_robots = []
        for my_robot in game.my_robots:
            if my_robot.position.x == 0:
                my_robot.status = "IDLE"

            if my_robot.is_carrying_ore():
                my_robot.target = Position(0, my_robot.position.y)
                order = "MOVE {} {}".format(my_robot.target.x, my_robot.target.y)
            else:
                if my_robot.status == "IDLE":
                    if radar_cooldown == 0 and my_robot.item == -1:
                        order = "REQUEST RADAR"
                    elif trap_cooldown == 0 and my_robot.item == -1:
                        order = "REQUEST TRAP"
                    elif my_robot.item == 2:  # radar
                        my_robot.status = "DIG"
                        if len(game.radar_points) > 0:
                            my_robot.target = game.get_best_radar_position()
                        else:
                            my_robot.target = game.get_best_target(my_robot.position)
                        order = "DIG {} {}".format(my_robot.target.x, my_robot.target.y)
                    else:
                        my_robot.status = "DIG"
                        my_robot.target = game.get_best_target(my_robot.position)
                        order = "DIG {} {}".format(my_robot.target.x, my_robot.target.y)
                elif my_robot.status == "DIG" and map.is_hole(my_robot.target):
                    my_robot.target = game.get_best_target(my_robot.position)
                    order = "DIG {} {}".format(my_robot.target.x, my_robot.target.y)
                else:
                    order = "{} {} {}".format(my_robot.status, my_robot.target.x, my_robot.target.y)

            new_robots.append(my_robot)
            print(order)

        game.my_robots = new_robots
