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
        return f"id: {self.id}, {self.ingredients}, price: {self.price}"

    def __repr__(self):
        return self.__str__()


class Spell:
    def __init__(self, id, ingedients, castable):
        self.id = id
        self.ingredients = ingedients
        self.castable = castable

    def __str__(self):
        return f"id: {self.id}, {self.ingredients}, castable: {self.castable}"

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


def get_missing_items(inventory_ingredients, other_ingredients):
    diff = [a + b for a, b in zip(inventory_ingredients, other_ingredients)]
    res = []

    for index, value in enumerate(diff):
        if value < 0:
            value = value * -1
            for counter in range(0, value):
                temp = [0, 0, 0, 0]
                temp[index] = 1
                res.append(temp)
    return res


def use_spell(inventory_ingredients, spell):
    spell_ingredients = spell.ingredients
    new_inventory_ingredients = [
        a + b for a, b in zip(inventory_ingredients, spell_ingredients)
    ]
    spell.castable = False

    return new_inventory_ingredients, spell


def get_spell_to_create_ingredient(ingredient, spells):
    valid_spells = [spell for spell in spells if spell.castable]
    item_index = ingredient.index(1)

    for spell in valid_spells:
        spell_ingredients = spell.ingredients
        if spell_ingredients[item_index] >= 1:
            return spell

    return None


def reset_spells(spells):
    for spell in spells:
        spell.castable = True

    return spells


def get_actions_missing_ingredient(
    missing_ingredient, actions, spells, inventory_ingredients
):
    spell = get_spell_to_create_ingredient(missing_ingredient, spells)

    if spell is None:
        actions.append("REST")
        spells = reset_spells(spells)
        return get_actions_missing_ingredient(
            missing_ingredient, actions, spells, inventory_ingredients
        )
    else:
        missing_ingredients_for_spell = get_missing_items(
            inventory_ingredients, spell.ingredients
        )

        if len(missing_ingredients_for_spell) == 0:
            actions.append(f"CAST {spell.id}")
            inventory_ingredients, spell2 = use_spell(inventory_ingredients, spell)

            return actions, spells, inventory_ingredients
        else:
            all_missing_ingredients = missing_ingredients_for_spell + [
                missing_ingredient
            ]
            return get_actions_missing_ingredients(
                all_missing_ingredients, actions, spells, inventory_ingredients
            )


def get_actions_missing_ingredients(
    missing_ingredients, actions, spells, inventory_ingredients
):
    for missing_ingredient in missing_ingredients:
        (actions, spells, inventory_ingredients) = get_actions_missing_ingredient(
            missing_ingredient, actions, spells, inventory_ingredients
        )

    return actions, spells, inventory_ingredients


def create_actions(inventory, order, spells):
    inventory_ingredients = inventory.ingredients
    order_ingredients = order.ingredients

    missing_ingredients = get_missing_items(inventory_ingredients, order_ingredients)

    if len(missing_ingredients) == 0:
        return [f"BREW {order.id}"]
    else:
        actions, spells, inventory_ingredients = get_actions_missing_ingredients(
            missing_ingredients, [], spells, inventory_ingredients
        )

        return actions


if __name__ == "__main__":
    while True:
        orders = []
        my_spells = []
        inventories = []

        action_count = int(input())  # the number of spells and recipes in play
        for i in range(action_count):
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

            if action_type == "BREW":
                order = Order(action_id, [delta_0, delta_1, delta_2, delta_3], price)
                orders.append(order)
            elif action_type == "CAST":
                spell = Spell(action_id, [delta_0, delta_1, delta_2, delta_3], castable)
                my_spells.append(spell)

        for i in range(2):
            # inv_0: tier-0 ingredients in inventory
            # score: amount of rupees
            inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]

            inventory = Inventory([inv_0, inv_1, inv_2, inv_3])
            inventories.append(inventory)

        my_inventory = inventories[0]

        print_debug(f"my inventory: {my_inventory}")
        print_debug(f"my spells: {my_spells}")
        print_debug(f"orders: {orders}")

        sorted_orders = sorted(orders, key=lambda order: order.price, reverse=True)
        best_order = sorted_orders[0]
        actions = create_actions(my_inventory, best_order, my_spells)
        fist_action = actions[0]

        print_debug(actions)

        # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT
        print(fist_action)
