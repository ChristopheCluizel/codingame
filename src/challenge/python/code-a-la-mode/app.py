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
        self.desserts = self.get_desserts_from_command_name(name)
        self.desserts_state = {}

    def __str__(self):
        return "---- Command id: {}, name: {}, award: {}\ndesserts: {}\ndesserts_state: {}\n".format(
            self.id,
            self.name,
            self.award,
            "|".join([str(dessert) for dessert in self.desserts]),
            self.desserts_state
        )

    def is_equal(self, that):
        return self.id == that.id and self.name == that.name and self.award == that.award

    def is_validated(self, current_commands):
        return self.id not in [command.id for command in current_commands]

    def get_desserts_from_command_name(self, command_name):
        return [Dessert(dessert_name) for dessert_name in command_name.split("-") if dessert_name != "DISH"]

    def set_desserts_state(self):
        for dessert in self.desserts:
            self.set_dessert_state(dessert.name, False)

    def set_dessert_state(self, dessert_name, state):
        self.desserts_state[dessert_name] = state

    def get_desserts_from_level(self, level):
        return [dessert for dessert in self.desserts if dessert.level == level]

    def get_dessert_from_name(self, dessert_name):
        res = [dessert for dessert in self.desserts if dessert.name == dessert_name]

        if len(res) > 0:
            return res[0]
        else:
            return None

    def get_desserts_from_state(self, state):
        return [self.get_dessert_from_name(key) for key, value in self.desserts_state.items() if value == state]

    def get_desserts_from_state_and_level(self, state, level):
        desserts_by_state = self.get_desserts_from_state(state)
        desserts_by_level = self.get_desserts_from_level(level)

        res = []
        for dessert_by_state in desserts_by_state:
            for dessert_by_level in desserts_by_level:
                if dessert_by_state.name == dessert_by_level.name:
                    res.append(dessert_by_state)
        return res


