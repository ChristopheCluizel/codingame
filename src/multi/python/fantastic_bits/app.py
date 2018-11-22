import sys
import math
import copy

def printd(message):
    print(message, file=sys.stderr)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)


class Speed:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def __str__(self):
        return "vx: {}, vy: {}".format(self.vx, self.vy)


class Goals:
    def __init__(self):
        self.left_goal = [Pole(Position(0, 1750), 300), Pole(Position(0, 5750), 300)]
        self.right_goal = [Pole(Position(16000, 1750), 300), Pole(Position(16000, 5750), 300)]

    def __str__(self):
        left_goal_string = "Pole1: {}    |    pole2: {}".format(self.left_goal[0], self.left_goal[1])
        right_goal_string = "Pole1: {}    |    pole2: {}".format(self.right_goal[0], self.right_goal[1])
        return "---- Left goal\n{}\n---- Right goal\n{}".format(left_goal_string, right_goal_string)

    def get_center(self, side):
        """
        Get the center position of a goal.

        :param side: LEFT or RIGHT
        :type side: string
        :return: the center position of a goal
        :rtype: Position
        """
        if side == "LEFT":
            return Position(0, 3750)
        else:
            return Position(16000, 3750)


class Pole:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def __str__(self):
        return "Position: {}, radius: {}".format(self.position, self.radius)


class Entity:
    def __init__(self, id, type, position, speed, state):
        self.id = id
        self.type = type
        self.position = position
        self.speed = speed
        self.state = state

    def __str__(self):
        return "id: {}, type: {}, position: {}, speed: {}, state: {}".format(
            self.id,
            self.type,
            self.position,
            self.speed,
            self.state
        )


class Snaffle(Entity):
    def __init__(self, id, type, position, speed, state):
        Entity.__init__(self, id, "SNAFFLE", position, speed, state)


class Wizard(Entity):
    def __init__(self, id, type, position, speed, state):
        Entity.__init__(self, id, "WIZARD", position, speed, state)


class Map:
    def __init__(self):
        self.width = 16001
        self.height = 7501
        self.goals = Goals

    def __str__(self):
        return ""


class Team:
    def __init__(self, id, score, magic):
        self.id = id
        self.score = score
        self.magic = magic

    def __str__(self):
        return "id: {}, score: {}, magic: {}".format(self.id, self.score, self.magic)


class Game:
    def __init__(self, my_team, enemy_team, map, entities):
        """

        :param map:
        :type map: Map
        :param entities:
        :type entities: list(Entity)
        """
        self.my_team = my_team
        self.enemy_team = enemy_team
        self.map = map
        self.entities = entities

    def __str__(self):
        return "---- my team\n{}\n---- enemy team\n{}\n---- entities\n{}".format(
            self.my_team,
            self.enemy_team,
            "\n".join([str(entity) for entity in self.entities])
        )


my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left

my_team = Team(my_team_id, 0, None)
enemy_team = Team(int(not my_team_id), 0, None)

map = Map()
game = Game(my_team, enemy_team, map, [])

# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
    opponent_score, opponent_magic = [int(i) for i in input().split()]

    my_team.score = my_score
    my_team.magic = my_magic
    enemy_team.score = opponent_score
    enemy_team.magic = opponent_magic

    entities_number = int(input())  # number of entities still in game
    entities = []
    for i in range(entities_number):
        # entity_id: entity identifier
        # entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        # x: position
        # y: position
        # vx: velocity
        # vy: velocity
        # state: 1 if the wizard is holding a Snaffle, 0 otherwise
        entity_id, entity_type, x, y, vx, vy, state = input().split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        state = int(state)
        entities.append(Entity(entity_id, entity_type, Position(x, y), Speed(vx, vy), state))
        game.entities = entities

    printd(game)

    for i in range(2):
        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        print("MOVE 8000 3750 100")
