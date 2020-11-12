import sys
import math

DEBUG = False


def print_debug(description):
    if DEBUG:
        print(description, file=sys.stderr)


class Order:
    def __init__(self, id, ingedients, price):
        self.id = id
        self.ingredients = ingedients
        self.price = price

    def __str__(self):
        return f"order id: {self.id}, {self.ingredients}, price: {self.price}"

    def __repr__(self):
        return self.__str__()


class Inventory:
    def __init__(self, ingedients):
        self.ingredients = ingedients

    def __str__(self):
        return f"inventory: {self.ingredients}"


def can_brew(inventory, order):
    for index, ingredient_nb in enumerate(order.ingredients):
        if inventory.ingredients[index] < ingredient_nb:
            return False

    return True


if __name__ == "__main__":
    while True:
        orders = []
        inventories = []
        action_count = int(input())  # the number of spells and recipes in play
        for i in range(action_count):
            # action_id: the unique ID of this spell or recipe
            # action_type: in the first league: BREW; later: CAST, OPPONENT_CAST, LEARN, BREW
            # delta_0: tier-0 ingredient change
            # delta_1: tier-1 ingredient change
            # delta_2: tier-2 ingredient change
            # delta_3: tier-3 ingredient change
            # price: the price in rupees if this is a potion
            # tome_index: in the first two leagues: always 0; later: the index in the tome if this is a tome spell, equal to the read-ahead tax
            # tax_count: in the first two leagues: always 0; later: the amount of taxed tier-0 ingredients you gain from learning this spell
            # castable: in the first league: always 0; later: 1 if this is a castable player spell
            # repeatable: for the first two leagues: always 0; later: 1 if this is a repeatable player spell
            (
                action_id,
                action_type,
                delta_0,
                delta_1,
                delta_2,
                delta_3,
                price,
                tome_index,
                tax_count,
                castable,
                repeatable,
            ) = input().split()
            action_id = int(action_id)
            delta_0 = int(delta_0)
            delta_1 = int(delta_1)
            delta_2 = int(delta_2)
            delta_3 = int(delta_3)
            price = int(price)
            tome_index = int(tome_index)
            tax_count = int(tax_count)
            castable = castable != "0"
            repeatable = repeatable != "0"

            order = Order(action_id, [delta_0, delta_1, delta_2, delta_3], price)
            orders.append(order)

        for i in range(2):
            # inv_0: tier-0 ingredients in inventory
            # score: amount of rupees
            inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]

            inventory = Inventory([inv_0, inv_1, inv_2, inv_3])
            inventories.append(inventory)

        my_inventory = inventories[0]

        for order in orders:
            print_debug(order)
        print_debug(my_inventory)

        sorted_orders = sorted(orders, key=lambda order: order.price, reverse=True)
        for order in sorted_orders:
            if can_brew(my_inventory, order):
                order_id = order.id
                break

        # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT
        print(f"BREW {order_id}")
