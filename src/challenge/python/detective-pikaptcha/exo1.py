import sys
import math
import copy

DEBUG = False


def print_debug(description):
    if DEBUG:
        print(description, file=sys.stderr)


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

    def solve(self):
        resMap = copy.deepcopy(self)
        print_debug(resMap)

        for row_index in range(self.height):
            for column_index in range(self.width):
                if self.tiles[column_index][row_index] == '0':
                    counter = 0
                    if column_index - 1 >= 0 and self.tiles[max(column_index - 1, 0)][row_index] == '0':
                        counter += 1
                    if column_index + 1 < self.width and self.tiles[min(self.width - 1, column_index + 1)][row_index] == '0':
                        counter += 1
                    if row_index - 1 >= 0 and self.tiles[column_index][max(0, row_index - 1)] == '0':
                        counter += 1
                    if row_index + 1 < self.height and self.tiles[column_index][min(self.height - 1, row_index + 1)] == '0':
                        counter += 1
                    print_debug(counter)
                    resMap.tiles[column_index][row_index] = counter

                else:
                    resMap.tiles[column_index][row_index] = "#"

        print_debug(resMap)
        return resMap


if __name__ == '__main__':

    width, height = [int(i) for i in input().split()]
    map = Map(width, height)

    for row_index in range(height):
        for column_index, tile in enumerate(input()):
            map.add_tile(row_index, column_index, tile)

    print(map.solve())
