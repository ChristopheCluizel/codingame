import sys
import math
import random


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

    def get_my_next_request_item(self):
        return [item for item in self.items if item.player_id == 0][0]

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

    def move(self):
        my_player = self.get_my_player()
        my_position = my_player.position
        my_node_index = self.graph.position_to_node_index(my_position, map.size)
        target_item = self.get_my_next_request_item()
        target_item_node = self.graph.position_to_node_index(target_item.position, map.size)

        is_item_reachable = self.graph.is_reachable(my_node_index, target_item_node)

        # print_debug("item: {} in {} reachable ? {}".format(target_item.name,
        #                                                    target_item.position,
        #                                                    is_item_reachable))

        if is_item_reachable:
            moves = []
            path = self.graph.get_path(my_node_index, target_item_node)
            # print_debug("Path: {}".format(path))
            for move_index, move_node in enumerate(path):
                move_order = self.move_order_between_two_neighbours(path[move_index], path[min(len(path) - 1, move_index + 1)])
                if move_order is not None:
                    moves.append(move_order)
            # print_debug("move orders: {}".format(moves))
            return "MOVE {}".format(" ".join(moves))
        else:
            # TODO: what move if item not reachable ?
            return "PASS"

    def get_push_order(self):
        random_index = random.randint(0, map.size - 1)
        random_direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

        return "PUSH {} {}".format(random_index, random_direction)

    def play(self):
        if self.which_turn() == "push":
            return self.get_push_order()
        else:
            return "{}".format(self.move())


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
