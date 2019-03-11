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


class Chef:
    def __init__(self):
        self.position = None
        self.item = "NONE"

    def __str__(self):
        return "Position: {}, item: {}".format(self.position, self.item)


class Command:
    def __init__(self, id, name, award):
        self.id = id
        self.name = name
        self.award = award

    def __str__(self):
        return "Command id: {}, name: {}, award: {}".format(self.id, self.name, self.award)


class Recipe:
    def __init__(self, id):
        self.id = id
        self.orders = self.initialize_orders(id)

    def initialize_orders(self, id):
        if id == "DISH-BLUEBERRIES-ICE_CREAM" or "DISH-BLUEBERRIES-ICE_CREAM":
            orders = [
                {"priority": 0, "action": "take", "item": "dish", "location": "dish_washer", "validation": "DISH"},
                {"priority": 1, "action": "take", "item": "blueberry", "location": "blueberry_crate", "validation": "BLUEBERRIES"},
                {"priority": 1, "action": "take", "item": "ice_cream", "location": "ice_cream_crate", "validation": "ICE_CREAM"},
                {"priority": 2, "action": "drop", "item": "window", "location": "window", "validation": "NONE"}
            ]
        else:
            orders = []

        return orders


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
        with open(file_path, 'r') as file:
            data = file.readlines()

        for row_index, row in enumerate(data):
            row = row.replace("\n", "")
            for column_index, tile_string in enumerate(row):
                self.add_tile(row_index, column_index, tile_string)

    def add_tile(self, row_index, column_index, tile_string):
        self.tiles[column_index].append(tile_string)

    def find_position(self, item_location):
        """

        :param item_location: "dish_washer", "window", "blueberry_crate", "ice_cream_crate"
        :type item_location: string
        :return:
        :rtype: Position
        """

        def find_letter(letter):
            for x in range(self.width):
                for y in range(self.height):
                    if self.tiles[x][y] == letter:
                        return Position(x, y)

        mapping = {
            "dish_washer": "D",
            "window": "W",
            "blueberry_crate": "B",
            "ice_cream_crate": "I"
        }

        return find_letter(mapping[item_location])


class Game:
    def __init__(self, map, total_commands, commands):
        self.map = map
        self.total_commands = total_commands
        self.commands = commands
        self.current_commands = []
        self.current_command = None
        self.remaining_turn = 0
        self.my_chef = Chef()
        self.other_chef = Chef()
        self.orders = []
        self.current_order = None
        self.round_counter = 100

    def __str__(self):
        return "---- Round counter: {}\nmy_chef: {}\nother_chef: {}\ncurrent_commands: {}\ncurrent_command: {}\norders: {}\ncurrent_order: {}".format(
            self.round_counter,
            self.my_chef,
            self.other_chef,
            "|".join([str(command) for command in self.current_commands]),
            self.current_command,
            "|".join([json.dumps(order) for order in self.orders]),
            self.current_order
        )

    def flush_game(self):
        self.current_command = None
        self.orders = []
        self.current_order = None

    def get_better_command(self):
        self.current_command = sorted(self.current_commands, key=lambda command: command.award, reverse=True)[0]

        return self.current_command

    def set_orders(self):
        if self.current_command is not None:
            orders = Recipe(self.current_command.name).orders
            self.orders = sorted(orders, key=lambda order: order["priority"])
        else:
            self.orders = []

    def get_order(self):
        if len(self.orders) > 0:
            self.current_order = self.orders[0]
        else:
            self.current_order = None

        return self.current_order

    def is_order_validated(self):
        return self.current_order is not None and self.current_order["validation"] in self.my_chef.item

    def is_command_validated(self):
        return self.current_command is not None and self.current_command.id not in [command.id for command in self.current_commands]


if __name__ == '__main__':
    num_all_customers = int(input())
    map = Map(11, 7)
    game = Game(map, num_all_customers, [])
    commands = []
    for i in range(num_all_customers):
        customer_item, customer_award = input().split()
        customer_award = int(customer_award)
        command_id = uuid.uuid4()
        commands.append(Command(command_id, customer_item, customer_award))
    game.commands = commands

    for row_index in range(7):
        for column_index, tile in enumerate(input()):
            map.add_tile(row_index, column_index, tile)

    print_debug(map)

    # game loop
    while True:
        game.remaining_turn = int(input())
        if game.round_counter == 0:
            game.round_counter = 100
            game.flush_game()

        game.round_counter -= 1

        player_x, player_y, player_item = input().split()
        player_x = int(player_x)
        player_y = int(player_y)

        game.my_chef.position = Position(player_x, player_y)
        game.my_chef.item = player_item

        partner_x, partner_y, partner_item = input().split()
        partner_x = int(partner_x)
        partner_y = int(partner_y)

        game.other_chef.position = Position(partner_x, partner_y)
        game.other_chef.item = partner_item

        num_tables_with_items = int(input())  # the number of tables in the kitchen that currently hold an item
        for i in range(num_tables_with_items):
            table_x, table_y, item = input().split()
            table_x = int(table_x)
            table_y = int(table_y)
        # oven_contents: ignore until wood 1 league
        oven_contents, oven_timer = input().split()
        oven_timer = int(oven_timer)

        num_customers = int(input())  # the number of customers currently waiting for food
        current_commands = []
        for i in range(num_customers):
            customer_item, customer_award = input().split()
            customer_award = int(customer_award)
            command_id = uuid.uuid4()
            current_commands.append(Command(command_id, customer_item, customer_award))
        game.current_commands = current_commands

        if len(game.orders) == 0:
            game.get_better_command()
            game.set_orders()

        current_order = game.get_order()

        if game.is_order_validated():
            game.orders = game.orders[1:]

            if len(game.orders) == 0:
                game.get_better_command()
                game.set_orders()
                current_order = game.get_order()
            else:
                current_order = game.get_order()

        target_position = game.map.find_position(current_order["location"])

        print_debug(game)

        print("USE {} {}".format(target_position.x, target_position.y))
