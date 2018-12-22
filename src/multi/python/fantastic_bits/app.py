import sys
import math
import copy

DEBUG = False

def printd(message):
    if DEBUG:
        print(message, file=sys.stderr)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def distance_with(self, that):
        return math.sqrt((that.x - self.x) * (that.x - self.x) + (that.y - self.y) * (that.y - self.y))


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
    def __init__(self, id, position, speed, state):
        Entity.__init__(self, id, "SNAFFLE", position, speed, state)

    def is_free(self):
        return not self.state


class Wizard(Entity):
    def __init__(self, id, position, speed, state):
        Entity.__init__(self, id, "WIZARD", position, speed, state)


class Map:
    def __init__(self):
        self.width = 16001
        self.height = 7501
        self.goals = Goals()

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

    def get_wizards(self, team_id):
        """

        :param team_id:
        :type team_id: integer
        :return:
        :rtype: list(Wizard)
        """
        if team_id == self.my_team.id:
            return [Wizard(entity.id, entity.position, entity.speed, entity.state) for entity in self.entities if entity.type == "WIZARD"]
        else:
            return [Wizard(entity.id, entity.position, entity.speed, entity.state) for entity in self.entities if entity.type == "OPPONENT_WIZARD"]

    def get_enemy_goal(self, my_team_id):
        if my_team_id == 0:
            return map.goals.get_center("RIGHT")
        else:
            return map.goals.get_center("LEFT")

    def get_closest_snaffle(self, wizard_position):
        """

        :param wizard_position:
        :type wizard_position: Position
        :return:
        :rtype: Snaffle
        """
        free_snaffles = [Snaffle(entity.id, entity.position, entity.speed, entity.state) for entity in self.entities if entity.type == "SNAFFLE" and entity.state == 0]
        if len(free_snaffles) != 0:
            return sorted(free_snaffles, key=lambda snaffle: snaffle.position.distance_with(wizard_position))[0]
        else:
            return None

    def get_bludgers(self):
        return [entity for entity in self.entities if entity.type == "BLUDGER"]

    def get_closest_enemy(self, wizard_position):
        enemies = self.get_wizards(self.enemy_team.id)
        return sorted(enemies, key=lambda enemy_wizard: enemy_wizard.position.distance_with(wizard_position))[0]

    def play(self):
        orders = []
        my_wizards = self.get_wizards(self.my_team.id)
        bludgers = self.get_bludgers()

        for wizard in my_wizards:
            # if wizard.state == 0:
            #     can_attack_bludgers = [bludger for bludger in bludgers if bludger.state != wizard.id]
            #     closest_bludgers = sorted(can_attack_bludgers, key=lambda bludger: bludger.position.distance_with(wizard.position))
            #
            #     if len(closest_bludgers) != 0 and closest_bludgers[0].position.distance_with(wizard.position) <= 1000:
            #         orders.append("PETRIFICUS {}".format(closest_bludgers[0].id))

            # wizard has no snaffle
            if wizard.state == 0:
                target = self.get_closest_snaffle(wizard.position)
                if target is not None:
                    if self.my_team.magic >= 15:
                        order = "ACCIO {}".format(target.id)
                    else:
                        order = "MOVE {} {} 150".format(target.position.x, target.position.y)
                    orders.append(order)
                else:
                    target = self.get_closest_enemy(wizard.position)
                    order = "MOVE {} {} 150".format(target.position.x, target.position.y)
                    orders.append(order)
            else:
                goal_position = self.get_enemy_goal(self.my_team.id)

                target_position = goal_position

                order = "THROW {} {} 500".format(target_position.x, target_position.y)
                orders.append(order)

        return orders[0:2]


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

    order1, order2 = game.play()

    print(order1)
    print(order2)
