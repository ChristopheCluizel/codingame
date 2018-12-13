import sys
import math
import random
import copy


def print_debug(description):
    print(description, file=sys.stderr)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def is_equal(self, that):
        return self.x == that.x and self.y == that.y


class Player:
    def __init__(self, id, cards_number, position, tile):
        """
        :param id: 0 = me, 1 = enemy
        :type id: integer
        :param cards_number:
        :type cards_number: integer
        :param position:
        :type position: Position
        :param tile:
        :type tile: Tile
        """
        self.id = id
        self.cards_number = cards_number
        self.position = position
        self.tile = tile

    def __str__(self):
        return "id: {}, cards_number: {}, position: {}, tile: {}".format(self.id, self.cards_number, self.position, self.tile)


class Item:
    def __init__(self, name, position, player_id):
        """
        :param name:
        :type name: string
        :param position:
        :type position: Position
        :param player_id: 0 = me, 1 = enemy
        :type player_id: integer
        """
        self.name = name
        self.position = position
        self.player_id = player_id

    def __str__(self):
        return "name: {}, position: {}, player_id: {}".format(self.name, self.position, self.player_id)


class Quest:
    def __init__(self, name, player_id):
        """
        :param name:
        :type name: string
        :param player_id: 0 = me, 1 = enemy
        :type player_id: integer
        """
        self.name = name
        self.player_id = player_id

    def __str__(self):
        return "name: {}, player_id: {}".format(self.name, self.player_id)


class Tile:
    def __init__(self, up, right, down, left):
        """
        :param up:
        :type up: boolean
        :param right:
        :type right: boolean
        :param down:
        :type down: boolean
        :param left:
        :type left: boolean
        """
        self.up = up
        self.right = right
        self.down = down
        self.left = left

    def __str__(self):
        return "{}{}{}{}".format(
            int(self.up),
            int(self.right),
            int(self.down),
            int(self.left)
        )


class Map:
    def __init__(self, size):
        self.tiles = None
        self.size = size
        self.flush()

    def __str__(self):
        res = ""
        for row_index in range(self.size):
            for column_index in range(self.size):
                res += str(self.tiles[column_index][row_index])
                res += "|"
            res = res[:-1]
            res += "\n"

        return res

    def flush(self):
        self.tiles = [[] for i in range(self.size)]

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            data = file.readlines()
        for row_index, row in enumerate(data):
            for column_index, tile_string in enumerate(row.split(" ")):
                self.add_tile(row_index, column_index, tile_string)

    def string_to_tile(self, tile_string):
        directions = list(tile_string)
        return Tile(bool(int(directions[0])),
                    bool(int(directions[1])),
                    bool(int(directions[2])),
                    bool(int(directions[3])))

    def add_tile(self, row_index, column_index, tile_string):
        self.tiles[column_index].append(self.string_to_tile(tile_string))

    def simulate_move(self, my_player_position, tile, insertion_id, direction):
        simulated_map = copy.deepcopy(self)
        item_position = Position(0, 0)
        new_my_player_position = my_player_position

        if direction == "RIGHT":
            item_position = Position(0, insertion_id)
            for column_index, column in enumerate(self.tiles):
                if column_index == 0:
                    simulated_map.tiles[column_index][insertion_id] = tile
                else:
                    simulated_map.tiles[column_index][insertion_id] = self.tiles[column_index - 1][insertion_id]
                if insertion_id == my_player_position.y:
                    new_my_player_position = Position(my_player_position.x + 1, insertion_id)
        if direction == "LEFT":
            item_position = Position(len(self.tiles[0]) - 1, insertion_id)
            for column_index, column in enumerate(self.tiles):
                if column_index == self.size - 1:
                    simulated_map.tiles[column_index][insertion_id] = tile
                else:
                    simulated_map.tiles[column_index][insertion_id] = self.tiles[column_index + 1][insertion_id]
                if insertion_id == my_player_position.y:
                    new_my_player_position = Position(my_player_position.x - 1, insertion_id)
        if direction == "UP":
            item_position = Position(insertion_id, len(self.tiles[0]) - 1)
            simulated_map.tiles[insertion_id] = self.tiles[insertion_id][1:] + [tile]
            if insertion_id == my_player_position.x:
                new_my_player_position = Position(insertion_id, my_player_position.y - 1)
        if direction == "DOWN":
            item_position = Position(insertion_id, 0)
            simulated_map.tiles[insertion_id] = [tile] + self.tiles[insertion_id][:-1]
            if insertion_id == my_player_position.x:
                new_my_player_position = Position(insertion_id, my_player_position.y + 1)
        return simulated_map, item_position, new_my_player_position


