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
        return abs(that.x - self.x) + abs(that.y - self.y)

    def in_positions_list(self, positions):
        res = False

        for position in positions:
            if self.is_equal(position):
                res = True
                break
        return res


class Pellet:
    def __init__(self, position, score):
        self.position = position
        self.score = score


class Pac:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.positions = []
        self.current_position = None
        self.speedTurnsLeft = 0
        self.abilityCooldown = 0

    def __str__(self):
        return f"id: {self.id}, current_position: {self.current_position}, type: {self.type}, all_positions: {','.join([str(position) for position in self.positions])}"

    def move(self, new_position):
        self.current_position = new_position
        self.positions.append(new_position)

    def is_blocked(self):
        if len(self.positions) < 3:
            return False
        else:
            # print_debug([str(position) for position in self.positions])
            return self.current_position.is_equal(
                self.positions[-2]
            ) and self.current_position.is_equal(self.positions[-3])

    # TODO: handle if the pac has already the good type
    def switch(self, enemy_type):
        # print_debug(f"enemy type: {enemy_type}")
        if enemy_type == "ROCK":
            new_type = "PAPER"
        elif enemy_type == "PAPER":
            new_type = "SCISSORS"
        else:
            new_type = "ROCK"
        return new_type


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

    def get_empty_positions(self):
        positions = []
        for row_index in range(self.height):
            for column_index in range(self.width):
                if self.tiles[column_index][row_index] == " ":
                    positions.append(Position(column_index, row_index))
        return positions

    def get_extreme_positions(self, current_position):
        empty_positions = self.get_empty_positions()
        return [empty_positions[0], empty_positions[-1]]

    def get_visible_positions(self, current_position):
        res = []
        current_x = current_position.x
        current_y = current_position.y

        for y in range(current_y, -1, -1):
            if self.tiles[current_x][y] == " ":
                res.append(Position(current_x, y))
            else:
                break

        for y in range(current_y, self.height):
            if self.tiles[current_x][y] == " ":
                res.append(Position(current_x, y))
            else:
                break

        for x in range(current_x, self.width):
            if self.tiles[x][current_y] == " ":
                res.append(Position(x, current_y))
            else:
                break

        for x in range(current_x, -1, -1):
            if self.tiles[x][current_y] == " ":
                res.append(Position(x, current_y))
            else:
                break

        return res


