import sys, os
import pytest

sys.path.insert(0, os.path.abspath('..'))
from app import Position, Simulator, AI

pytest.total_score = 0


@pytest.fixture()
def before():
    print("\r")


def test_initialize_game():
    simulator = Simulator()
    inital_game = simulator.initialize_game(
        Position(0, 0),
        3,
        [{"id": 0, "position_x": 500, "position_y": 600},
         {"id": 1, "position_x": 700, "position_y": 300},
         {"id": 2, "position_x": 100, "position_y": 900}],
        1,
        [{"id": 0, "position_x": 2000, "position_y": 1000}]
    )

    assert len(inital_game.humans) == 3
    assert len(inital_game.zombies) == 1

    inital_game = simulator.initialize_game(
        Position(0, 0),
        4,
        [],
        2,
        []
    )

    assert len(inital_game.humans) == 4
    assert len(inital_game.zombies) == 2


def test_play_round_move():
    simulator = Simulator()
    inital_game = simulator.initialize_game(
        Position(0, 0),
        1,
        [{"id": 0, "position_x": 8250, "position_y": 4500}],
        1,
        [{"id": 0, "position_x": 8250, "position_y": 8999}]
    )

    ash_target_position = Position(8250, 8999)
    updated_game, round_score = simulator.play_round(inital_game, ash_target_position)

    assert updated_game.zombies[0].position.is_equal(Position(8250, 8599))
    assert updated_game.ash.position.is_equal(Position(675, 737))


def test_play_round_kill_zombies():
    simulator = Simulator()
    inital_game = simulator.initialize_game(
        Position(0, 0),
        3,
        [{"id": 0, "position_x": 8250, "position_y": 4500},
         {"id": 1, "position_x": 8000, "position_y": 7000},
         {"id": 2, "position_x": 2500, "position_y": 1000}],
        2,
        [{"id": 0, "position_x": 100, "position_y": 100},
         {"id": 0, "position_x": 200, "position_y": 200}]
    )

    ash_target_position = Position(8250, 8999)
    updated_game, round_score = simulator.play_round(inital_game, ash_target_position)

    assert inital_game.zombies_count == 2
    assert updated_game.zombies_count == 0
    assert len(updated_game.zombies) == 0
    assert round_score == 270


def test_play_round_eat_humans():
    simulator = Simulator()
    inital_game = simulator.initialize_game(
        Position(0, 0),
        3,
        [{"id": 0, "position_x": 8250, "position_y": 4500},
         {"id": 1, "position_x": 8000, "position_y": 7000},
         {"id": 2, "position_x": 2500, "position_y": 1000}],
        3,
        [{"id": 0, "position_x": 8200, "position_y": 4490},
         {"id": 0, "position_x": 8050, "position_y": 7000},
         {"id": 1, "position_x": 50, "position_y": 50}]
    )

    ash_target_position = Position(8250, 8999)
    updated_game, round_score = simulator.play_round(inital_game, ash_target_position)

    assert inital_game.humans_count == 3
    assert inital_game.zombies_count == 3
    assert updated_game.humans_count == 1
    assert updated_game.zombies_count == 2
    assert len(updated_game.humans) == 1
    assert round_score == 90


def test_testCase1():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(Position(0, 0), 1, [{"id": 0, "position_x": 8250, "position_y": 4500}], 1, [{"id": 0, "position_x": 8250, "position_y": 8999}])

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score == 10


