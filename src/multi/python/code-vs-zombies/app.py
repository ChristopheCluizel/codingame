import sys
import math
from math import sqrt
import json
import uuid
import random
import time

DEBUG = False

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
        return sqrt((that.x - self.x) * (that.x - self.x) + (that.y - self.y) * (that.y - self.y))


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

    def play_round(self, ash, humans, zombies, ash_target_position):
        def get_fibonacci(index):
            return [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811][index]

        def get_new_position(old_position, target_position, move_length):
            old_x = old_position.x
            old_y = old_position.y

            xb_xa = target_position.x - old_x
            yb_ya = target_position.y - old_y
            distance = sqrt((xb_xa * xb_xa) + (yb_ya * yb_ya))

            return Position(math.floor(old_x + safe_division(xb_xa, distance) * move_length),
                            math.floor(old_y + safe_division(yb_ya, distance) * move_length))

        def get_distances_between_person_and_others(person, others):
            """

            :param person:
            :type person: Human or Zombie
            :param others:
            :type others: Human or Zombie
            :return:
            :rtype:
            """

            return [(other, person.position.distance_with(other.position)) for other in others]

        def move_zombies(ash, humans, zombies):
            new_zombies = []

            for zombie in zombies:
                humans_distances = get_distances_between_person_and_others(zombie, humans + [ash])
                sorted_humans_distances = sorted(humans_distances, key=lambda tuple: tuple[1])
                target = sorted_humans_distances[0][0]
                distance_between = sorted_humans_distances[0][1]

                if distance_between <= ZOMBIE_RANGE:
                    new_zombie_position = target.position
                else:
                    new_zombie_position = get_new_position(zombie.position, target.position, ZOMBIE_MOVE)

                new_zombies.append(Zombie(zombie.id, new_zombie_position, None))

            return new_zombies

        def move_ash(ash_position, target_position):
            return get_new_position(ash_position, target_position, ASH_MOVE)

        def kill_zombies(ash_position, remaining_humans_count, zombies):
            score = 0
            killed_zombie_counter = 0
            zombies_not_in_range = []

            for zombie in zombies:
                if ash_position.distance_with(zombie.position) <= ASH_RANGE:
                    score += (remaining_humans_count * remaining_humans_count) * 10 * (get_fibonacci(killed_zombie_counter + 2))
                    killed_zombie_counter += 1
                else:
                    zombies_not_in_range.append(zombie)

            return zombies_not_in_range, score

        def eat_humans(humans, zombies):
            alive_humans = []
            for human in humans:
                closed_zombies = [zombie for zombie in zombies if human.position.distance_with(zombie.position) == 0]

                if len(closed_zombies) == 0:
                    alive_humans.append(human)

            return alive_humans

        new_zombies = move_zombies(ash, humans, zombies)
        new_ash_position = move_ash(ash.position, ash_target_position)
        new_zombies, score = kill_zombies(new_ash_position, len(humans), new_zombies)
        new_humans = eat_humans(humans, new_zombies)

        return Game(Human(None, new_ash_position), len(new_humans), new_humans, len(new_zombies), new_zombies), score

    def simulate(self, game):
        def random_strategy(round_counter, zombies, targeted_zombie):
            if round_counter <= random.randint(0, 1):
                return Human(None, Position(random.randint(0, ZONE_WIDTH), random.randint(0, ZONE_HEIGHT)))
            else:
                if targeted_zombie.id in [zombie.id for zombie in zombies]:
                    return targeted_zombie
                else:
                    random_index = random.randint(0, len(zombies) - 1)
                    targeted_zombie = zombies[random_index]
                    return targeted_zombie

        ash_target = Zombie(10000, Position(0, 0), None)
        round_counter = 0
        total_score = 0
        first_move = game.zombies[0]

        while not game.are_all_humans_dead() and game.zombies_count > 0:
            ash_target = random_strategy(round_counter, game.zombies, ash_target)
            ash_target_position = ash_target.position
            # save the first move of Ash
            if round_counter == 0:
                first_move = ash_target_position
            game, score = self.play_round(game.ash, game.humans, game.zombies, ash_target_position)
            total_score += score
            round_counter += 1

        if game.are_all_humans_dead():
            total_score = 0

        return total_score, first_move


class Game:
    def __init__(self, ash, humans_count, humans, zombies_count, zombies):
        self.ash = ash
        self.humans_count = humans_count
        self.humans = humans
        self.zombies_count = zombies_count
        self.zombies = zombies
        self.round_counter = 0

    def __str__(self):
        return "round: {}, ash: {}\n---- Humans ----\n{}\n----Zombies ----\n{}".format(
            self.round_counter,
            self.ash,
            "\n".join([str(human) for human in self.humans]),
            "\n".join([str(zombie) for zombie in self.zombies])
        )

    def are_all_humans_dead(self):
        return len(self.humans) == 0

    def get_best_move(self):
        best_move = self.zombies[0].position
        best_score = 0

        start_time = time.time() * 1000

        i = 0
        for i in range(0, 10000):
            score, move = simulator.simulate(self)
            if score > best_score:
                best_score = score
                best_move = move
            during_time = time.time() * 1000

            if during_time - start_time >= 98:
                break

        print_debug("Nb of simulation: {}".format(i))

        return best_score, best_move


simulator = Simulator()

if __name__ == '__main__':
    while True:
        x, y = [int(i) for i in input().split()]
        ash = Human(None, Position(x, y))

        human_count = int(input())
        humans = [None] * human_count
        for i in range(human_count):
            human_id, human_x, human_y = [int(j) for j in input().split()]
            humans[i] = Human(human_id, Position(human_x, human_y))

        zombie_count = int(input())
        zombies = [None] * zombie_count
        for i in range(zombie_count):
            zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
            zombies[i] = (Zombie(zombie_id, Position(zombie_x, zombie_y), None))

        game = Game(ash, human_count, humans, zombie_count, zombies)

        # print_debug(game)

        best_score, best_move = game.get_best_move()
        game.round_counter += 1
        print("{} {}".format(best_move.x, best_move.y))