class Game:
    def __init__(self, map):
        self.map = map
        self.my_pacs = []
        self.enemy_pacs = []
        self.pellets = []
        self.targeted_positions = []
        self.empty_positions = []

    def __str__(self):
        return ""

    def delete_my_pac(self, pac_id):
        self.my_pacs = [pac for pac in self.my_pacs if pac.id != pac_id]

    def delete_enemy_pac(self, pac_id):
        self.enemy_pacs = [pac for pac in self.enemy_pacs if pac.id != pac_id]

    def get_best_pellets(self):
        sorted_pellets = sorted(self.pellets, key=lambda pellet: pellet.score)

        return sorted_pellets

    def get_best_closest_scored_pellets(self, current_position):
        best_scored_pellets = [
            pellet
            for pellet in self.pellets
            if pellet.score == 10
            and not pellet.position.in_positions_list(self.targeted_positions)
        ]

        pellets_distances = [
            (pellet, current_position.distance_with(pellet.position))
            for pellet in best_scored_pellets
        ]
        sorted_pellets_distances = sorted(
            pellets_distances, key=lambda tuple: tuple[1], reverse=True
        )

        return [tuple[0] for tuple in sorted_pellets_distances]

    def get_closest_pellets(self, current_position):
        pellets_distances = [
            (pellet, current_position.distance_with(pellet.position))
            for pellet in self.pellets
            if not pellet.position.in_positions_list(self.targeted_positions)
        ]
        sorted_pellets_distances = sorted(
            pellets_distances, key=lambda tuple: tuple[1], reverse=True
        )

        return [tuple[0] for tuple in sorted_pellets_distances]

    def get_random_pellests(self):
        temp = [pellet for pellet in self.pellets]
        random.shuffle(temp)
        return temp

    def get_farest_unexplored_position(self, current_position, explored_positions):
        unexplored_positions = []

        for empty_position in self.map.get_empty_positions():
            equal = False
            for explored_position in explored_positions:
                if empty_position.is_equal(explored_position):
                    equal = True
                    break
            if not equal:
                unexplored_positions.append(empty_position)

        positions_distances = [
            (position, current_position.distance_with(position))
            for position in unexplored_positions
        ]

        res = sorted(positions_distances, key=lambda tuple: tuple[1], reverse=True)

        if len(res) > 0:
            return res[0][0]
        else:
            return current_position

    def get_closest_enemy_pac(self, current_position):
        enemy_pacs = self.enemy_pacs

        if len(enemy_pacs) > 0:
            distances_tuples = [
                (enemy_pac, current_position.distance_with(enemy_pac.current_position))
                for enemy_pac in enemy_pacs
            ]
            sorted_distance_tuples = sorted(
                distances_tuples, key=lambda tuple: tuple[1]
            )

            enemy_pac = sorted_distance_tuples[0][0]
            enemy_distance = sorted_distance_tuples[0][1]

            # print_debug(
            #     f"enemy pac {enemy_pac.id} has a distance of {enemy_distance} with my current position {current_position}"
            # )

            if enemy_distance < 3:
                return enemy_pac
            else:
                return None
        else:
            return None

    def update_empty_position(self, current_position):
        visible_pellets_positions = [pellet.position for pellet in self.pellets]
        visible_positions = self.map.get_visible_positions(current_position)

        for visible_position in visible_positions:
            if not visible_position.in_positions_list(
                visible_pellets_positions
            ) and not visible_position.in_positions_list(self.empty_positions):
                self.empty_positions.append(visible_position)

    def get_random_optimized_position(self):
        target_positions = []
        empty_positions = self.map.get_empty_positions()
        no_pellet_positions = self.empty_positions

        for empty_position in empty_positions:
            if not empty_position.in_positions_list(no_pellet_positions):
                target_positions.append(empty_position)

        return random.choice(target_positions)


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
        my_existing_pack_ids = []
        enemy_existing_pack_ids = []
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
                my_existing_pack_ids.append(pac_id)
                temp_pacs = [pac for pac in game.my_pacs if pac.id == pac_id]

                if len(temp_pacs) == 0:
                    game.my_pacs.append(Pac(pac_id, type_id))
                    game.my_pacs[-1].move(Position(x, y))
                else:
                    my_pac = temp_pacs[0]
                    my_pac.speedTurnsLeft = speed_turns_left
                    my_pac.abilityCooldown = ability_cooldown
                    my_pac.move(Position(x, y))
            else:
                enemy_existing_pack_ids.append(pac_id)
                temp_pacs = [pac for pac in game.enemy_pacs if pac.id == pac_id]

                if len(temp_pacs) == 0:
                    game.enemy_pacs.append(Pac(pac_id, type_id))
                    game.enemy_pacs[-1].move(Position(x, y))
                else:
                    enemy = temp_pacs[0]
                    enemy.type = type_id
                    enemy.speedTurnsLeft = speed_turns_left
                    enemy.abilityCooldown = ability_cooldown
                    enemy.move(Position(x, y))

        # print_debug("==== My pacs ====")
        # for pac in game.my_pacs:
        #     print_debug(pac)

        print_debug("==== Enemy pacs ====")
        for pac in game.enemy_pacs:
            print_debug(pac)

        # print_debug([str(position) for position in game.empty_positions])

        # remove died pacs
        pac_ids_to_delete = list(
            set([pac.id for pac in game.my_pacs]) - set(my_existing_pack_ids)
        )
        for pac_id in pac_ids_to_delete:
            game.delete_my_pac(pac_id)

        pac_ids_to_delete = list(
            set([pac.id for pac in game.enemy_pacs]) - set(enemy_existing_pack_ids)
        )
        for pac_id in pac_ids_to_delete:
            game.delete_enemy_pac(pac_id)

        visible_pellet_count = int(input())  # all pellets in sight
        game.pellets = []
        for i in range(visible_pellet_count):
            # value: amount of points this pellet is worth
            x, y, value = [int(j) for j in input().split()]
            game.pellets.append(Pellet(Position(x, y), value))

        orders = []
        game.targeted_positions = []
        for pac in game.my_pacs:
            game.update_empty_position(pac.current_position)
            closest_enemy_pac = game.get_closest_enemy_pac(pac.current_position)
            # print_debug(closest_enemy_pac)

            if (
                closest_enemy_pac is not None
                and pac.abilityCooldown == 0
                and pac.switch(closest_enemy_pac.type) != pac.type
            ):
                new_type = pac.switch(closest_enemy_pac.type)
                pac.type = new_type
                print_debug(f"pac {pac.id} switches to {new_type}")
                orders.append(f"SWITCH {pac.id} {new_type}")
            elif pac.is_blocked():
                print_debug(f"pac {pac.id} is blocked")
                extreme_position = random.choice(
                    game.map.get_extreme_positions(pac.current_position)
                )
                if random.random() > 0.6:
                    best_position = extreme_position
                else:
                    best_position = pac.current_position

                best_pellet = Pellet(best_position, -1,)
                orders.append(
                    f"MOVE {pac.id} {best_pellet.position.x} {best_pellet.position.y}"
                )
            else:
                # MOVE order
                best_pellets = game.get_best_closest_scored_pellets(
                    pac.current_position
                )
                if len(best_pellets) > 0:
                    print_debug(f"pac {pac.id} go to closest BIG pellet")

                    # SPEED order
                    if pac.abilityCooldown == 0:
                        orders.append(f"SPEED {pac.id}")
                    else:
                        best_pellet = best_pellets.pop()
                        game.targeted_positions.append(
                            Position(best_pellet.position.x, best_pellet.position.y)
                        )
                        orders.append(
                            f"MOVE {pac.id} {best_pellet.position.x} {best_pellet.position.y}"
                        )
                else:
                    best_pellets = game.get_closest_pellets(pac.current_position)
                    if len(best_pellets) > 0:
                        print_debug(f"pac {pac.id} go to closest pellet")
                        best_pellet = best_pellets.pop()
                        game.targeted_positions.append(
                            Position(best_pellet.position.x, best_pellet.position.y)
                        )
                        orders.append(
                            f"MOVE {pac.id} {best_pellet.position.x} {best_pellet.position.y}"
                        )
                    else:
                        print_debug(f"pac {pac.id} go to unexplored position")
                        if pac.abilityCooldown == 0:
                            orders.append(f"SPEED {pac.id}")
                        else:
                            best_position = game.get_random_optimized_position()
                            game.targeted_positions.append(best_position)
                            best_pellet = Pellet(best_position, -1,)
                            orders.append(
                                f"MOVE {pac.id} {best_pellet.position.x} {best_pellet.position.y}"
                            )

        string_orders = "|".join(orders)
        print(string_orders)
