import sys, os
import pytest

sys.path.insert(0, os.path.abspath(".."))
from app import (
    Spell,
    reset_spells,
    get_missing_items,
    use_spell,
    get_spell_to_create_ingredient,
    get_actions_missing_ingredient,
    get_actions_missing_ingredients,
)


@pytest.fixture()
def before():
    print("\r")


def test_reset_spells():
    spells = [Spell(0, [-1, 1, 0, 0], True), Spell(1, [0, -1, 1, 0], False)]

    new_spells = reset_spells(spells)

    assert new_spells[0].castable
    assert new_spells[1].castable


def test_get_missing_items():
    inventory_ingredients = [3, 0, 0, 0]
    other_ingredients = [-1, -2, 0, -1]
    missing_items = get_missing_items(inventory_ingredients, other_ingredients)
    assert missing_items == [[0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]]

    inventory_ingredients = [3, 0, 0, 0]
    other_ingredients = [-1, 0, 0, 0]
    missing_items = get_missing_items(inventory_ingredients, other_ingredients)
    assert missing_items == []


def test_use_spell():
    inventory_ingredients = [3, 0, 0, 0]
    spell = Spell(0, [-1, 1, 0, 0], True)

    new_inventory_ingredients, spell2 = use_spell(inventory_ingredients, spell)

    assert new_inventory_ingredients == [2, 1, 0, 0]
    assert not spell.castable


def test_get_spell_to_create_ingredient():
    ingredient = [0, 1, 0, 0]
    spells = [Spell(0, [-1, 1, 0, 0], True), Spell(1, [0, -1, 1, 0], True)]
    res_spell = get_spell_to_create_ingredient(ingredient, spells)
    assert res_spell.id == 0

    ingredient = [0, 1, 0, 0]
    spells = [Spell(0, [-1, 1, 0, 0], False), Spell(1, [0, -1, 1, 0], False)]
    res_spell = get_spell_to_create_ingredient(ingredient, spells)
    assert res_spell is None


def test_get_actions_missing_ingredient_simple_case():
    inventory_ingredients = [3, 0, 0, 0]
    missing_ingredient = [0, 1, 0, 0]
    actions = []
    spells = [Spell(0, [-1, 1, 0, 0], True), Spell(1, [0, -1, 1, 0], True)]

    actions_res, spells_res, inventory_ingredients = get_actions_missing_ingredient(
        missing_ingredient, actions, spells, inventory_ingredients
    )

    assert actions_res == ["CAST 0"]


def test_get_actions_missing_ingredient_no_spell_left():
    inventory_ingredients = [3, 0, 0, 0]
    missing_ingredient = [0, 1, 0, 0]
    actions = []
    spells = [Spell(0, [-1, 1, 0, 0], False), Spell(1, [0, -1, 1, 0], False)]

    actions_res, spells_res, inventory_ingredients = get_actions_missing_ingredient(
        missing_ingredient, actions, spells, inventory_ingredients
    )

    assert actions_res == ["REST", "CAST 0"]


def test_get_actions_missing_ingredient_with_one_intermediate_ingredient():
    inventory_ingredients = [3, 0, 0, 0]
    missing_ingredient = [0, 0, 1, 0]
    actions = []
    spells = [Spell(0, [-1, 1, 0, 0], True), Spell(1, [0, -1, 1, 0], True)]

    actions_res, spells_res, inventory_ingredients = get_actions_missing_ingredient(
        missing_ingredient, actions, spells, inventory_ingredients
    )

    assert actions_res == ["CAST 0", "CAST 1"]
    assert inventory_ingredients == [2, 0, 1, 0]
    assert not spells[0].castable
    assert not spells[1].castable


def test_get_actions_missing_ingredient_two_intermediate_ingredients():
    inventory_ingredients = [0, 0, 0, 0]
    missing_ingredient = [0, 0, 0, 1]
    actions = []
    spells = [
        Spell(0, [2, 0, 0, 0], True),
        Spell(1, [-1, 1, 0, 0], True),
        Spell(2, [0, -1, 1, 0], True),
        Spell(3, [0, 0, -1, 1], True),
    ]

    actions_res, spells_res, inventory_ingredients = get_actions_missing_ingredient(
        missing_ingredient, actions, spells, inventory_ingredients
    )

    assert actions_res == [
        "CAST 0",
        "CAST 1",
        "CAST 2",
        "CAST 3",
    ]
    assert inventory_ingredients == [1, 0, 0, 1]


def test_get_actions_missing_ingredients_two_same_ingredients():
    inventory_ingredients = [3, 0, 0, 0]
    missing_ingredients = [[0, 1, 0, 0], [0, 1, 0, 0]]
    actions = []
    spells = [Spell(0, [-1, 1, 0, 0], True), Spell(1, [0, -1, 1, 0], True)]

    actions_res, spells_res, inventory_ingredients = get_actions_missing_ingredients(
        missing_ingredients, actions, spells, inventory_ingredients
    )

    assert actions_res == ["CAST 0", "REST", "CAST 0"]
    assert inventory_ingredients == [1, 2, 0, 0]


# @pytest.mark.usefixtures("before")
def test_get_actions_missing_ingredients_hard_case():
    inventory_ingredients = [3, 0, 0, 0]
    missing_ingredients = [
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
    ]
    actions = []
    spells = [
        Spell(0, [2, 0, 0, 0], True),
        Spell(1, [-1, 1, 0, 0], True),
        Spell(2, [0, -1, 1, 0], True),
        Spell(3, [0, 0, -1, 1], True),
    ]

    expected_actions = [
        "CAST 1",
        "CAST 2",
        "CAST 3",
        "REST",
        "CAST 1",
        "CAST 2",
        "CAST 3",
        "REST",
        "CAST 1",
        "CAST 2",
        "CAST 3",
        "REST",
        "CAST 0",
        "CAST 1",
        "CAST 2",
        "CAST 3",
        "REST",
        "CAST 1",
        "CAST 2",
        "CAST 3",
    ]

    actions_res, spells_res, inventory_ingredients = get_actions_missing_ingredients(
        missing_ingredients, actions, spells, inventory_ingredients
    )

    assert actions_res == expected_actions
    assert inventory_ingredients == [0, 0, 0, 5]
