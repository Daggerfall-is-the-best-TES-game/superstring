from random import shuffle, choice
from collections import Counter
from itertools import permutations, product
from multiprocessing import Pool, freeze_support
from cProfile import run
from pickle import dump, load, HIGHEST_PROTOCOL
from os.path import isfile
from dawg import DAWG
from collections import defaultdict


class Solve:

    def __init__(self):
        with open('enable1.txt', 'r') as file:
            self.valid_scrabble_words = {str(string[:x].lower() + string[x:].capitalize())[:y]
                                         + str(string[:x].lower() + string[x:].capitalize())[y:].capitalize()
                                         for string in {word.strip() for word in file}
                                         for x in range(len(string)) for y in range(x, len(string))}
            self.valid_scrabble_words |= {word.strip() for word in file}

        self.scrabble_tile_frequencies = {'?': 2,
                                          'e': 12, 'a': 9, 'i': 9, 'o': 8, 'n': 6, 'r': 6, 't': 6, 'l': 4, 's': 4,
                                          'u': 4,
                                          'd': 4, 'g': 3,
                                          'b': 2, 'c': 2, 'm': 2, 'p': 2,
                                          'f': 2, 'h': 2, 'v': 2, 'w': 2, 'y': 2,
                                          'k': 1,
                                          'j': 1, 'x': 1,
                                          'q': 1, 'z': 1}
        self.scrabble_tiles = [tile for tile in self.scrabble_tile_frequencies for x in
                               range(self.scrabble_tile_frequencies[tile])]
        self.test_solution = ""
        #  wildcard tiles, which are represented by uppercase letters, will default to a value of 0
        self.letter_scores = defaultdict(int, {'e': 1, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'r': 1, 't': 1, 'l': 1, 's': 1,
                                               'u': 1,
                                               'd': 2, 'g': 2,
                                               'b': 3, 'c': 3, 'm': 3, 'p': 3,
                                               'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                                               'k': 5,
                                               'j': 8, 'x': 8,
                                               'q': 10, 'z': 10})

        if not isfile("word scores.pkl"):
            with Pool(8) as p:
                self.word_scores = dict(
                    zip(self.valid_scrabble_words, p.map(self.string_score_2, self.valid_scrabble_words)))
            with open("word scores.pkl", 'wb') as file:
                dump(self.word_scores, file, HIGHEST_PROTOCOL)
        else:
            with open("word scores.pkl", 'rb') as file:
                self.word_scores = load(file)

        self.word_graph = DAWG(self.valid_scrabble_words)

    def string_score(self, solution):
        """solution is a string that is worth points
        returns the point value of the string including subwords"""

        return sum(self.word_scores[word] for word in
                   self.words_in_string(solution))  # TODO: word in solution must be modified to account for wildcards

    def string_score_2(self, solution):
        """solution is a string that is worth points
        returns the point value of the string NOT including subwords"""
        return sum(self.letter_scores[letter] for letter in solution)

    def words_in_string(self, string):
        return {word for x in range(len(string)) for word in self.word_graph.prefixes(string[x:])}

    def evaluate_part(self, candidate_tiles):
        """candidate_tiles is a tuple of 1 character strings which form a word when concatenated
        returns a tuple where the first item is candidate_tiles, and the second item is the point-value
        of the string that candidate_tiles represent"""
        return candidate_tiles, self.string_score(self.test_solution + "".join(candidate_tiles))

    def make_solution_method_1(self):
        """returns a string that is worth as many points as possible"""

        def part_value(part):
            return part[1]

        def get_part(part):
            return part[0]

        with Pool(32) as p:
            while self.scrabble_tiles:

                possible_part_list = p.map(self.evaluate_part, set(permutations(self.scrabble_tiles, r=4)))
                best_part = max(possible_part_list, key=part_value)

                print(best_part)
                self.test_solution += "".join(get_part(best_part))
                for tile in get_part(best_part):
                    self.scrabble_tiles.remove(tile)
                print(self.test_solution)
        return self.test_solution

    def get_feasible_parts(
            self):  # TODO: update get_feasible_parts to use a DAWG as well
        """returns a set of tuples of 1 character strings which form a valid scrabble word when concatenated
        that can be made from the current set of tiles left"""
        current_tile_count = Counter(self.scrabble_tiles)
        return {word for word in self.valid_scrabble_words if
                all(current_tile_count[letter] >= Counter(word)[letter] for letter in word)}

    def make_solution_method_2(self):
        """returns a string that is worth as many points as possible"""

        def part_value(part):
            return part[1]

        def get_part(part):
            return part[0]

        with Pool(8) as p:
            while self.scrabble_tiles:
                possible_part_list = p.map(self.evaluate_part, self.get_feasible_parts())
                if possible_part_list:
                    best_part = max(possible_part_list, key=part_value)
                    print(best_part)
                    self.test_solution += "".join(get_part(best_part))
                    for tile in get_part(best_part):
                        self.scrabble_tiles.remove(tile)
                    print(self.test_solution)
                else:
                    break
        return self.test_solution


if __name__ == '__main__':
    freeze_support()
    run('solver = Solve()', sort='cumulative')

    # run('solution = solver.make_solution_method_1()', sort='cumulative')
    # print(solver.string_score(solution))
    # print(solution)
    # print(len(solution))  # our solution is the right length...
    # print(Counter(solution))
    # print(Counter(solution) == solver.scrabble_tile_frequencies)  # ... with the right letters

    # string = "hello"
    # print([str(string[:x].lower() + string[x:].capitalize())[:y] + str(string[:x].lower() + string[x:].capitalize())[y:].capitalize() for x in range(len(string)) for y in range(x, len(string))])

# TODO: profile method 2 and possible update it to search through combinations of two valid scrabble words at a time
# best so far forethoughtfulnessescodevelopersdecarboxylatedoverelaboratedouttrumpingawakeningamainzayin
