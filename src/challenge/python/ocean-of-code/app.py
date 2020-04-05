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
        return math.sqrt(
            (that.x - self.x) * (that.x - self.x)
            + (that.y - self.y) * (that.y - self.y)
        )


class Unit:
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return "position: {}".format(self.position)


class Map:
    def __init__(self):
        self.width = 15
        self.height = 15
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
        with open(file_path, "r") as file:
            data = file.readlines()

        for row_index, row in enumerate(data):
            row = row.replace("\n", "")
            for column_index, tile_string in enumerate(row):
                self.add_tile(row_index, column_index, tile_string)

    def add_tile(self, row_index, column_index, tile_string):
        self.tiles[column_index].append(tile_string)

    def get_water_positions(self):
        res = []
        for row_index in range(self.height):
            for column_index in range(self.width):
                tile = self.tiles[column_index][row_index]
                if tile == ".":
                    res.append(Position(column_index, row_index))

        return res


class Game:
    def __init__(self, my_id):
        self.my_id = my_id
        self.map = None
        self.my_unit = None
        self.visited_positions = []

    def __str__(self):
        return "===={}".format(self.map)

    def get_random_direction(self):
        x = self.my_unit.position.x
        y = self.my_unit.position.y

        water_positions = self.map.get_water_positions()
        
        if len([water_position for water_position in water_positions if water_position.is_equal(Position(x + 1, y))]) > 0 and len([visited_position for visited_position in self.visited_positions if visited_position.is_equal(Position(x + 1, y))]) == 0:
            self.visited_positions.append(Position(x + 1, y))
            return "E"
        elif len([water_position for water_position in water_positions if water_position.is_equal(Position(x - 1, y))]) > 0 and len([visited_position for visited_position in self.visited_positions if visited_position.is_equal(Position(x - 1, y))]) == 0:
            self.visited_positions.append(Position(x - 1, y))
            return "W"
        elif len([water_position for water_position in water_positions if water_position.is_equal(Position(x, y - 1))]) > 0 and len([visited_position for visited_position in self.visited_positions if visited_position.is_equal(Position(x, y - 1))]) == 0:
            self.visited_positions.append(Position(x, y - 1))
            return "N"
        elif len([water_position for water_position in water_positions if water_position.is_equal(Position(x, y + 1))]) > 0 and len([visited_position for visited_position in self.visited_positions if visited_position.is_equal(Position(x, y + 1))]) == 0:
            self.visited_positions.append(Position(x, y + 1))
            return "S"
        else:
            return None


if __name__ == "__main__":

    width, height, my_id = [int(i) for i in input().split()]
    game = Game(my_id)

    # get map
    map = Map()
    for i in range(height):
        for column_index, tile in enumerate(input()):
            map.add_tile(i, column_index, tile)
    game.map = map

    # print_debug(game.map)

    starting_position = game.map.get_water_positions()[0]
    game.visited_positions.append(starting_position)
    print(f"{starting_position.x} {starting_position.y}")

    # game loop
    while True:
        (
            x,
            y,
            my_life,
            opp_life,
            torpedo_cooldown,
            sonar_cooldown,
            silence_cooldown,
            mine_cooldown,
        ) = [int(i) for i in input().split()]
        sonar_result = input()
        opponent_orders = input()

        game.my_unit = Unit(Position(x, y))

        direction = game.get_random_direction()
        if direction is not None:
            print(f"MOVE {direction} TORPEDO")
        else:
            game.visited_positions = [game.my_unit.position]
            print(f"SURFACE TORPEDO")
