import sys
import math
import copy

DEBUG = True


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

    def add_tile(self, row_index, column_index, tile_string):
        self.tiles[column_index].append(tile_string)

    def can_turn_left(self, current_position, current_direction):
        column_index = current_position.x
        row_index = current_position.y

        if current_direction == ">":
            return row_index - 1 >= 0 and self.tiles[column_index][max(0, row_index - 1)] != '#', Position(current_position.x, current_position.y - 1), "^"
        elif current_direction == "<":
            return row_index + 1 < self.height and self.tiles[column_index][min(self.height - 1, row_index + 1)] != '#', Position(current_position.x, current_position.y + 1), "v"
        elif current_direction == "^":
            return column_index - 1 >= 0 and self.tiles[max(column_index - 1, 0)][row_index] != '#', Position(current_position.x - 1, current_position.y), "<"
        elif current_direction == "v":
            return column_index + 1 < self.width and self.tiles[min(self.width - 1, column_index + 1)][row_index] != '#', Position(current_position.x + 1, current_position.y), ">"

    def can_turn_right(self, current_position, current_direction):
        column_index = current_position.x
        row_index = current_position.y

        if current_direction == ">":
            return row_index + 1 < self.height and self.tiles[column_index][min(self.height - 1, row_index + 1)] != '#', Position(current_position.x, current_position.y + 1), "v"
        elif current_direction == "<":
            return row_index - 1 >= 0 and self.tiles[column_index][max(0, row_index - 1)] != '#', Position(current_position.x, current_position.y - 1), "^"
        elif current_direction == "^":
            return column_index + 1 < self.width and self.tiles[min(self.width - 1, column_index + 1)][row_index] != '#', Position(current_position.x + 1, current_position.y), ">"
        elif current_direction == "v":
            return column_index - 1 >= 0 and self.tiles[max(column_index - 1, 0)][row_index] != '#', Position(current_position.x - 1, current_position.y), "<"

    def can_go_ahead(self, current_position, current_direction):
        column_index = current_position.x
        row_index = current_position.y

        if current_direction == ">":
            return column_index + 1 < self.width and self.tiles[min(self.width - 1, column_index + 1)][row_index] != '#', Position(current_position.x + 1, current_position.y), ">"
        elif current_direction == "<":
            return column_index - 1 >= 0 and self.tiles[max(column_index - 1, 0)][row_index] != '#', Position(current_position.x - 1, current_position.y), "<"
        elif current_direction == "^":
            return row_index - 1 >= 0 and self.tiles[column_index][max(0, row_index - 1)] != '#', Position(current_position.x, current_position.y - 1), "^"
        elif current_direction == "v":
            return row_index + 1 < self.height and self.tiles[column_index][min(self.height - 1, row_index + 1)] != '#', Position(current_position.x, current_position.y + 1), "v"

    def can_go_reverse(self, current_position, current_direction):
        column_index = current_position.x
        row_index = current_position.y

        if current_direction == ">":
            return column_index - 1 >= 0 and self.tiles[max(column_index - 1, 0)][row_index] != '#', Position(current_position.x - 1, current_position.y), "<"
        elif current_direction == "<":
            return column_index + 1 < self.width and self.tiles[min(self.width - 1, column_index + 1)][row_index] != '#', Position(current_position.x + 1, current_position.y), ">"
        elif current_direction == "^":
            return row_index + 1 < self.height and self.tiles[column_index][min(self.height - 1, row_index + 1)] != '#', Position(current_position.x, current_position.y + 1), "v"
        elif current_direction == "v":
            return row_index - 1 >= 0 and self.tiles[column_index][max(0, row_index - 1)] != '#', Position(current_position.x, current_position.y - 1), "^"

    def move(self, current_position, current_direction, wall_to_follow):

        if wall_to_follow == "L":
            can_left, new_position, new_direction = self.can_turn_left(current_position, current_direction)
            if can_left:
                return new_position, new_direction
            can_go_ahead, new_position, new_direction = self.can_go_ahead(current_position, current_direction)
            if can_go_ahead:
                return new_position, new_direction
            can_right, new_position, new_direction = self.can_turn_right(current_position, current_direction)
            if can_right:
                return new_position, new_direction
            can_go_reverse, new_position, new_direction = self.can_go_reverse(current_position, current_direction)
            if can_go_reverse:
                return new_position, new_direction
            else:
                return current_position, current_direction

        else:
            can_right, new_position, new_direction = self.can_turn_right(current_position, current_direction)
            if can_right:
                return new_position, new_direction
            can_go_ahead, new_position, new_direction = self.can_go_ahead(current_position, current_direction)
            if can_go_ahead:
                return new_position, new_direction
            can_left, new_position, new_direction = self.can_turn_left(current_position, current_direction)
            if can_left:
                return new_position, new_direction
            can_go_reverse, new_position, new_direction = self.can_go_reverse(current_position, current_direction)
            if can_go_reverse:
                return new_position, new_direction
            else:
                return current_position, current_direction

    def find_start_position(self):
        for row_index in range(self.height):
            for column_index in range(self.width):
                if self.tiles[column_index][row_index] != '0' and self.tiles[column_index][row_index] != '#':
                    return Position(column_index, row_index)

    def solve(self, wall_to_follow):
        resMap = copy.deepcopy(self)
        start_position = self.find_start_position()
        start_direction = self.tiles[start_position.x][start_position.y]

        print_debug(start_position)
        print_debug(start_direction)

        resMap.tiles[start_position.x][start_position.y] = 0
        new_position, new_direction = self.move(start_position, start_direction, wall_to_follow)
        print_debug("{} : {}".format(new_position, new_direction))
        if not new_position.is_equal(start_position):
            resMap.tiles[new_position.x][new_position.y] = int(resMap.tiles[new_position.x][new_position.y]) + 1
        print_debug(resMap)

        debug_counter = 0
        while not new_position.is_equal(start_position):
            # debug_counter += 1
            # print_debug(debug_counter)
            new_position, new_direction = self.move(new_position, new_direction, wall_to_follow)
            print_debug("{} : {}".format(new_position, new_direction))
            resMap.tiles[new_position.x][new_position.y] = int(resMap.tiles[new_position.x][new_position.y]) + 1
            print_debug(resMap)

        return resMap


if __name__ == '__main__':

    width, height = [int(i) for i in input().split()]
    map = Map(width, height)

    for row_index in range(height):
        for column_index, tile in enumerate(input()):
            map.add_tile(row_index, column_index, tile)

    wall_to_follow = input()

    print_debug(map)
    print_debug(wall_to_follow)

    res = map.solve(wall_to_follow)

    print(res)
