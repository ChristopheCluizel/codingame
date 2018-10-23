import sys
import math
import statistics
import copy


class Game:
    def __init__(self, number_of_participants, gift_price, budgets):
        self.number_of_participants = number_of_participants
        self.gift_price = gift_price
        self.budgets = budgets

    def __str__(self):
        return "nb participants: {}\ngift price: {}\nbudgets: {}".format(self.number_of_participants,
                                                                         self.gift_price,
                                                                         self.budgets)

    def print_debug(self, message):
        print(message, file=sys.stderr)

    def play(self):
        gifts = []
        virtual_price = self.gift_price
        sorted_budgets = sorted(self.budgets)
        remaining_budgets = copy.deepcopy(sorted_budgets)

        for budget in sorted_budgets:
            mean = int(virtual_price / len(remaining_budgets))
            if mean <= budget and virtual_price - mean >= 0:
                gifts.append(mean)
                virtual_price -= mean
                remaining_budgets.pop(0)
            elif mean > budget and virtual_price - budget >= 0:
                gifts.append(budget)
                virtual_price -= budget
                remaining_budgets.pop(0)
            else:
                gifts.append(virtual_price)
                virtual_price -= virtual_price
                remaining_budgets.pop(0)

        if virtual_price == 0:
            return sorted(gifts)
        else:
            return "IMPOSSIBLE"


def my_main():
    number_of_participants = int(input())
    gift_price = int(input())
    budgets = []
    for i in range(number_of_participants):
        b = int(input())
        budgets.append(b)
    game = Game(number_of_participants, gift_price, budgets)

    res = game.play()

    if res == "IMPOSSIBLE":
        print(res)
    else:
        print("\n".join([str(item) for item in res]))


if __name__ == '__main__':
    my_main()
