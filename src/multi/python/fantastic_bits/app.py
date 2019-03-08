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

    def get_goal(self, side):
        if side == "LEFT":
            return self.left_goal
        else:
            return self.right_goal


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

    def get_enemy_goal_center_position(self, my_team_id):
        if my_team_id == 0:
            return map.goals.get_center("RIGHT")
        else:
            return map.goals.get_center("LEFT")

    def get_enemy_goal(self, my_team_id):
        if my_team_id == 0:
            return map.goals.get_goal("RIGHT")
        else:
            return map.goals.get_goal("LEFT")

    def get_closest_snaffles(self, wizard_position):
        """

        :param wizard_position:
        :type wizard_position: Position
        :return:
        :rtype: list(Snaffle)
        """
        free_snaffles = [Snaffle(entity.id, entity.position, entity.speed, entity.state) for entity in self.entities if entity.type == "SNAFFLE" and entity.state == 0]
        if len(free_snaffles) != 0:
            return sorted(free_snaffles, key=lambda snaffle: snaffle.position.distance_with(wizard_position))
        else:
            return []

    def get_bludgers(self):
        return [entity for entity in self.entities if entity.type == "BLUDGER"]

    def get_closest_enemy(self, wizard_position):
        enemies = self.get_wizards(self.enemy_team.id)
        return sorted(enemies, key=lambda enemy_wizard: enemy_wizard.position.distance_with(wizard_position))[0]

    def is_snaffle_behind(self, wizard_position, snaffle_position):
        if self.my_team.id == 0:
            return wizard_position.x > snaffle_position.x
        elif self.my_team.id == 1:
            return wizard_position.x < snaffle_position.x

    def can_wizard_shoot(self, wizard_position, snaffle):
        pole_radius = 300
        snaffle_position = snaffle.position
        x_a = wizard_position.x
        y_a = wizard_position.y
        x_b = snaffle_position.x
        y_b = snaffle_position.y
        x_goal = self.get_enemy_goal(self.my_team.id)[0].position.x
        y_goal = [self.get_enemy_goal(self.my_team.id)[0].position.y, self.get_enemy_goal(self.my_team.id)[1].position.y]

        div = (x_b - x_a)
        if div == 0:
            div = 1
        y = ((y_b - y_a) / div) * (x_goal - x_a) + y_a

        # printd("target shoot position: {}, goal y: {}".format(str(Position(x_goal, y)), y_goal))
        # printd("can shoot {}: {}".format(snaffle.id, (y_goal[0] <= y <= y_goal[1])))

        return y_goal[0] + pole_radius <= y <= y_goal[1] - pole_radius

    def no_entity_behind_snaffle(self, current_entity):
        if self.my_team.id == 0:
            return len([entity for entity in self.entities if entity.position.x > current_entity.position.x]) == 0
        elif self.my_team.id == 1:
            return len([entity for entity in self.entities if entity.position.x < current_entity.position.x]) == 0

    def play(self):
        orders = []
        my_wizards = self.get_wizards(self.my_team.id)

        snaffle_id_already_targeted = 1000

        for wizard in my_wizards:
            # wizard has no snaffle
            if wizard.state == 0:
                targets = self.get_closest_snaffles(wizard.position)

                snaffles_which_can_be_shot = [snaffle for snaffle in targets if self.can_wizard_shoot(wizard.position, snaffle)
                                              and self.no_entity_behind_snaffle(snaffle)]
                # check if snaffle can be shot with flipendo spell
                if len(snaffles_which_can_be_shot) > 0 and self.my_team.magic >= 20:
                    target_id = snaffles_which_can_be_shot[0].id
                    order = "FLIPENDO {}".format(target_id)
                    orders.append(order)
                else:
                    if len(targets) >= 1:
                        # handle different targets if more than 2 snaffles
                        if len(targets) >= 2:
                            if targets[0].id != snaffle_id_already_targeted:
                                target = targets[0]
                            else:
                                target = targets[1]
                            snaffle_id_already_targeted = target.id
                        else:
                            target = targets[0]
                            snaffle_id_already_targeted = 1000

                        behind_snaffles = [(snaffle, wizard.position.distance_with(snaffle.position)) for snaffle in targets if self.is_snaffle_behind(wizard.position, snaffle.position)]
                        closest_behind_snaffles = [snaffle_tuple[0] for snaffle_tuple in sorted(behind_snaffles, key=lambda tuple: tuple[1]) if snaffle_tuple[1] <= 4000]
                        # grab behind snaffles
                        if (self.my_team.magic >= 15 or len(targets) <= 1) and len(closest_behind_snaffles) > 0:
                            target = closest_behind_snaffles[0]
                            order = "ACCIO {}".format(target.id)
                        else:
                            order = "MOVE {} {} 150".format(target.position.x, target.position.y)
                        orders.append(order)
                    else:
                        target = self.get_closest_enemy(wizard.position)
                        order = "MOVE {} {} 150".format(target.position.x, target.position.y)
                        orders.append(order)
            else:
                goal_position = self.get_enemy_goal_center_position(self.my_team.id)

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

    # printd(game)

    order1, order2 = game.play()

    print(order1)
    print(order2)
