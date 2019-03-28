import sys
import math
import json
import uuid
import random
import copy

DEBUG = True

ZONE_WIDTH = 16000
ZONE_HEIGHT = 9000
ZOMBIE_MOVE = 400
ZOMBIE_RANGE = 400
ASH_MOVE = 1000
ASH_RANGE = 2000


def print_debug(description):
    if DEBUG:
        print(description, file=sys.stderr)


def safe_division(num, denom):
    if denom == 0:
        denom = 1

    return num / denom


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

    def add_vector(self, vector):
        return Position(math.floor(self.x + vector.x), math.floor(self.y + vector.y))


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)


class Human:
    def __init__(self, id, position):
        self.id = id
        self.position = position

    def __str__(self):
        return "id: {}, type: 'human', position: {}".format(self.id, self.position)


class Zombie:
    def __init__(self, id, position, next_position):
        self.id = id
        self.position = position
        self.next_position = next_position

    def __str__(self):
        return "id: {}, type: 'zombie', position: {}, next_position: {}".format(self.id, self.position, self.next_position)


class Simulator:
    def __init__(self):
        pass

    def initialize_game(self, ash_position, nb_humans, human_objects, nb_zombies, zombie_objects):
        def initialize_ash(ash_position):
            if ash_position is None:
                return Human(None, Position(0, 0))
            else:
                return Human(None, ash_position)

        def initialize_humans(nb_humans, human_objects):
            if len(human_objects) > 0:
                humans = [Human(human_object["id"], Position(human_object["position_x"], human_object["position_y"])) for human_object in human_objects]
                return humans
            else:
                humans = []
                for i in range(nb_humans):
                    alea_x = random.randint(0, ZONE_WIDTH)
                    alea_y = random.randint(0, ZONE_HEIGHT)
                    human = Human(i, Position(alea_x, alea_y))
                    humans.append(human)
                return humans

        def initialize_zombies(nb_zombies, zombie_objects):
            if len(zombie_objects) > 0:
                zombies = [Zombie(zombie_object["id"], Position(zombie_object["position_x"], zombie_object["position_y"]), None) for zombie_object in zombie_objects]
                return zombies
            else:
                zombies = []
                for i in range(nb_zombies):
                    alea_x = random.randint(0, ZONE_WIDTH)
                    alea_y = random.randint(0, ZONE_HEIGHT)
                    zombies.append(Zombie(i, Position(alea_x, alea_y), None))
                return zombies

        ash = initialize_ash(ash_position)
        humans = initialize_humans(nb_humans, human_objects)
        zombies = initialize_zombies(nb_zombies, zombie_objects)

        return Game(ash, nb_humans, humans, nb_zombies, zombies)

    def play_round(self, initial_game, ash_target_position):
        def get_fibonacci():
            return [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]

        def move_zombies(initial_game):
            zombies = initial_game.zombies
            humans = initial_game.humans
            ash = initial_game.ash
            new_zombies = []

            for zombie in zombies:
                humans_distances = game.get_distances_between_person_and_others(zombie, humans + [ash])
                if len(humans_distances) > 0:
                    target = sorted(humans_distances, key=lambda tuple: tuple[1])[0][0]
                else:
                    target = ash

                vector_towards_target = Vector(target.position.x - zombie.position.x, target.position.y - zombie.position.y)
                # print_debug("------ for zombie")
                # print_debug("vector: {}".format(vector_towards_target))
                distance_between = zombie.position.distance_with(target.position)
                # print_debug("distance: {}".format(distance_between))

                if distance_between <= ZOMBIE_RANGE:
                    new_zombie_position = target.position
                else:
                    unit_vector_towards_target = Vector(safe_division(vector_towards_target.x, distance_between), safe_division(vector_towards_target.y, distance_between))
                    # print_debug("unit vector: {}".format(unit_vector_towards_target))
                    zombie_move_vector = Vector(unit_vector_towards_target.x * ZOMBIE_MOVE, unit_vector_towards_target.y * ZOMBIE_MOVE)
                    # print_debug("move vector: {}".format(zombie_move_vector))
                    new_zombie_position = zombie.position.add_vector(zombie_move_vector)

                new_zombies.append(Zombie(zombie.id, new_zombie_position, None))

            new_game = Game(initial_game.ash, initial_game.humans_count, initial_game.humans, initial_game.zombies_count, new_zombies)
            return new_game

        def move_ash(initial_game, target_position):
            ash_position = initial_game.ash.position
            vector_towards_target = Vector(target_position.x - ash_position.x, target_position.y - ash_position.y)
            distance_between = ash_position.distance_with(target_position)
            unit_vector_towards_target = Vector(safe_division(vector_towards_target.x, distance_between), safe_division(vector_towards_target.y, distance_between))
            ash_move_vector = Vector(unit_vector_towards_target.x * ASH_MOVE, unit_vector_towards_target.y * ASH_MOVE)
            new_ash_position = ash_position.add_vector(ash_move_vector)

            new_game = Game(
                Human(None, new_ash_position),
                initial_game.humans_count,
                initial_game.humans,
                initial_game.zombies_count,
                initial_game.zombies
            )
            return new_game

        def kill_zombies(initial_game):
            ash_position = initial_game.ash.position
            zombies = initial_game.zombies
            score = 0

            zombies_in_range = [zombie for zombie in zombies if ash_position.distance_with(zombie.position) <= ASH_RANGE]
            zombies_not_in_range = [zombie for zombie in zombies if ash_position.distance_with(zombie.position) > ASH_RANGE]
            remaining_humans_count = initial_game.humans_count

            for index, zombie in enumerate(zombies_in_range):
                # print_debug("KILL zombie {}!!!".format(zombie.id))
                index = index
                score += (remaining_humans_count * remaining_humans_count) * 10 * (get_fibonacci()[index + 2])

            updated_game = Game(
                initial_game.ash,
                initial_game.humans_count,
                initial_game.humans,
                len(zombies_not_in_range),
                zombies_not_in_range
            )

            return updated_game, score

        def eat_humans(initial_game):
            zombies = initial_game.zombies
            humans = initial_game.humans

            alive_humans = []
            for human in humans:
                closed_zombies = [zombie for zombie in zombies if human.position.distance_with(zombie.position) == 0]

                if len(closed_zombies) == 0:
                    alive_humans.append(human)

            updated_game = Game(
                initial_game.ash,
                len(alive_humans),
                alive_humans,
                initial_game.zombies_count,
                initial_game.zombies
            )

            return updated_game

        game = copy.deepcopy(initial_game)

        game = move_zombies(game)
        game = move_ash(game, ash_target_position)
        game, score = kill_zombies(game)
        game = eat_humans(game)

        return game, score

    def simulate(self, initial_game, ai):
        game = copy.deepcopy(initial_game)

        total_score = 0
        round_count = 2

        while not game.are_all_humans_dead() and game.zombies_count > 0:
            # print_debug("========= Round {}: points: {} =====\n{}\n".format(round_count, total_score, game))
            ash_target_position = ai.kill_nearest_zombie_strategy(game)
            game, score = self.play_round(game, ash_target_position)
            total_score += score
            round_count += 1

        if game.are_all_humans_dead():
            total_score = 0

        return total_score


