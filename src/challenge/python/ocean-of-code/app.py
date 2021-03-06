import sys
import math
import json
import uuid
import queue
import random
import re


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


class Node:
    def __init__(self, id, is_ocean):
        self.id = id
        self.is_ocean = is_ocean


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

    def get_node_ids(self, owners, state=None):
        if state is None:
            return [
                node.id for index, node in self.nodes.items() if node.owner in owners
            ]
        else:
            return [
                node.id
                for index, node in self.nodes.items()
                if node.owner in owners and node.state == state
            ]


class Game:
    def __init__(self, my_id):
        self.my_id = my_id
        self.map = None
        self.my_unit = None
        self.enemy_moves = []
        self.enemy_orders = []
        self.enemy_zone = None
        self.torpedo_cooldown = None
        self.sonar_cooldown = None
        self.silence_cooldown = None
        self.mine_cooldown = None
        self.mine_position_ids = []
        self.visited_ids = []
        self.graph = Graph()

    def __str__(self):
        return "===={}".format(self.map)

    def get_direction_from_target_position(self, my_position, target_position):
        target_x = target_position.x
        target_y = target_position.y
        x = my_position.x
        y = my_position.y

        if target_x == x:
            if target_y < y:
                return "N"
            else:
                return "S"
        if target_y == y:
            if target_x > x:
                return "E"
            else:
                return "W"

    def get_target_node_id_from_direction(self, my_position, direction):
        my_id = self.position_to_node_id(my_position)
        neighbours = self.graph.get_neighbours(my_id)
        neighbours_positions = [self.node_id_to_position(id) for id in neighbours]

        # print_debug([str(position) for position in neighbours_positions])

        if direction == "N":
            res_positions = [position for position in neighbours_positions if my_position.x == position.x and my_position.y > position.y]
        elif direction == "S":
            res_positions = [position for position in neighbours_positions if my_position.x == position.x and my_position.y < position.y]
        elif direction == "W":
            res_positions = [position for position in neighbours_positions if my_position.x > position.x and my_position.y == position.y]
        elif direction == "E":
            res_positions = [position for position in neighbours_positions if my_position.x < position.x and my_position.y == position.y]
        else:
            return None

        if len(res_positions) > 0:
            return self.position_to_node_id(res_positions[0])
        else:
            return None

    def get_random_direction(self):
        id = self.position_to_node_id(self.my_unit.position)
        neighbour_ids = self.graph.get_neighbours(id)

        if len(neighbour_ids) > 0:
            target_ids = list(set(neighbour_ids) - set(self.visited_ids))

            if len(target_ids) > 0:
                target_id = random.choice(target_ids)

                self.visited_ids.append(target_id)
                target_position = self.node_id_to_position(target_id)
                direction = self.get_direction_from_target_position(self.my_unit.position, target_position)
                return direction
        return None

    def get_direction_with_more_spaces(self, id):
        neighbour_ids = self.graph.get_neighbours(id)

        if len(neighbour_ids) > 0:
            target_ids = list(set(neighbour_ids) - set(self.visited_ids))

            if len(target_ids) > 0:
                target_id = sorted(
                    [
                        (target_id, self.count_free_spaces(target_id, self.visited_ids))
                        for target_id in target_ids
                    ],
                    key=lambda t: t[1],
                    reverse=True,
                )[0][0]

                # self.visited_ids.append(target_id)
                target_position = self.node_id_to_position(target_id)
                direction = self.get_direction_from_target_position(self.my_unit.position, target_position)
                return direction
        return None

    def count_free_spaces(self, node_id, visited_ids):
        total = 0

        seen = set(visited_ids)
        q = queue.Queue()
        q.put(node_id)

        while not q.empty():
            id = q.get()
            neighbours = self.graph.get_neighbours(id)

            if len(neighbours) > 0:
                for neighbour_id in neighbours:
                    if neighbour_id not in seen:
                        total = total + 1
                        seen.add(neighbour_id)
                        q.put(neighbour_id)

        return total

    def get_follow_the_side_direction(self):
        """not working
        
        Returns:
            [type] -- [description]
        """
        id = self.position_to_node_id(self.my_unit.position)
        neighbour_ids = self.graph.get_neighbours(id)

        if len(neighbour_ids) > 0:
            target_ids = list(set(neighbour_ids) - set(self.visited_ids))

            if len(target_ids):
                target_positions = [self.node_id_to_position(id) for id in target_ids]
                sorted_1 = sorted(
                    target_positions, key=lambda position: (position.y, position.x)
                )
                # sorted_2 = sorted(sorted1, key=lambda position: position.x)
                target_position = sorted_1[0]
                target_id = self.position_to_node_id(target_position)
                self.visited_ids.append(target_id)
                direction = self.get_direction_from_target_position(self.my_unit.position, target_position)
                return direction
        return None

    def map_to_graph(self, map):
        graph = Graph()

        for y in range(0, map.height):
            for x in range(0, map.width):
                character = map.tiles[x][y]
                node_id = x + y * map.width

                if character == ".":
                    is_ocean = True
                else:
                    is_ocean = False

                node = Node(node_id, is_ocean)
                graph.add_node(node)

                if x + 1 < map.width and map.tiles[x + 1][y] != "x":
                    graph.add_edge(
                        node_id, self.position_to_node_id(Position(x + 1, y), map.width)
                    )
                if x - 1 >= 0 and map.tiles[x - 1][y] != "x":
                    graph.add_edge(
                        node_id, self.position_to_node_id(Position(x - 1, y), map.width)
                    )
                if y + 1 < map.height and map.tiles[x][y + 1] != "x":
                    graph.add_edge(
                        node_id, self.position_to_node_id(Position(x, y + 1), map.width)
                    )
                if y - 1 >= 0 and map.tiles[x][y - 1] != "x":
                    graph.add_edge(
                        node_id, self.position_to_node_id(Position(x, y - 1), map.width)
                    )

        return graph

    def position_to_node_id(self, position, map_width=15):
        return position.x + position.y * map_width

    def node_id_to_position(self, id, map_width=15):
        x = id % map_width
        y = id // map_width

        return Position(x, y)

    def get_random_starting_position(self):
        ocean_node_ids = [
            node.id for index, node in self.graph.nodes.items() if node.is_ocean
        ]
        return game.node_id_to_position(random.choice(ocean_node_ids))

    def get_enemy_move(self, orders):
        """Extract the movement from row orders

        Arguments:
            orders {string} -- a string with several orders separated by |
        """

        # TODO: approximate by saying that the enemy don't move before or after surfacing
        if "SURFACE" in orders:
            p = re.compile("SURFACE [1-9]")
            res = p.findall(orders)[0]
            self.enemy_zone = int(res.split("SURFACE ")[-1])
            self.enemy_moves = []
            return None

        # TODO: approximate by saying that the enemy don't move before or after silencing, that he make a silence of 1 and in the same direction than his previous movement
        if orders == "SILENCE":
            if len(self.enemy_moves) > 0:
                return self.enemy_moves[-1]
            else:
                return "N"

        p = re.compile(" {1}[EWNS]{1} *")
        res = p.findall(orders)

        if len(res) > 0:
            return res[0].strip()
        else:
            return None

    def detect_enemy(self, moves):
        """List of direction

        Arguments:
            moves {list[string]} -- list of cardinal direction

        Returns:
            [Position] -- The position of the enemy
        """
        starting_nodes_ids = []

        if self.enemy_zone is None:
            starting_nodes_ids = [
                node.id for index, node in self.graph.nodes.items() if node.is_ocean
            ]
        else:
            starting_nodes_ids = self.get_ids_in_zone(self.enemy_zone)

        possible_starting_node_ids = []
        possible_current_node_ids = []

        for starting_node_id in starting_nodes_ids:
            simulation_moves, estimated_current_node_id = self.simulate_moves(starting_node_id, moves)

            if simulation_moves:
                possible_starting_node_ids.append(starting_node_id)
                possible_current_node_ids.append(estimated_current_node_id)

        return [self.node_id_to_position(id) for id in possible_current_node_ids]

    def simulate_moves(self, starting_node_id, moves):
        current_node_id = starting_node_id
        visited_node_ids = [current_node_id]

        for move_direction in moves:
            target_id = self.get_target_node_id_from_direction(self.node_id_to_position(current_node_id), move_direction)

            neighbour_ids = self.graph.get_neighbours(current_node_id)
            if target_id not in list(set(neighbour_ids) - set(visited_node_ids)):
                return (False, None)
            else:
                current_node_id = target_id
                visited_node_ids.append(target_id)
        return (True, visited_node_ids[-1])

    def get_ids_in_zone(self, zone):
        """[summary]

        Arguments:
            zone {int} -- [description]
        """
        res = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
        }

        for x in range(14):
            for y in range(14):
                if x <= 4 and y <= 4:
                    res[1].append(Position(x, y))
                elif x <= 9 and y <= 4:
                    res[2].append(Position(x, y))
                elif x > 9 and y <= 4:
                    res[3].append(Position(x, y))
                elif x <= 4 and y <= 9:
                    res[4].append(Position(x, y))
                elif x <= 9 and y <= 9:
                    res[5].append(Position(x, y))
                elif x > 9 and y <= 9:
                    res[6].append(Position(x, y))
                elif x <= 4 and y > 9:
                    res[7].append(Position(x, y))
                elif x <= 9 and y > 9:
                    res[8].append(Position(x, y))
                elif x > 9 and y > 9:
                    res[9].append(Position(x, y))
        return [self.position_to_node_id(position) for position in res[zone]]

    def get_enemy_in_range_positions(self, estimated_positions):
        distances_positions = [(position, self.my_unit.position.distance_with(position)) for position in estimated_positions]

        if len(distances_positions) > 0:
            in_range_positions = [t for t in distances_positions if t[1] <= 4]
            return in_range_positions
        else:
            return []

    def get_direction_towards_enemy(self, estimated_positions):
        target_ids = list(set([self.position_to_node_id(position) for position in estimated_positions]) - set(self.visited_ids))
        target_positions = [self.node_id_to_position(id) for id in target_ids]
        distances_positions = [(position, self.my_unit.position.distance_with(position)) for position in target_positions]

        if len(distances_positions) > 0:
            closest_position = sorted(distances_positions, key=lambda t: t[1])[0][0]
            target_id = self.position_to_node_id(closest_position)
            self.visited_ids.append(target_id)
            print_debug(f"toward enemy: {closest_position}")
            # TODO: line below doesn't work. To move towards the enemy, use the graph
            return self.get_direction_from_target_position(self.my_unit.position, closest_position)
        else:
            print_debug("random")
            return self.get_direction_with_more_spaces(self.position_to_node_id(self.my_unit.position))

    def get_straight_move(self, starting_node_id, direction, nb_of_moves):
        """[summary]

        Arguments:
            starting_node_id {[type]} -- [description]
            direction {[type]} -- [description]
            nb_of_moves {[type]} -- [description]

        Returns:
            int -- the node id at the end of the straight move
        """
        current_node_id = starting_node_id

        for i in range(nb_of_moves):
            current_position = self.node_id_to_position(current_node_id)
            next_node_id = game.get_target_node_id_from_direction(current_position, direction)

            if next_node_id is None or next_node_id in self.visited_ids:
                return None
            else:
                current_node_id = next_node_id

        return current_node_id