class Game:
    def __init__(self, turn, map, players, items, quests):
        """
        :param turn: 0 = push, 1 = move
        :type turn: integer
        :param map:
        :type map: Map
        :param players:
        :type players: list(Player)
        :param items:
        :type items: list(Item)
        :param quests:
        :type quests: list(Quest)
        """
        self.turn = turn
        self.map = map
        self.players = players
        self.items = items
        self.quests = quests
        self.graph = Graph()

    def __str__(self):
        return "==== Turn: {} ====\n---- Players ----\n{}\n---- Items ----\n{}\n---- Quests ----\n{}".format(
            self.which_turn(),
            "\n".join([str(player) for player in self.players]),
            "\n".join([str(item) for item in self.items]),
            "\n".join([str(quest) for quest in self.quests])
        )

    def synchronize_graph(self):
        self.graph = Graph()
        self.graph.map_to_graph(self.map)

    def get_my_player(self):
        return [player for player in self.players if player.id == 0][0]

    def get_enemy_player(self):
        return [player for player in self.players if player.id == 1][0]

    def get_my_quest_items(self, my_quests):
        my_quest_names = [quest.name for quest in my_quests]
        return [item for item in self.items if item.player_id == 0 and item.name in my_quest_names]

    def get_my_quests(self):
        my_quests = [quest for quest in self.quests if quest.player_id == 0]
        return my_quests

    def which_turn(self):
        if self.turn == 0:
            return "push"
        else:
            return "move"

    def flush_players(self):
        self.players = []

    def flush_items(self):
        self.items = []

    def flush_quests(self):
        self.quests = []

    def move_order_between_two_neighbours(self, node_index_start, node_index_end):
        node_position_start = self.graph.node_index_to_position(node_index_start, self.map.size)
        node_position_end = self.graph.node_index_to_position(node_index_end, self.map.size)

        start_tile = self.map.tiles[node_position_start.x][node_position_start.y]
        end_tile = self.map.tiles[node_position_end.x][node_position_end.y]

        if start_tile.left and end_tile.right and node_position_start.x > node_position_end.x:
            return "LEFT"
        if start_tile.right and end_tile.left and node_position_start.x < node_position_end.x:
            return "RIGHT"
        if start_tile.up and end_tile.down and node_position_start.y > node_position_end.y:
            return "UP"
        if start_tile.down and end_tile.up and node_position_start.y < node_position_end.y:
            return "DOWN"

    def move(self, my_node_index, my_quest_items):
        reachable_items = []
        for item in my_quest_items:
            target_item_node = self.graph.position_to_node_index(item.position, map.size)
            is_item_reachable = self.graph.is_reachable(my_node_index, target_item_node)
            if is_item_reachable:
                reachable_items.append(item)

        if len(reachable_items) != 0:
            target_item_node = self.graph.position_to_node_index(reachable_items[0].position, map.size)
            moves = []
            path = self.graph.get_path(my_node_index, target_item_node)
            # print_debug("Path: {}".format(path))
            for move_index, move_node in enumerate(path):
                move_order = self.move_order_between_two_neighbours(path[move_index], path[min(len(path) - 1, move_index + 1)])
                if move_order is not None:
                    moves.append(move_order)
            return "MOVE {}".format(" ".join(moves))
        else:
            # TODO: what move if item not reachable ?
            return "PASS"

    def get_push_order(self, my_player, my_quest_items):
        def get_best_insertion(item, my_player):
            for insertion_id in range(0, self.map.size - 1):
                for direction in ["DOWN", "UP", "RIGHT", "LEFT"]:
                    simulated_map, item_position, my_player_position = self.map.simulate_move(my_player.position, my_player.tile, insertion_id, direction)
                    simulated_graph = Graph()
                    simulated_graph.map_to_graph(simulated_map)
                    my_player_index = simulated_graph.position_to_node_index(my_player_position, map.size)
                    item_index = simulated_graph.position_to_node_index(item_position, map.size)

                    # print_debug("my_position: {}, my_index: {}, item_position: {}, item_index: {}".format(my_player_position,
                    #                                                                                       my_player_index,
                    #                                                                                       item_position,
                    #                                                                                       item_index))

                    is_reachable = simulated_graph.is_reachable(my_player_index, item_index)
                    # print_debug("{}, {} => {}".format(insertion_id, direction, is_reachable))
                    if is_reachable:
                        return insertion_id, direction

            return None, None

        def move_target_item(item, my_player):
            item_position = item.position
            # if our target item is in enemy's hand we move the enemy
            if item_position.is_equal(Position(-2, -2)):
                return move_enemy()

            # if we have the target item in hand
            if item_position.is_equal(Position(-1, -1)):
                insertion_id, direction = get_best_insertion(item, my_player)
                if insertion_id is None and direction is None:
                    # print_debug("Random insertion")
                    insertion_id = random.randint(0, self.map.size - 1)
                    direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

                # print_debug("Got item '{}' in hand and move: {} to the {}".format(item.name, insertion_id, direction))

                return "{} {}".format(insertion_id, direction)

            # try to eject our target item
            else:
                x = item.position.x
                y = item.position.y
                # (side of the board, distance from item to the side of the board)
                distances_from_side = [
                    ("LEFT", abs(x - 0)),
                    ("RIGHT", abs((self.map.size - 1) - x)),
                    ("UP", abs(y - 0)),
                    ("DOWN", abs((self.map.size - 1) - y))
                ]
                closest_side_tuple = sorted(distances_from_side, key=lambda tuple: tuple[1])[0]

                target_direction = closest_side_tuple[0]
                if target_direction in ["RIGHT", "LEFT"]:
                    target_position = y
                else:
                    target_position = x

                # print_debug("Move to eject my item '{}': row {} to the {}".format(item.name, target_position, target_direction))
                return "{} {}".format(target_position, target_direction)

        # TODO: improve by ejecting the enemy from board ?
        def move_enemy():
            enemy_player = self.get_enemy_player()
            enemy_position = enemy_player.position

            target_position = enemy_position.x
            target_direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

            # print_debug("Move enemy: {} to the {}".format(target_position, target_direction))

            return "{} {}".format(target_position, target_direction)

        def get_best_quest_item(items):
            """
            Find the best quest item to move (or get item in our hand)
            :param items:
            :type items: list(Item)
            :return:
            :rtype: Item
            """
            for item in items:  # select item in our hands
                if item.position.is_equal(Position(-1, -1)):
                    return item

            if len([item for item in items if not item.position.is_equal(Position(-2, -2))]) != 0:
                res = []
                for item in items:  # select item next to side of the board
                    x = item.position.x
                    y = item.position.y
                    minimum = min(abs(x - 0), abs((self.map.size - 1) - x), abs(y - 0), abs((self.map.size - 1) - y))
                    res.append((item, minimum))
                return sorted(res, key=lambda tuple: tuple[1])[0][0]
            else:
                # default
                return items[0]

        my_node_index = self.graph.position_to_node_index(my_player.position, map.size)
        reachable_items = []
        for item in my_quest_items:
            target_item_node = self.graph.position_to_node_index(item.position, map.size)
            is_item_reachable = self.graph.is_reachable(my_node_index, target_item_node)
            if is_item_reachable:
                reachable_items.append(item)

        order = ""
        if len(reachable_items) != 0:
            order = move_enemy()
        else:
            best_item = get_best_quest_item(my_quest_items)
            order = move_target_item(best_item, my_player)

        return "PUSH {}".format(order)

    def play(self):
        my_player = self.get_my_player()
        my_position = my_player.position
        my_node_index = self.graph.position_to_node_index(my_position, map.size)
        my_quests = self.get_my_quests()
        my_quest_items = self.get_my_quest_items(my_quests)

        if self.which_turn() == "push":
            return self.get_push_order(my_player, my_quest_items)
        else:
            return "{}".format(self.move(my_node_index, my_quest_items))


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_edge(self, node_id_1, node_id_2):
        if not self.are_connected(node_id_1, node_id_2):
            if node_id_1 in self.nodes:
                self.nodes[node_id_1].append(node_id_2)
            else:
                self.nodes[node_id_1] = [node_id_2]
            if node_id_2 in self.nodes:
                self.nodes[node_id_2].append(node_id_1)
            else:
                self.nodes[node_id_2] = [node_id_1]

    def remove_edge(self, node_id_1, node_id_2):
        if self.are_connected(node_id_1, node_id_2):
            self.nodes[node_id_1].remove(node_id_2)
            self.nodes[node_id_2].remove(node_id_1)

    def get_neighbours(self, node_id):
        if node_id in self.nodes:
            return self.nodes[node_id]
        else:
            return []

    def are_connected(self, node_id_1, node_id_2):
        return node_id_1 in self.nodes and node_id_2 in self.nodes[node_id_1]

    def position_to_node_index(self, position, map_size):
        return position.y * map_size + position.x

    def node_index_to_position(self, node_index, map_size):
        y = node_index // map_size
        x = node_index % map_size

        return Position(x, y)

    def map_to_graph(self, map):
        """
        :param map:
        :type map: Map
        :return:
        :rtype:
        """
        for column_index, column in enumerate(map.tiles):
            for row_index, tile in enumerate(column):
                left_tile_index = column_index - 1
                right_tile_index = column_index + 1
                up_tile_index = row_index - 1
                down_tile_index = row_index + 1

                if tile.left and (left_tile_index >= 0) and map.tiles[left_tile_index][row_index].right:
                    self.add_edge(
                        self.position_to_node_index(Position(column_index, row_index), map.size),
                        self.position_to_node_index(Position(left_tile_index, row_index), map.size)
                    )

                if tile.right and (right_tile_index <= map.size - 1) and map.tiles[right_tile_index][row_index].left:
                    self.add_edge(
                        self.position_to_node_index(Position(column_index, row_index), map.size),
                        self.position_to_node_index(Position(right_tile_index, row_index), map.size)
                    )

                if tile.up and (up_tile_index >= 0) and map.tiles[column_index][up_tile_index].down:
                    self.add_edge(
                        self.position_to_node_index(Position(column_index, row_index), map.size),
                        self.position_to_node_index(Position(column_index, up_tile_index), map.size)
                    )

                if tile.down and (down_tile_index <= map.size - 1) and map.tiles[column_index][down_tile_index].up:
                    self.add_edge(
                        self.position_to_node_index(Position(column_index, row_index), map.size),
                        self.position_to_node_index(Position(column_index, down_tile_index), map.size)
                    )

    def is_reachable(self, start_node_index, end_node_index):
        nodes_number = len(self.nodes)
        visited = [False] * nodes_number * nodes_number
        queue = []

        queue.append(start_node_index)
        visited[start_node_index] = True

        while queue:
            current_node_index = queue.pop(0)

            if current_node_index == end_node_index:
                return True
            for neighbour in self.get_neighbours(current_node_index):
                if not visited[neighbour]:
                    queue.append(neighbour)
                    visited[neighbour] = True
        return False

    def get_path(self, start_node, end_node):
        def get_path_utils(current_node, end_node, visited, path):
            visited[current_node] = True
            path.append(current_node)

            if current_node == end_node:
                return path
            else:
                for neighbour in self.get_neighbours(current_node):
                    if not visited[neighbour]:
                        res = get_path_utils(neighbour, end_node, visited, path)
                        if res is not None:
                            return res
            path.pop()
            visited[current_node] = False

        nodes_number = len(self.nodes)
        visited = [False] * nodes_number * nodes_number
        path = []

        return get_path_utils(start_node, end_node, visited, path)

    def __str__(self):
        return "{}".format(self.nodes)


