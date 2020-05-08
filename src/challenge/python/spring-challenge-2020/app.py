import sys
import math
import json
import uuid
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


class Pellet:
    def __init__(self, position, score):
        self.position = position
        self.score = score


class Pac:
    def __init__(self, id):
        self.id = id
        self.positions = []
        self.current_position = None

    def __str__(self):
        return f"id: {self.id}, current_position: {self.current_position}, all_positions: {','.join([str(position) for position in self.positions])}"

    def move(self, new_position):
        self.current_position = new_position
        self.positions.append(new_position)

    def is_blocked(self):
        if len(self.positions) < 2:
            return False
        else:
            return self.current_position.is_equal(self.positions[-2])


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
        self.orders = []

    def __str__(self):
        return ""

    def get_best_pellets(self):
        sorted_pellets = sorted(self.pellets, key=lambda pellet: pellet.score)

        return sorted_pellets

    def get_closest_pellets(self, current_position):
        pellets_distances = [
            (pellet, current_position.distance_with(pellet.position))
            for pellet in self.pellets
        ]
        sorted_pellets_distances = sorted(
            pellets_distances, key=lambda tuple: tuple[1], reverse=True
        )

        return [tuple[0] for tuple in sorted_pellets_distances]

    def get_random_pellests(self):
        temp = [pellet for pellet in self.pellets]
        random.shuffle(temp)
        return temp


if __name__ == "__main__":
    # Grab the pellets as fast as you can!

    # width: size of the grid
    # height: top left corner is (x=0, y=0)
    width, height = [int(i) for i in input().split()]
    map = Map(width, height)
    game = Game(map)

    for row_index in range(height):
        for column_index, tile in enumerate(input()):
            map.add_tile(row_index, column_index, tile)

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
                temp_pacs = [pac for pac in game.my_pacs if pac.id == pac_id]

                if len(temp_pacs) == 0:
                    # print_debug(f"initialise pac {pac_id}")
                    game.my_pacs.append(Pac(pac_id))
                    game.my_pacs[-1].move(Position(x, y))
                else:
                    # print_debug(f"update pac {pac_id}")
                    my_pac = temp_pacs[0]
                    my_pac.move(Position(x, y))

        # for pac in game.my_pacs:
        #     print_debug(pac)

        visible_pellet_count = int(input())  # all pellets in sight

        game.pellets = []
        for i in range(visible_pellet_count):
            # value: amount of points this pellet is worth
            x, y, value = [int(j) for j in input().split()]
            game.pellets.append(Pellet(Position(x, y), value))

        orders = []

        for pac in game.my_pacs:
            best_pellets = game.get_closest_pellets(pac.current_position)
            best_pellet = best_pellets.pop()
            if pac.is_blocked():
                best_pellet = game.get_random_pellests()[0]
            orders.append(
                f"MOVE {pac.id} {best_pellet.position.x} {best_pellet.position.y}"
            )

        string_orders = "|".join(orders)
        print(string_orders)
