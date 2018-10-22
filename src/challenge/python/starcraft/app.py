import sys
import copy


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)


class Robot:
    def __init__(self, id, position, direction):
        """
        :param id:
        :type id: integer
        :param position:
        :type position: Position
        :param direction:
        :type direction: string
        """
        self.id = id
        self.position = position
        self.direction = direction

    def __str__(self):
        return "id: {}, position: {}, direction: {}".format(self.id, self.position, self.direction)

    def move(self):
        if self.direction == 'R':
            self.position = Position(self.position.x + 1, self.position.y)
        elif self.direction == 'L':
            self.position = Position(self.position.x - 1, self.position.y)
        elif self.direction == 'U':
            self.position = Position(self.position.x, self.position.y - 1)
        else:
            self.position = Position(self.position.x, self.position.y + 1)


class Map:
    def __init__(self):
        self.width = 19
        self.height = 10
        self.grid = [['#' for x in range(self.width)] for y in range(self.height)]

    def __str__(self):
        string = "==== Map ====\n"
        for i in range(0, self.height):
            for j in range(0, self.width):
                string += self.grid[i][j]
            string += '\n'
        return string

    def get_platforms_positions(self):
        platforms_positions = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.grid[i][j] == '.':
                    platforms_positions.append(Position(j, i))
        return platforms_positions


class Game:
    def __init__(self, map, nb_robots, robots):
        self.map = map
        self.nb_robots = nb_robots
        self.robots = robots
        self.point = 0

    def __str__(self):
        return "{}\n==== Robots ====\n{}\n\n".format(self.map, '\n'.join([str(robot) for robot in self.robots]))

    def is_end_game(self):
        is_robot_out_of_game = False
        if len(["falling" for robot in self.robots if self.map.grid[robot.position.y][robot.position.x] == '#']) != 0:
            is_robot_out_of_game = True

        return is_robot_out_of_game

    def move_robots(self):
        for robot in self.robots:
            robot.move()

    def increase_point(self):
        for robot in self.robots:
            if self.map.grid[robot.position.y][robot.position.x] != '#':
                self.point += 1

    def set_robots_direction(self):
        for robot in self.robots:
            square = self.map.grid[robot.position.y][robot.position.x]
            if square in ['R', 'L', 'U', 'D']:
                robot.direction = square

    def play(self):
        while not self.is_end_game():
            self.increase_point()
            self.set_robots_direction()
            self.move_robots()

    def add_arrows(self, arrows):
        """

        :param arrows:
        :type arrows: list[string]
        :return:
        :rtype: list[string]
        """
        for arrow in arrows:
            x, y, direction = arrow.split(" ")
            x = int(x)
            y = int(y)
            self.map.grid[y][x] = direction

    def find_arrows(self):
        possible_positions = self.map.get_platforms_positions()
        possible_directions = ['U', 'D', 'R', 'L']

        # print('---- possible start ----')
        # print([str(position) for position in possible_positions])
        # print('---- possible end ----')

        tries = []
        for position in possible_positions:
            for direction in possible_directions:
                arrow = "{} {} {}".format(position.x, position.y, direction)
                virtual_game = copy.deepcopy(self)
                virtual_game.add_arrows([arrow])
                virtual_game.play()
                tries.append((arrow, virtual_game.point))

        print(tries, file=sys.stderr)
        best_try = sorted(tries, key=lambda x: x[1], reverse=True)[0]

        print(best_try, file=sys.stderr)

        return [best_try[0]]


DEBUG = True

map = Map()
for i in range(10):
    line = input()
    map.grid[i] = list(line)

robot_count = int(input())
robots = []
for i in range(robot_count):
    x, y, direction = input().split()
    x = int(x)
    y = int(y)
    robots.append(Robot(i, Position(x, y), direction))

game = Game(map, robot_count, robots)
arrows = game.find_arrows()

if DEBUG:
    game.add_arrows(arrows)
    print(game, file=sys.stderr)
    game.play()
    print("====== Points: {} ====".format(game.point), file=sys.stderr)
else:
    print(game, file=sys.stderr)
    print(" ".join(arrows))