if __name__ == '__main__':
    map = Map(7)
    game = Game(0, map, [], [], [])

    # game loop
    while True:
        turn_type = int(input())
        game.turn = turn_type

        # update map tiles
        map.flush()
        for row_index in range(7):
            for column_index, tile in enumerate(input().split()):
                map.add_tile(row_index, column_index, tile)
        game.synchronize_graph()

        # update players
        game.flush_players()
        for i in range(2):
            # num_player_cards: the total number of quests for a player (hidden and revealed)
            num_player_cards, player_x, player_y, player_tile = input().split()
            num_player_cards = int(num_player_cards)
            player_x = int(player_x)
            player_y = int(player_y)

            game.players.append(Player(i, num_player_cards, Position(player_x, player_y), map.string_to_tile(player_tile)))

        # update items
        game.flush_items()
        num_items = int(input())  # the total number of items available on board and on player tiles
        for i in range(num_items):
            item_name, item_x, item_y, item_player_id = input().split()
            item_x = int(item_x)
            item_y = int(item_y)
            item_player_id = int(item_player_id)

            game.items.append(Item(item_name, Position(item_x, item_y), item_player_id))

        # update quests
        game.flush_quests()
        num_quests = int(input())  # the total number of revealed quests for both players
        for i in range(num_quests):
            quest_item_name, quest_player_id = input().split()
            quest_player_id = int(quest_player_id)

            game.quests.append(Quest(quest_item_name, quest_player_id))

        # print_debug(game)
        # print_debug(map)
        # print_debug(game.graph)

        print(game.play())