class AI:
    def kill_nearest_zombie_strategy(self, game):
        distances = game.get_distances_between_person_and_others(game.ash, game.zombies)
        nearest_zombies = sorted(distances, key=lambda tuple: tuple[1])

        if len(nearest_zombies) > 0:
            nearest_zombie = nearest_zombies[0][0]
        else:
            nearest_zombie = None

        if nearest_zombie is not None:
            target_position = Position(nearest_zombie.position.x, nearest_zombie.position.y)
        else:
            target_position = Position(0, 0)

        return target_position


class Game:
    def __init__(self, ash, humans_count, humans, zombies_count, zombies):
        self.ash = ash
        self.humans_count = humans_count
        self.humans = humans
        self.zombies_count = zombies_count
        self.zombies = zombies

    def __str__(self):
        return "ash: {}\n---- Humans ----\n{}\n----Zombies ----\n{}".format(
            self.ash,
            "\n".join([str(human) for human in self.humans]),
            "\n".join([str(zombie) for zombie in self.zombies])
        )

    def are_all_humans_dead(self):
        return len(self.humans) == 0

    def get_distances_between_person_and_others(self, person, others):
        """

        :param person:
        :type person: Human or Zombie
        :param others:
        :type others: Human or Zombie
        :return:
        :rtype:
        """

        return [(other, person.position.distance_with(other.position)) for other in others]


if __name__ == '__main__':
    # while True:
    #     x, y = [int(i) for i in input().split()]
    #     ash = Human(None, Position(x, y))
    #
    #     humans = []
    #     human_count = int(input())
    #     for i in range(human_count):
    #         human_id, human_x, human_y = [int(j) for j in input().split()]
    #         humans.append(Human(human_id, Position(human_x, human_y)))
    #
    #     zombies = []
    #     zombie_count = int(input())
    #     for i in range(zombie_count):
    #         zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
    #         zombies.append(Zombie(zombie_id, Position(zombie_x, zombie_y), Position(zombie_xnext, zombie_ynext)))
    #
    #     game = Game(ash, human_count, humans, zombie_count, zombies)
    #
    #     print_debug(game)
    #
    #     order = game.play()
    #     print(order)
    simulator = Simulator()
    ai = AI()
    initial_game = simulator.initialize_game(Position(5000, 0),
                                             1,
                                             [{"id": 0, "position_x": 950, "position_y": 6000}, {"id": 1, "position_x": 8000, "position_y": 6100}],
                                             1,
                                             [{"id": 0, "position_x": 3100, "position_y": 7000}, {"id": 1, "position_x": 11500, "position_y": 7100}]
                                             )
    final_score = simulator.simulate(initial_game, ai)

    print_debug("Final score: {}".format(final_score))
