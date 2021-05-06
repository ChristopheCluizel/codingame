import sys
import copy

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
    def __init__(self, id, ingredients, castable):
        self.id = id
        self.ingredients = ingredients
        self.castable = castable

    def __str__(self):
        return f"id: {self.id}, {self.ingredients}, castable: {self.castable}"

    def __repr__(self):
        return self.__str__()


class TomeSpell(Spell):
    def __init__(self, id, ingredients, index):
        super().__init__(id, ingredients, False)
        self.index = index

    def __str__(self):
        return super().__str__() + f", index: {self.index}"


class Inventory:
    def __init__(self, ingedients):
        self.ingredients = ingedients

    def __str__(self):
        return f"inventory: {self.ingredients}"


class Game:
    def __init__(self):
        self.rounds_left = 100

    def __str__(self):
        return f"rounds_left: {self.rounds_left}"


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
    new_spell = Spell(spell.id, spell.ingredients, False)

    return new_inventory_ingredients, new_spell


def get_spell_to_create_ingredient(ingredient, spells):
    valid_spells = [spell for spell in spells if spell.castable]
    item_index = ingredient.index(1)

    eligible_spells = []
    for spell in valid_spells:
        spell_ingredients = spell.ingredients
        if spell_ingredients[item_index] >= 1:
            eligible_spells.append(spell)

    if len(eligible_spells) > 0:
        optimised_spell = sorted(
            eligible_spells, key=lambda spell: sum(spell.ingredients), reverse=True
        )[0]
        return optimised_spell
    else:
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
            inventory_ingredients, updated_spell = use_spell(
                inventory_ingredients, spell
            )
            spells = [spell for spell in spells if spell.id != updated_spell.id]
            spells.append(updated_spell)

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


def get_actions_to_create_order(inventory, order, spells):
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


def get_missing_items_for_tome_spell(inventory_ingredients, tome_spell):
    tome_spell_index = tome_spell.index
    nb_item_needed = tome_spell_index - inventory_ingredients[0]

    if nb_item_needed > 0:
        return [[1, 0, 0, 0] for i in range(0, nb_item_needed)]
    else:
        return []


def get_actions_to_create_tome_spell(inventory, tome_spell, spells):
    inventory_ingredients = inventory.ingredients

    missing_ingredients = get_missing_items_for_tome_spell(
        inventory_ingredients, tome_spell
    )

    if len(missing_ingredients) == 0:
        return [f"LEARN {tome_spell.id}"]
    else:
        actions, spells, inventory_ingredients = get_actions_missing_ingredients(
            missing_ingredients, [], spells, inventory_ingredients
        )

        return actions


def is_interesting_tome_spell(tome_spells):
    eligible_spells = []
    for spell in tome_spells:
        ingredients = spell.ingredients

        if all(i >= 0 for i in ingredients):
            print_debug(ingredients)
            eligible_spells.append(spell)

    if len(eligible_spells) > 0:
        return sorted(
            eligible_spells, key=lambda spell: sum(spell.ingredients), reverse=True
        )[0]
    else:
        return None


if __name__ == "__main__":
    game = Game()

    while True:
        orders = []
        my_spells = []
        inventories = []
        tome_spells = []

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
            elif action_type == "LEARN":
                spell = TomeSpell(
                    action_id, [delta_0, delta_1, delta_2, delta_3], tome_index
                )
                tome_spells.append(spell)

        for i in range(2):
            # inv_0: tier-0 ingredients in inventory
            # score: amount of rupees
            inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]

            inventory = Inventory([inv_0, inv_1, inv_2, inv_3])
            inventories.append(inventory)

        my_inventory = inventories[0]
        interesting_spell = is_interesting_tome_spell(tome_spells)
        if interesting_spell is not None:
            print_debug(f"{interesting_spell.id} is an interesting tome spell")
            actions = get_actions_to_create_tome_spell(
                copy.deepcopy(my_inventory),
                copy.deepcopy(interesting_spell),
                copy.deepcopy(my_spells),
            )
        else:
            orders_actions = []
            for order in orders:
                actions = get_actions_to_create_order(
                    copy.deepcopy(my_inventory),
                    copy.deepcopy(order),
                    copy.deepcopy(my_spells),
                )
                gain = order.price / len(actions)
                order_actions = (order, actions, gain)
                orders_actions.append(order_actions)

            # keep only orders we can make before the end of the game
            possible_orders_actions = [
                item for item in orders_actions if len(item[1]) <= game.rounds_left
            ]

            sorted_triple = sorted(
                possible_orders_actions, key=lambda triple: triple[2], reverse=True
            )

            best_triple = sorted_triple[0]
            actions = best_triple[1]
            print_debug("=========")
            print_debug(f"chosen triple: {best_triple}")

        game.rounds_left -= 1
        # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT
        print(actions[0])