class Dessert:
    def __init__(self, name):
        self.name = name
        self.level = self.set_level()

    def __str__(self):
        return "{}, level: {}".format(self.name, self.level)

    def is_equal(self, that):
        return self.name == that.name and self.level == that.level

    def set_level(self):
        mapping = {
            "BLUEBERRIES": "basic",
            "ICE_CREAM": "basic",
            "CHOPPED_STRAWBERRIES": "classic",
            "CROISSANT": "classic",
            "TART": "advanced"
        }
        return mapping[self.name]

    def prepare(self):
        if self.name == "BLUEBERRIES":
            orders = [
                {"priority": 10, "action": "take", "item": "BLUEBERRIES", "location": "blueberry_crate", "validation": "BLUEBERRIES"}
            ]
        elif self.name == "ICE_CREAM":
            orders = [
                {"priority": 10, "action": "take", "item": "ICE_CREAM", "location": "ice_cream_crate", "validation": "ICE_CREAM"}
            ]
        else:
            orders = []

        return orders


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = None
        self.tables_with_item = []
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

    def find_stable_position(self, item_location, my_chef_position=None):
        """

        :param item_location: "dish_washer", "window", "blueberry_crate", "ice_cream_crate", "strawberry_crate", "chopping_board", "oven", "dough_crate"
        :type item_location: string
        :return:
        :rtype: Position
        """

        def find_letter(letter):
            for x in range(self.width):
                for y in range(self.height):
                    if self.tiles[x][y] == letter:
                        return Position(x, y)
            return None

        def get_empty_position_near_chef():
            positions_near_chef = [
                Position(max(0, my_chef_position.x - 1), max(0, my_chef_position.y - 1)),
                Position(max(0, my_chef_position.x), max(0, my_chef_position.y - 1)),
                Position(min(10, my_chef_position.x + 1), max(0, my_chef_position.y - 1)),
                Position(max(0, my_chef_position.x - 1), max(0, my_chef_position.y)),
                Position(min(10, my_chef_position.x + 1), max(0, my_chef_position.y)),
                Position(max(0, my_chef_position.x - 1), min(6, my_chef_position.y + 1)),
                Position(max(0, my_chef_position.x), min(6, my_chef_position.y + 1)),
                Position(min(10, my_chef_position.x + 1), min(6, my_chef_position.y + 1))
            ]

            positions_with_item = [table.position for table in self.tables_with_item]

            res = []
            for position_near_chef in positions_near_chef:
                if len(positions_with_item) == 0:
                    res.append(position_near_chef)
                else:
                    if not any([position_near_chef.is_equal(position) for position in positions_with_item]):
                        res.append(position_near_chef)
            return res

        if item_location == "empty_table":
            empty_fixed_positions = []
            for x in range(self.width):
                for y in range(self.height):
                    if self.tiles[x][y] == '#':
                        empty_fixed_positions.append(Position(x, y))

            empty_positions_near_chef = get_empty_position_near_chef()

            for empty_fixed_position in empty_fixed_positions:
                for empty_position_near_chef in empty_positions_near_chef:
                    if empty_fixed_position.is_equal(empty_position_near_chef):
                        return empty_fixed_position
        else:
            mapping = {
                "DISH": "D",
                "window": "W",
                "BLUEBERRIES": "B",
                "ICE_CREAM": "I",
                "STRAWBERRIES": "S",
                "chopping_board": "C",
                "DOUGH": "H",
                "oven": "O"
            }
            letter = mapping.get(item_location, None)

            if letter is not None:
                return find_letter(letter)
            else:
                return None

    def find_variable_position(self, item, my_chef, oven, current_command, other_chef):
        my_chef_position = my_chef.position
        target_positions = []

        # find on oven in priority
        if item in ["TART", "CROISSANT"] and oven.item == item:
            return self.find_stable_position("oven")

        # find on static sources
        static_position = self.find_stable_position(item, my_chef_position)
        if static_position is not None:
            target_positions.append(static_position)

        # if no dish in dishwasher then ignore the dishwasher
        if self.is_no_dish_in_dishwasher(other_chef) and item == "DISH":
            target_positions = []

        # find best dish
        if item == "DISH":
            dynamic_positions = []

            # get dish with already cooked desserts
            for table in self.tables_with_item:
                if "DISH-" in table.item:
                    desserts_in_dish = [Dessert(dessert_name) for dessert_name in table.item.split("DISH-")[1].split("-")]
                    all_desserts_in_command = True

                    # if one dessert in dish is not in the current command then false
                    for dessert_in_dish in desserts_in_dish:
                        if dessert_in_dish.name not in [dessert.name for dessert in current_command.desserts]:
                            all_desserts_in_command = False

                    if all_desserts_in_command:
                        # if dish exists with already made desserts, then ignore dish from dishwasher
                        target_positions = []
                        dynamic_positions.append(table.position)

            # get empty dish
            if len(dynamic_positions) == 0:
                for table in self.tables_with_item:
                    if "DISH" == table.item:
                        dynamic_positions.append(table.position)
        else:  # find on tables
            dynamic_positions = [table.position for table in self.tables_with_item if table.item == item]

        target_positions += dynamic_positions

        if len(target_positions) > 0:
            return self.get_nearest_target_position(my_chef_position, target_positions)
        else:
            return None

    def get_nearest_target_position(self, my_chef_position, target_positions):
        res = []
        for target_position in target_positions:
            distance = my_chef_position.distance_with(target_position)
            res.append((target_position, distance))

        return sorted(res, key=lambda t: t[1])[0][0]

    def is_no_dish_in_dishwasher(self, other_chef):
        return len([table for table in self.tables_with_item if "DISH" in table.item]) == 3 or \
               (len([table for table in self.tables_with_item if "DISH" in table.item]) == 2 and "DISH" in other_chef.item)


class Table:
    def __init__(self, position, item):
        self.position = position
        self.item = item

    def __str__(self):
        return """"Table: {}, item: {}""".format(self.position, self.item)