def test_testCase2():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(5000, 0),
        1,
        [{"id": 0, "position_x": 950, "position_y": 6000},
         {"id": 1, "position_x": 8000, "position_y": 6100}],
        1,
        [{"id": 0, "position_x": 3100, "position_y": 7000},
         {"id": 1, "position_x": 11500, "position_y": 7100}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score == 80


def test_testCase3():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(10999, 0),
        1,
        [{"id": 0, "position_x": 8000, "position_y": 5500},
         {"id": 1, "position_x": 4000, "position_y": 5500}],
        1,
        [{"id": 0, "position_x": 1250, "position_y": 5500},
         {"id": 1, "position_x": 15999, "position_y": 5500}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase4():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(8000, 2000),
        1,
        [{"id": 0, "position_x": 8000, "position_y": 4500}],
        2,
        [{"id": 0, "position_x": 2000, "position_y": 6500},
         {"id": 1, "position_x": 14000, "position_y": 6500}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase5():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(7500, 2000),
        2,
        [{"id": 0, "position_x": 9000, "position_y": 1200},
         {"id": 1, "position_x": 4000, "position_y": 6000}],
        3,
        [{"id": 0, "position_x": 2000, "position_y": 1500},
         {"id": 1, "position_x": 13900, "position_y": 6500},
         {"id": 2, "position_x": 7000, "position_y": 7500}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase6():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(500, 4500),
        6,
        [
            {"id": 0, "position_x": 100, "position_y": 4000},
            {"id": 1, "position_x": 130, "position_y": 5000},
            {"id": 2, "position_x": 10, "position_y": 4500},
            {"id": 3, "position_x": 500, "position_y": 3500},
            {"id": 4, "position_x": 10, "position_y": 5500},
            {"id": 5, "position_x": 100, "position_y": 3000}
        ],
        10,
        [
            {"id": 0, "position_x": 8000, "position_y": 4500},
            {"id": 1, "position_x": 9000, "position_y": 4500},
            {"id": 2, "position_x": 10000, "position_y": 4500},
            {"id": 3, "position_x": 11000, "position_y": 4500},
            {"id": 4, "position_x": 12000, "position_y": 4500},
            {"id": 5, "position_x": 13000, "position_y": 4500},
            {"id": 6, "position_x": 14000, "position_y": 4500},
            {"id": 7, "position_x": 15000, "position_y": 3500},
            {"id": 8, "position_x": 14500, "position_y": 2500},
            {"id": 9, "position_x": 15900, "position_y": 500}
        ]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase7():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(0, 4000),
        2,
        [
            {"id": 0, "position_x": 0, "position_y": 1000},
            {"id": 1, "position_x": 0, "position_y": 8000}
        ],
        16,
        [
            {"id": 0, "position_x": 5000, "position_y": 1000},
            {"id": 1, "position_x": 5000, "position_y": 8000},
            {"id": 2, "position_x": 7000, "position_y": 1000},
            {"id": 3, "position_x": 7000, "position_y": 8000},
            {"id": 4, "position_x": 9000, "position_y": 1000},
            {"id": 5, "position_x": 9000, "position_y": 8000},
            {"id": 6, "position_x": 11000, "position_y": 1000},
            {"id": 7, "position_x": 11000, "position_y": 8000},
            {"id": 8, "position_x": 13000, "position_y": 1000},
            {"id": 9, "position_x": 13000, "position_y": 8000},
            {"id": 10, "position_x": 14000, "position_y": 1000},
            {"id": 11, "position_x": 14000, "position_y": 8000},
            {"id": 12, "position_x": 14500, "position_y": 1000},
            {"id": 13, "position_x": 14500, "position_y": 8000},
            {"id": 14, "position_x": 15000, "position_y": 1000},
            {"id": 15, "position_x": 15000, "position_y": 8000}
        ]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase8():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(0, 4000),
        2,
        [
            {"id": 0, "position_x": 0, "position_y": 1000},
            {"id": 1, "position_x": 0, "position_y": 8000}
        ],
        20,
        [
            {"id": 0, "position_x": 3000, "position_y": 1000},
            {"id": 1, "position_x": 3000, "position_y": 8000},
            {"id": 2, "position_x": 4000, "position_y": 1000},
            {"id": 3, "position_x": 4000, "position_y": 8000},
            {"id": 4, "position_x": 5000, "position_y": 1000},
            {"id": 5, "position_x": 5000, "position_y": 8000},
            {"id": 6, "position_x": 7000, "position_y": 1000},
            {"id": 7, "position_x": 7000, "position_y": 8000},
            {"id": 8, "position_x": 9000, "position_y": 1000},
            {"id": 9, "position_x": 9000, "position_y": 8000},
            {"id": 10, "position_x": 11000, "position_y": 1000},
            {"id": 11, "position_x": 11000, "position_y": 8000},
            {"id": 12, "position_x": 13000, "position_y": 1000},
            {"id": 13, "position_x": 13000, "position_y": 8000},
            {"id": 14, "position_x": 14000, "position_y": 1000},
            {"id": 15, "position_x": 14000, "position_y": 8000},
            {"id": 16, "position_x": 14500, "position_y": 1000},
            {"id": 17, "position_x": 14500, "position_y": 8000},
            {"id": 18, "position_x": 15000, "position_y": 1000},
            {"id": 19, "position_x": 15000, "position_y": 8000}
        ]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase9():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(8000, 4500),
        4,
        [
            {"id": 0, "position_x": 4000, "position_y": 2250},
            {"id": 1, "position_x": 4000, "position_y": 6750},
            {"id": 2, "position_x": 12000, "position_y": 2250},
            {"id": 3, "position_x": 12000, "position_y": 6750}
        ],
        12,
        [
            {"id": 0, "position_x": 4000, "position_y": 3375},
            {"id": 1, "position_x": 12000, "position_y": 3375},
            {"id": 2, "position_x": 4000, "position_y": 4500},
            {"id": 3, "position_x": 12000, "position_y": 4500},
            {"id": 4, "position_x": 4000, "position_y": 5625},
            {"id": 5, "position_x": 12000, "position_y": 5625},
            {"id": 6, "position_x": 6000, "position_y": 2250},
            {"id": 7, "position_x": 8000, "position_y": 2250},
            {"id": 8, "position_x": 10000, "position_y": 2250},
            {"id": 9, "position_x": 6000, "position_y": 6750},
            {"id": 10, "position_x": 8000, "position_y": 6750},
            {"id": 11, "position_x": 10000, "position_y": 6750}
        ]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase10():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(8000, 0),
        3,
        [
            {"id": 0, "position_x": 0, "position_y": 4500},
            {"id": 1, "position_x": 15999, "position_y": 4500},
            {"id": 2, "position_x": 8000, "position_y": 7999}
        ]
        ,
        23,
        [
            {"id": 0, "position_x": 2000, "position_y": 1200},
            {"id": 1, "position_x": 3000, "position_y": 1800},
            {"id": 2, "position_x": 4000, "position_y": 2400},
            {"id": 3, "position_x": 5000, "position_y": 3000},
            {"id": 4, "position_x": 6000, "position_y": 3600},
            {"id": 5, "position_x": 9000, "position_y": 5400},
            {"id": 6, "position_x": 10000, "position_y": 6000},
            {"id": 7, "position_x": 11000, "position_y": 6600},
            {"id": 8, "position_x": 12000, "position_y": 7200},
            {"id": 9, "position_x": 13000, "position_y": 7800},
            {"id": 10, "position_x": 14000, "position_y": 8400},
            {"id": 11, "position_x": 14000, "position_y": 600},
            {"id": 12, "position_x": 13000, "position_y": 1200},
            {"id": 13, "position_x": 12000, "position_y": 1800},
            {"id": 14, "position_x": 11000, "position_y": 2400},
            {"id": 15, "position_x": 10000, "position_y": 3000},
            {"id": 16, "position_x": 9000, "position_y": 3600},
            {"id": 17, "position_x": 6000, "position_y": 5400},
            {"id": 18, "position_x": 5000, "position_y": 6000},
            {"id": 19, "position_x": 4000, "position_y": 6600},
            {"id": 20, "position_x": 3000, "position_y": 7200},
            {"id": 21, "position_x": 2000, "position_y": 7800},
            {"id": 22, "position_x": 1000, "position_y": 8400}
        ]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase11():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(9000, 684),
        3,
        [{"id": 0, "position_x": 15999, "position_y": 4500},
         {"id": 1, "position_x": 8000, "position_y": 7999},
         {"id": 2, "position_x": 0, "position_y": 4500}]

        ,
        9,
        [{"id": 0, "position_x": 0, "position_y": 3033},
         {"id": 1, "position_x": 1500, "position_y": 6251},
         {"id": 2, "position_x": 3000, "position_y": 2502},
         {"id": 3, "position_x": 4500, "position_y": 6556},
         {"id": 4, "position_x": 6000, "position_y": 3905},
         {"id": 5, "position_x": 7500, "position_y": 5472},
         {"id": 6, "position_x": 10500, "position_y": 2192},
         {"id": 7, "position_x": 12000, "position_y": 6568},
         {"id": 8, "position_x": 13500, "position_y": 7448}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase12():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(8000, 4000),
        2,
        [{"id": 0, "position_x": 0, "position_y": 4000},
         {"id": 1, "position_x": 15000, "position_y": 4000}]

        ,
        9,
        [{"id": 0, "position_x": 4333, "position_y": 1800},
         {"id": 1, "position_x": 4333, "position_y": 3600},
         {"id": 2, "position_x": 4333, "position_y": 5400},
         {"id": 3, "position_x": 4333, "position_y": 7200},
         {"id": 4, "position_x": 10666, "position_y": 1800},
         {"id": 5, "position_x": 10666, "position_y": 3600},
         {"id": 6, "position_x": 10666, "position_y": 5400},
         {"id": 7, "position_x": 10666, "position_y": 7200},
         {"id": 8, "position_x": 0, "position_y": 7200}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase13():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(4920, 6810),
        10,
        [{"id": 0, "position_x": 50, "position_y": 4810},
         {"id": 1, "position_x": 14820, "position_y": 3870},
         {"id": 2, "position_x": 10869, "position_y": 8250},
         {"id": 3, "position_x": 9695, "position_y": 7220},
         {"id": 4, "position_x": 10160, "position_y": 5600},
         {"id": 5, "position_x": 12988, "position_y": 5820},
         {"id": 6, "position_x": 14892, "position_y": 5180},
         {"id": 7, "position_x": 881, "position_y": 1210},
         {"id": 8, "position_x": 7258, "position_y": 2130},
         {"id": 9, "position_x": 13029, "position_y": 6990}]

        ,
        14,
        [{"id": 0, "position_x": 11048, "position_y": 720},
         {"id": 1, "position_x": 2155, "position_y": 1650},
         {"id": 2, "position_x": 9618, "position_y": 2820},
         {"id": 3, "position_x": 12157, "position_y": 3770},
         {"id": 4, "position_x": 2250, "position_y": 5180},
         {"id": 5, "position_x": 8617, "position_y": 4890},
         {"id": 6, "position_x": 7028, "position_y": 960},
         {"id": 7, "position_x": 1518, "position_y": 280},
         {"id": 8, "position_x": 7996, "position_y": 4080},
         {"id": 9, "position_x": 13029, "position_y": 150},
         {"id": 10, "position_x": 3119, "position_y": 4600},
         {"id": 11, "position_x": 3339, "position_y": 4150},
         {"id": 12, "position_x": 894, "position_y": 7340},
         {"id": 13, "position_x": 7550, "position_y": 7550}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase14():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(8020, 3500),
        3,
        [{"id": 0, "position_x": 11000, "position_y": 1000},
         {"id": 1, "position_x": 11000, "position_y": 6000},
         {"id": 2, "position_x": 4000, "position_y": 3500}]
        ,
        5,
        [{"id": 0, "position_x": 15000, "position_y": 1000},
         {"id": 1, "position_x": 15000, "position_y": 6000},
         {"id": 2, "position_x": 120, "position_y": 3500},
         {"id": 3, "position_x": 0, "position_y": 4000},
         {"id": 4, "position_x": 120, "position_y": 3000}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase15():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(3900, 5000),
        4,
        [{"id": 0, "position_x": 3000, "position_y": 3000},
         {"id": 1, "position_x": 3000, "position_y": 5000},
         {"id": 2, "position_x": 3000, "position_y": 7000},
         {"id": 3, "position_x": 12000, "position_y": 3500}]

        ,
        6,
        [{"id": 0, "position_x": 10000, "position_y": 1000},
         {"id": 1, "position_x": 10000, "position_y": 6000},
         {"id": 2, "position_x": 15500, "position_y": 2000},
         {"id": 3, "position_x": 15500, "position_y": 3600},
         {"id": 4, "position_x": 15500, "position_y": 5000},
         {"id": 5, "position_x": 0, "position_y": 1200}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase16():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(3989, 3259),
        3,
        [{"id": 0, "position_x": 302, "position_y": 6109},
         {"id": 1, "position_x": 3671, "position_y": 981},
         {"id": 2, "position_x": 6863, "position_y": 809}]
        ,
        11,
        [{"id": 0, "position_x": 208, "position_y": 156},
         {"id": 1, "position_x": 10129, "position_y": 711},
         {"id": 2, "position_x": 13229, "position_y": 413},
         {"id": 3, "position_x": 203, "position_y": 3627},
         {"id": 4, "position_x": 7310, "position_y": 3912},
         {"id": 5, "position_x": 9814, "position_y": 3223},
         {"id": 6, "position_x": 13556, "position_y": 3668},
         {"id": 7, "position_x": 3923, "position_y": 6251},
         {"id": 8, "position_x": 6720, "position_y": 6574},
         {"id": 9, "position_x": 10387, "position_y": 6136},
         {"id": 10, "position_x": 13093, "position_y": 6253}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase17():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(3989, 3259),
        4,
        [{"id": 0, "position_x": 3647, "position_y": 384},
         {"id": 1, "position_x": 60, "position_y": 3262},
         {"id": 2, "position_x": 2391, "position_y": 1601},
         {"id": 3, "position_x": 2363, "position_y": 3422}]
        ,
        30,
        [{"id": 0, "position_x": 6485, "position_y": 499},
         {"id": 1, "position_x": 7822, "position_y": 446},
         {"id": 2, "position_x": 9202, "position_y": 826},
         {"id": 3, "position_x": 11060, "position_y": 253},
         {"id": 4, "position_x": 12568, "position_y": 808},
         {"id": 5, "position_x": 14148, "position_y": 650},
         {"id": 6, "position_x": 6571, "position_y": 1893},
         {"id": 7, "position_x": 8484, "position_y": 2013},
         {"id": 8, "position_x": 9669, "position_y": 1968},
         {"id": 9, "position_x": 7570, "position_y": 3338},
         {"id": 10, "position_x": 9780, "position_y": 3611},
         {"id": 11, "position_x": 8360, "position_y": 4767},
         {"id": 12, "position_x": 9804, "position_y": 4154},
         {"id": 13, "position_x": 10935, "position_y": 4977},
         {"id": 14, "position_x": 12310, "position_y": 4614},
         {"id": 15, "position_x": 13891, "position_y": 4302},
         {"id": 16, "position_x": 913, "position_y": 5636},
         {"id": 17, "position_x": 2410, "position_y": 5912},
         {"id": 18, "position_x": 3952, "position_y": 6143},
         {"id": 19, "position_x": 4615, "position_y": 5995},
         {"id": 20, "position_x": 6568, "position_y": 6085},
         {"id": 21, "position_x": 8204, "position_y": 5579},
         {"id": 22, "position_x": 9049, "position_y": 5470},
         {"id": 23, "position_x": 30, "position_y": 6798},
         {"id": 24, "position_x": 1798, "position_y": 6682},
         {"id": 25, "position_x": 3247, "position_y": 7664},
         {"id": 26, "position_x": 5005, "position_y": 7319},
         {"id": 27, "position_x": 6415, "position_y": 7094},
         {"id": 28, "position_x": 8159, "position_y": 7447},
         {"id": 29, "position_x": 9550, "position_y": 6847}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase18():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(3989, 3259),
        8,
        [{"id": 0, "position_x": 647, "position_y": 384},
         {"id": 1, "position_x": 60, "position_y": 1262},
         {"id": 2, "position_x": 1391, "position_y": 1601},
         {"id": 3, "position_x": 1363, "position_y": 422},
         {"id": 4, "position_x": 15470, "position_y": 384},
         {"id": 5, "position_x": 15060, "position_y": 1262},
         {"id": 6, "position_x": 11391, "position_y": 1601},
         {"id": 7, "position_x": 11363, "position_y": 422}]
        ,
        18,
        [{"id": 0, "position_x": 7900, "position_y": 1579},
         {"id": 1, "position_x": 8500, "position_y": 2470},
         {"id": 2, "position_x": 7500, "position_y": 3798},
         {"id": 3, "position_x": 6500, "position_y": 4682},
         {"id": 4, "position_x": 9000, "position_y": 5664},
         {"id": 5, "position_x": 7500, "position_y": 6319},
         {"id": 6, "position_x": 8500, "position_y": 7094},
         {"id": 7, "position_x": 7800, "position_y": 8447},
         {"id": 8, "position_x": 8100, "position_y": 8847},
         {"id": 9, "position_x": 0, "position_y": 7000},
         {"id": 10, "position_x": 1000, "position_y": 7900},
         {"id": 11, "position_x": 3000, "position_y": 8500},
         {"id": 12, "position_x": 5000, "position_y": 7500},
         {"id": 13, "position_x": 7000, "position_y": 6500},
         {"id": 14, "position_x": 9000, "position_y": 7000},
         {"id": 15, "position_x": 11000, "position_y": 7500},
         {"id": 16, "position_x": 13000, "position_y": 8500},
         {"id": 17, "position_x": 15000, "position_y": 7800}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase19():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(8000, 4500),
        2,
        [{"id": 0, "position_x": 3000, "position_y": 4500},
         {"id": 1, "position_x": 14000, "position_y": 4500}]
        ,
        2,
        [{"id": 0, "position_x": 2500, "position_y": 4500},
         {"id": 1, "position_x": 15500, "position_y": 6500}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase20():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(0, 4500),
        2,
        [{"id": 0, "position_x": 7000, "position_y": 3500},
         {"id": 1, "position_x": 0, "position_y": 500},
         {"id": 2, "position_x": 7000, "position_y": 5500},
         {"id": 3, "position_x": 3500, "position_y": 1000},
         {"id": 4, "position_x": 9250, "position_y": 8000},
         {"id": 5, "position_x": 13000, "position_y": 4500}]
        ,
        2,
        [{"id": 0, "position_x": 3600, "position_y": 3500},
         {"id": 1, "position_x": 3700, "position_y": 4500},
         {"id": 2, "position_x": 3400, "position_y": 6500},
         {"id": 3, "position_x": 9000, "position_y": 3500},
         {"id": 4, "position_x": 8990, "position_y": 4500},
         {"id": 5, "position_x": 9000, "position_y": 5500},
         {"id": 6, "position_x": 11000, "position_y": 4000},
         {"id": 7, "position_x": 9100, "position_y": 10}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_testCase21():
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(
        Position(7992, 8304),
        15,
        [{"id": 0, "position_x": 757, "position_y": 3545},
         {"id": 1, "position_x": 510, "position_y": 8170},
         {"id": 2, "position_x": 1119, "position_y": 733},
         {"id": 3, "position_x": 1416, "position_y": 7409},
         {"id": 4, "position_x": 1110, "position_y": 8488},
         {"id": 5, "position_x": 2118, "position_y": 1983},
         {"id": 6, "position_x": 3167, "position_y": 480},
         {"id": 7, "position_x": 6576, "position_y": 664},
         {"id": 8, "position_x": 8704, "position_y": 1276},
         {"id": 9, "position_x": 13340, "position_y": 5663},
         {"id": 10, "position_x": 13808, "position_y": 4731},
         {"id": 11, "position_x": 15355, "position_y": 3528},
         {"id": 12, "position_x": 15495, "position_y": 5035},
         {"id": 13, "position_x": 15182, "position_y": 6184},
         {"id": 14, "position_x": 15564, "position_y": 7640}]
        ,
        7,
        [{"id": 0, "position_x": 3996, "position_y": 4152},
         {"id": 1, "position_x": 3996, "position_y": 4844},
         {"id": 2, "position_x": 3996, "position_y": 7612},
         {"id": 3, "position_x": 5328, "position_y": 1384},
         {"id": 4, "position_x": 7992, "position_y": 3460},
         {"id": 5, "position_x": 11322, "position_y": 5536},
         {"id": 6, "position_x": 11322, "position_y": 8304}]
    )

    final_score = simulator.simulate(initial_game, ai)
    pytest.total_score += final_score
    assert final_score > 0


def test_display_total_score():
    print(pytest.total_score)