if __name__ == "__main__":

    width, height, my_id = [int(i) for i in input().split()]
    game = Game(my_id)

    # get map
    map = Map()
    for i in range(height):
        for column_index, tile in enumerate(input()):
            map.add_tile(i, column_index, tile)
    game.map = map
    game.graph = game.map_to_graph(map)

    # print_debug(game.graph)

    starting_position = game.get_random_starting_position()
    game.visited_ids.append(game.position_to_node_id(starting_position))

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

        game.enemy_orders.append(opponent_orders)
        enemy_move = game.get_enemy_move(opponent_orders)

        if enemy_move is not None:
            game.enemy_moves.append(enemy_move)
            game.enemy_zone = None

        game.my_unit = Unit(Position(x, y))
        game.silence_cooldown = silence_cooldown
        game.torpedo_cooldown = torpedo_cooldown
        game.silence_cooldown = silence_cooldown
        game.mine_cooldown = mine_cooldown

        enemy_positions = game.detect_enemy(game.enemy_moves)

        if len(enemy_positions) == 0 and len(game.enemy_moves) > 0:
            game.enemy_moves = []

        # print_debug(game.enemy_moves)
        # print_debug(f"torpedo cooldown: {game.torpedo_cooldown}")
        # print_debug(f"silence cooldown: {game.silence_cooldown}")
        # print_debug(game.enemy_moves)
        print_debug([str(position) for position in enemy_positions])

        direction = game.get_direction_with_more_spaces(game.position_to_node_id(game.my_unit.position))
        # direction = game.get_direction_towards_enemy(enemy_positions)
        print_debug(f"direction: {direction}")

        all_orders = ""
        fire_order = ""
        mine_order = ""
        move_order = ""
        charge_order = ""
        target_positions_distance = game.get_enemy_in_range_positions(enemy_positions)

        if len(target_positions_distance) == 0:
            target_position = None
        elif len(enemy_positions) <= 4:
            target_position = sorted(target_positions_distance, key=lambda t: t[1], reverse=True)[0][0]
        else:
            target_position = None

        # fire order
        if target_position is not None and game.torpedo_cooldown == 0:
            fire_order = f"TORPEDO {target_position.x} {target_position.y}"

        # TODO: don't trigger mine if I am in mine diagonal
        # mine trigger
        if len(enemy_positions) <= 20:
            enemy_ids = [game.position_to_node_id(position) for position in enemy_positions]

            for enemy_id in enemy_ids:
                for mine_id in game.mine_position_ids:
                    mine_neighbours_ids = game.graph.get_neighbours(mine_id)

                    my_position_id = game.position_to_node_id(game.my_unit.position)
                    if (enemy_id == mine_id or enemy_id in mine_neighbours_ids) and (my_position_id != mine_id and my_position_id not in mine_neighbours_ids) and len(mine_order) == 0:
                        game.mine_position_ids.remove(mine_id)
                        mine_position = game.node_id_to_position(mine_id)
                        print_debug(f"FIRE: {mine_position}")
                        mine_order = f"TRIGGER {mine_position.x} {mine_position.y}"

        # mine drop
        if game.mine_cooldown == 0 and len(mine_order) == 0 and direction is not None:
            mine_node_id = game.get_target_node_id_from_direction(game.my_unit.position, direction)
            game.mine_position_ids.append(mine_node_id)
            mine_order = f"MINE {direction}"

        my_current_position = game.my_unit.position

        # move order
        if direction is not None:
            if game.silence_cooldown == 0:
                all_res = []

                for nb_of_moves in [2]:
                    for straight_line_direction in ["N", "S", "W", "E"]:
                        final_node_id = game.get_straight_move(game.position_to_node_id(my_current_position), straight_line_direction, nb_of_moves)

                        if final_node_id is not None:
                            all_res.append((final_node_id, straight_line_direction, nb_of_moves))

                if len(all_res) > 0:
                    selected_move = random.choice(all_res)
                    first_node_id = game.get_target_node_id_from_direction(my_current_position, selected_move[1])
                    second_node_id = game.get_target_node_id_from_direction(game.node_id_to_position(first_node_id), selected_move[1])
                    game.visited_ids.append(first_node_id)
                    game.visited_ids.append(second_node_id)
                    move_order = f"SILENCE {selected_move[1]} {selected_move[2]}"
                else:
                    game.visited_ids.append(game.get_target_node_id_from_direction(my_current_position, direction))
                    move_order = f"MOVE {direction}"
            else:
                game.visited_ids.append(game.get_target_node_id_from_direction(my_current_position, direction))
                move_order = f"MOVE {direction}"
        else:
            game.visited_ids = [game.position_to_node_id(my_current_position)]
            move_order = f"SURFACE"

        # charge order
        if game.torpedo_cooldown != 0:
            charge_order = f"TORPEDO"
        elif game.mine_cooldown != 0 and random.random() > 0.67:
            charge_order = f"MINE"
        else:
            charge_order = f"SILENCE"

        if len(fire_order) > 0:
            all_orders = f"{fire_order}|"

        if len(mine_order) > 0:
            all_orders += f"{mine_order}|"

        all_orders += f"{move_order}"

        if "MOVE" in move_order:
            all_orders += f" {charge_order}"

        print(all_orders)
