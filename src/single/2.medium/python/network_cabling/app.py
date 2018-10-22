import sys
import math
import statistics


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def distance_with(self, that):
        return math.sqrt((that.x - self.x) * (that.x - self.x) + (that.y - self.y) * (that.y - self.y))


class House:
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return "House: {}".format(self.position)


class Game:
    def __init__(self, nb_houses, houses):
        self.nb_houses = nb_houses
        self.houses = houses

    def __str__(self):
        return "==== Houses: {} ====\n{}".format(self.nb_houses, "\n".join([str(house) for house in self.houses]))

    def print_debug(self, message):
        print(message, file=sys.stderr)

    def get_horizontal_cable_length(self, min_x, max_x):
        return Position(min_x, 0).distance_with(Position(max_x, 0))

    def get_vertical_cable_length(self, y_median):
        vertical_lengths = []
        for house in self.houses:
            house_x = house.position.x
            median_position = Position(house_x, y_median)
            res = median_position.distance_with(house.position)
            vertical_lengths.append(res)
        return sum(vertical_lengths)

    def play(self):
        sorted_x_houses = [house.position.x for house in self.houses]
        min_x = min(sorted_x_houses)
        max_x = max(sorted_x_houses)
        sorted_y_houses = sorted(self.houses, key=lambda house: house.position.y)
        y_median = round(statistics.median([house.position.y for house in sorted_y_houses]))

        horizontal = self.get_horizontal_cable_length(min_x, max_x)
        vertical = self.get_vertical_cable_length(y_median)

        self.print_debug("horizontal: {}, vertical: {}".format(horizontal, vertical))

        res = horizontal + vertical

        return int(res)


def my_main():
    number_of_houses = int(input())
    houses = []
    for i in range(number_of_houses):
        x, y = [int(j) for j in input().split()]
        houses.append(House(Position(x, y)))

    game = Game(number_of_houses, houses)

    game.print_debug(game)

    res = game.play()

    print(res)


if __name__ == '__main__':
    my_main()