class Oven:
    def __init__(self, timer, item):
        self.timer = timer
        self.item = item

    def __str__(self):
        return "Oven timer: {}, item: {}".format(self.timer, self.item)


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
        self.oven = None

    def __str__(self):
        return "---- my_chef: {}\nother_chef: {}\n---- current_command: {}\norders: {}\ncurrent_order: {}\ntables: {}\noven: {}".format(
            self.my_chef,
            self.other_chef,
            self.current_command,
            "|".join([json.dumps(order) for order in self.orders]),
            self.current_order,
            "|".join([str(table) for table in self.map.tables_with_item]),
            self.oven
        )

    def flush_game(self):
        self.current_command = None
        self.orders = []
        self.current_order = None

    def get_better_command(self):
        print_debug("Get a new command!")
        sorted_commands = sorted([command for command in self.current_commands], key=lambda command: command.award, reverse=True)
        self.current_command = sorted_commands[0]

        return self.current_command

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

    def make(self, dessert):
        if "DISH" in self.my_chef.item:
            orders = [{"priority": 0, "action": "drop", "item": "DISH", "location": "empty_table", "validation": "NONE"}]
        else:
            if dessert.name == "CHOPPED_STRAWBERRIES":
                orders = [
                    {"priority": 0, "action": "take", "item": "STRAWBERRIES", "location": "strawberry_crate", "validation": "STRAWBERRIES"},
                    {"priority": 0, "action": "chop", "item": "STRAWBERRIES", "location": "chopping_board", "validation": "CHOPPED_STRAWBERRIES"},
                    {"priority": 0, "action": "drop", "item": "CHOPPED_STRAWBERRIES", "location": "empty_table", "validation": "NONE"}
                ]
            elif dessert.name == "CROISSANT":
                orders = [
                    {"priority": 0, "action": "take", "item": "DOUGH", "location": "dough_crate", "validation": "DOUGH"},
                    {"priority": 0, "action": "drop", "item": "DOUGH", "location": "oven", "validation": "NONE"},
                    {"priority": 0, "action": "take", "item": "DISH", "location": "dish_washer", "validation": "DISH"},
                    {"priority": 0, "action": "wait", "item": "CROISSANT", "location": "oven", "validation": "CROISSANT"},
                    {"priority": 0, "action": "take", "item": "CROISSANT", "location": "oven", "validation": "CROISSANT"}
                ]
            elif dessert.name == "TART":
                orders = [
                    {"priority": 0, "action": "take", "item": "DOUGH", "location": "dough_crate", "validation": "DOUGH"},
                    {"priority": 0, "action": "chop", "item": "DOUGH", "location": "chopping_board", "validation": "CHOPPED_DOUGH"},
                    {"priority": 0, "action": "take", "item": "BLUEBERRIES", "location": "blueberry_crate", "validation": "RAW_TART"},
                    {"priority": 0, "action": "drop", "item": "RAW_TART", "location": "oven", "validation": "NONE"},
                    {"priority": 0, "action": "take", "item": "DISH", "location": "dish_washer", "validation": "DISH"},
                    {"priority": 0, "action": "wait", "item": "TART", "location": "oven", "validation": "TART"},
                    {"priority": 0, "action": "take", "item": "TART", "location": "oven", "validation": "TART"}
                ]
            else:
                orders = []

        return orders

    # Not used
    def _find(self, dessert):
        # check on tables
        for table in self.map.tables_with_item:
            if table.item == dessert.name:
                return {"priority": 0, "action": "take", "item": dessert.name, "location": str(table.position), "validation": dessert.name}
        # check in oven
        if self.oven.item == dessert.name:
            return {"priority": 0, "action": "take", "item": dessert.name, "location": str(self.map.find_stable_position("oven")), "validation": dessert.name}
        return None

    def is_dessert_existed(self, dessert):
        # check in hands
        if dessert.name in self.my_chef.item and "RAW_" not in self.my_chef.item:
            return True
        # check on tables
        for table in self.map.tables_with_item:
            # if my chef doesn't carry a dish, he will be able to take the dish with the existing dessert
            if dessert.name == table.item or \
                    ("DISH" not in self.my_chef.item and
                     dessert.name in table.item and
                     self.does_table_contain_dish_with_only_desserts_for_my_command(table)):
                return True
        # check in oven
        if self.oven.item == dessert.name:
            return True
        return False

    def does_table_contain_dish_with_only_desserts_for_my_command(self, table):
        command_dessert_names = [dessert.name for dessert in self.current_command.desserts]
        dish_dessert_names = [name for name in table.item.split("-") if name != "DISH"]

        if "DISH" not in table.item:
            return False

        for dish_dessert_name in dish_dessert_names:
            if dish_dessert_name not in command_dessert_names:
                return False
        return True

    def find_or_make(self, dessert):
        if not self.is_dessert_existed(dessert):
            make_orders = self.make(dessert)
            return make_orders
        else:
            self.current_command.set_dessert_state(dessert.name, True)
            return []

    def find(self, dessert):
        orders = []

        if "DISH" not in self.my_chef.item:
            orders.append({"priority": 0, "action": "take", "item": "DISH", "location": "dish_washer", "validation": "DISH"})
        elif dessert.name not in self.my_chef.item:
            if dessert.name == "ICE_CREAM":
                orders += Dessert("ICE_CREAM").prepare()
            elif dessert.name == "BLUEBERRIES":
                orders += Dessert("BLUEBERRIES").prepare()
            else:
                # check on tables
                for table in self.map.tables_with_item:
                    if dessert.name == table.item:
                        orders.append({"priority": 0, "action": "take", "item": dessert.name, "location": str(table.position), "validation": dessert.name})
                # check in oven
                if len(orders) == 0 and self.oven.item == dessert.name:
                    orders.append({"priority": 0, "action": "take", "item": dessert.name, "location": str(self.map.find_stable_position("oven")), "validation": dessert.name})

        self.orders = orders

        return orders

    def get_orders(self):
        classic_desserts = self.current_command.get_desserts_from_state_and_level(False, "classic")
        for classic_dessert in classic_desserts:
            print_debug("Make classic desserts")
            game.orders = self.find_or_make(classic_dessert)
            if len(game.orders) > 0:
                break

        if len(game.orders) == 0:
            advanced_desserts = self.current_command.get_desserts_from_state_and_level(False, "advanced")
            for advanced_dessert in advanced_desserts:
                print_debug("Make advanced desserts")
                game.orders = self.find_or_make(advanced_dessert)
                if len(game.orders) > 0:
                    break

        if len(game.orders) == 0:
            all_desserts = self.current_command.get_desserts_from_state_and_level(True, "advanced") + \
                           self.current_command.get_desserts_from_state_and_level(True, "classic") + \
                           self.current_command.get_desserts_from_state_and_level(False, "basic") + \
                           self.current_command.get_desserts_from_state_and_level(True, "basic")
            all_dessert_positions = []
            for dessert in all_desserts:
                position = self.map.find_variable_position(dessert.name, self.my_chef, self.oven, self.current_command, self.other_chef)
                print_debug("{}: {}".format(str(dessert), str(position)))
                if position is not None:
                    all_dessert_positions.append((dessert, position))

            desserts_distances = [(tuple[0], self.my_chef.position.distance_with(tuple[1])) for tuple in all_dessert_positions]

            sorted_list = sorted(desserts_distances, key=lambda tuple: tuple[1])
            if len(sorted_list) > 0:
                for basic_dessert_tuple in sorted_list:
                    basic_dessert = basic_dessert_tuple[0]
                    game.orders = self.find(basic_dessert)
                    if len(game.orders) > 0:
                        break

        if len(game.orders) == 0:
            print_debug("GO to window!")
            game.orders = [{"priority": 0, "action": "drop", "item": "WINDOW", "location": "window", "validation": "NONE"}]

    def flush_orders(self, action):
        res = self.orders

        if action == "take":
            inexisting_desserts = self.current_command.get_desserts_from_state_and_level(False, "classic") + \
                                  self.current_command.get_desserts_from_state_and_level(False, "advanced")

            inexisting_dessert_names = [dessert.name for dessert in inexisting_desserts]
            first_order = self.orders[0]

            if first_order["action"] == action and first_order["item"] in inexisting_dessert_names:
                res = res[1:]

        return res

    def flush_all_orders(self):
        self.orders = []

    def execute_orders(self):
        if self.current_command is None or self.current_command.is_validated(self.current_commands):
            game.get_better_command()

        if len(self.orders) == 0:
            self.get_orders()

        if self.is_order_validated():
            self.orders = self.orders[1:]
            if len(self.orders) == 0:
                self.get_orders()

        current_order = self.get_order()
        print_debug(game)

        # if "CROISSANT" or "TART" is ready, cancel the WAIT
        if current_order["action"] == "wait" and (self.oven.item == "CROISSANT" or self.oven.item == "TART"):
            self.orders = self.orders[1:]
            current_order = self.get_order()

        game.orders = self.flush_orders("take")

        if current_order["action"] == "drop":
            print_debug("DROP")
            target_position = game.map.find_stable_position(current_order["location"], self.my_chef.position)
        elif current_order["action"] == "chop":
            print_debug("CHOP")
            target_position = game.map.find_stable_position("chopping_board")
        elif current_order["action"] == "take":
            print_debug("TAKE")
            target_position = game.map.find_variable_position(current_order["item"], self.my_chef, self.oven, self.current_command, self.other_chef)
        else:
            target_position = None

        if target_position is None or current_order["action"] == "wait":
            print("WAIT")
        else:
            print("USE {} {}".format(target_position.x, target_position.y))

    def get_command_or_create(self, command_id, command_name, command_award):
        if self.current_command is None:
            command = Command(command_id, command_name, command_award)
        elif self.current_command.name == command_name:
            command = self.current_command
        else:
            command = Command(command_id, command_name, command_award)

        for dessert in command.desserts:
            command.set_dessert_state(dessert.name, self.is_dessert_existed(dessert))

        return command

    def get_positions_near_chef(self):
        my_chef_position = self.my_chef.position
        positions_near_chef = [
            Position(max(0, my_chef_position.x - 1), max(0, my_chef_position.y - 1)),
            Position(max(0, my_chef_position.x), max(0, my_chef_position.y - 1)),
            Position(min(10, my_chef_position.x + 1), max(0, my_chef_position.y - 1)),
            Position(max(0, my_chef_position.x - 1), max(0, my_chef_position.y)),
            Position(min(10, my_chef_position.x + 1), max(0, my_chef_position.y)),
            Position(max(0, my_chef_position.x - 1), min(6, my_chef_position.y + 1)),
            Position(max(0, my_chef_position.x), min(6, my_chef_position.y + 1)),
            Position(min(10, my_chef_position.x + 1), min(6, my_chef_position.y + 1))
        ]
        return positions_near_chef

    def is_oven_next_to_chef(self):
        positions_near_chef = self.get_positions_near_chef()
        oven_position = self.map.find_stable_position("oven")

        oven_near_chef = False
        for position_near_chef in positions_near_chef:
            if position_near_chef.is_equal(oven_position):
                oven_near_chef = True

        return oven_near_chef


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
        tables = []
        for i in range(num_tables_with_items):
            table_x, table_y, item = input().split()
            table_x = int(table_x)
            table_y = int(table_y)
            tables.append(Table(Position(table_x, table_y), item))
        game.map.tables_with_item = tables

        # oven_contents: ignore until wood 1 league
        oven_contents, oven_timer = input().split()
        oven_timer = int(oven_timer)
        game.oven = Oven(oven_timer, oven_contents)

        num_customers = int(input())  # the number of customers currently waiting for food
        current_commands = []
        for i in range(num_customers):
            customer_item, customer_award = input().split()
            customer_award = int(customer_award)
            command_id = uuid.uuid4()
            current_commands.append(game.get_command_or_create(command_id, customer_item, customer_award))
        game.current_commands = current_commands

        game.execute_orders()
