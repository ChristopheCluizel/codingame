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
        return math.sqrt(
            (that.x - self.x) * (that.x - self.x)
            + (that.y - self.y) * (that.y - self.y)
        )


class Pellet:
    def __init__(self, position, score):
        self.position = position
        self.score = score


class Pac:
    def __init__(self, id, position):
        self.id = id
        self.position = position


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


class Game:
    def __init__(self, map):
        self.map = map
        self.my_pacs = []
        self.pellets = []

    def __str__(self):
        return ""

    def get_best_pellet(self):
        sorted_pellets = sorted(
            self.pellets, key=lambda pellet: pellet.score, reverse=True
        )

        if len(sorted_pellets) > 0:
            return sorted_pellets[0]
        else:
            None


if __name__ == "__main__":
    # Grab the pellets as fast as you can!

    # width: size of the grid
    # height: top left corner is (x=0, y=0)
    width, height = [int(i) for i in input().split()]
    map = Map(width, height)
    game = Game(map)

    # for row_index in range(7):
    #     for column_index, tile in enumerate(input()):
    #         map.add_tile(row_index, column_index, tile)

    for row_index in range(height):
        for column_index, tile in enumerate(input()):
            map.add_tile(row_index, column_index, tile)

    # print_debug(map)

    # game loop
    while True:
        my_score, opponent_score = [int(i) for i in input().split()]
        visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
        for i in range(visible_pac_count):
            # pac_id: pac number (unique within a team)
            # mine: true if this pac is yours
            # x: position in the grid
            # y: position in the grid
            # type_id: unused in wood leagues
            # speed_turns_left: unused in wood leagues
            # ability_cooldown: unused in wood leagues
            (
                pac_id,
                mine,
                x,
                y,
                type_id,
                speed_turns_left,
                ability_cooldown,
            ) = input().split()
            pac_id = int(pac_id)
            mine = mine != "0"
            x = int(x)
            y = int(y)
            speed_turns_left = int(speed_turns_left)
            ability_cooldown = int(ability_cooldown)

            if mine:
                game.my_pacs.append(Pac(pac_id, Position(x, y)))

        visible_pellet_count = int(input())  # all pellets in sight
        game.pellets = []
        for i in range(visible_pellet_count):
            # value: amount of points this pellet is worth
            x, y, value = [int(j) for j in input().split()]
            game.pellets.append(Pellet(Position(x, y), value))

        best_pellet = game.get_best_pellet()

        # MOVE <pacId> <x> <y>
        print(f"MOVE 0 {best_pellet.position.x} {best_pellet.position.y}")
