import sys
import copy


class Game:
    def __init__(self, dictionary, letters):
        self.dictionary = dictionary
        self.letters = letters

    def __str__(self):
        return "letters: {}\n{}".format(self.letters, self.dictionary)

    def print_debug(self, message):
        print(message, file=sys.stderr)

    def create_word_with_letters(self, word):
        letters = copy.deepcopy(self.letters)
        letters_bis = copy.deepcopy(letters)
        word_bis = copy.deepcopy(word)
        word_size = len(word)

        res = []

        for i in range(len(word)):
            letters = copy.deepcopy(letters_bis)
            for index, letter in enumerate(letters):
                word = copy.deepcopy(word_bis)
                if letter in word:
                    res.append(letter)
                    letters_bis = letters_bis.replace(letter, '', 1)
                    word_bis = word_bis.replace(letter, '', 1)
        return len(res) == word_size

    def play(self):
        res = {}
        for word, point in self.dictionary.items():
            if self.create_word_with_letters(word):
                res[word] = point

        final_res = sorted(res.items(), key=lambda x: x[1], reverse=True)
        return final_res[0][0]


def word_point(word):
    points = {
        "eaionrtslsu": 1,
        "dg": 2,
        "bcmp": 3,
        "fhvwy": 4,
        "k": 5,
        "jx": 8,
        "qz": 10
    }

    value = 0

    for letter in word:
        for letter_suite, point in points.items():
            if letter in letter_suite:
                value += point
    return value


def my_main():
    dictionary_length = int(input())
    dictionary = {}
    for i in range(dictionary_length):
        word = input()
        point = word_point(word)
        dictionary[word] = point
    letters = input()
    game = Game(dictionary, letters)

    res = game.play()

    print(res)


if __name__ == '__main__':
    my_main()
