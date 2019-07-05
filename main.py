from random import shuffle, choice, randrange
from collections import Counter
from itertools import permutations, chain
from multiprocessing import Pool, freeze_support
from cProfile import run
from pickle import dump, load, HIGHEST_PROTOCOL
from os.path import isfile
from dawg import DAWG
from collections import defaultdict
from heapq import nlargest


class Solve:

    def __init__(self):
        with open('enable1.txt', 'r') as file:
            self.valid_scrabble_words = set()  # could use chain.from_iterable here when we start using wildcards again
            for string in file:
                # self.valid_scrabble_words |= self.wildcard_it(string.strip())
                self.valid_scrabble_words.add(string.strip())

        self.scrabble_tile_frequencies = {'e': 12, 'a': 9, 'i': 9, 'o': 8, 'n': 6, 'r': 6, 't': 6, 'l': 4, 's': 4,
                                          'u': 4,
                                          'd': 4, 'g': 3,
                                          'b': 2, 'c': 2, 'm': 2, 'p': 2,
                                          'f': 2, 'h': 2, 'v': 2, 'w': 2, 'y': 2,
                                          'k': 1,
                                          'j': 1, 'x': 1,
                                          'q': 1, 'z': 1}
        # dummy tiles representing wildcards
        self.scrabble_tile_frequencies.update(dict.fromkeys("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 2))
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

        if not isfile('word graph.dawg'):
            self.word_graph = DAWG(self.valid_scrabble_words)
            self.word_graph.save('word graph.dawg')
        else:
            self.word_graph = DAWG().load('word graph.dawg')

    def wildcard_it(self, string):
        return {str(string[:x].lower() + string[x:].capitalize())[:y]
                + str(string[:x].lower() + string[x:].capitalize())[y:].capitalize() for x in range(len(string)) for y
                in range(x, len(string))}

    def string_score(self, solution):
        """solution is a string that is worth points
        returns the point value of the string including subwords"""

        return sum(self.word_scores[word] for word in
                   self.words_in_string(solution))

    def string_score_2(self, solution):
        """solution is a string that is worth points
        returns the point value of the string NOT including subwords"""
        return sum(self.letter_scores[letter] for letter in solution)

    def words_in_string(self, string):
        return {word for x in range(len(string)) for word in self.word_graph.prefixes(string[x:])}

    def evaluate_part(self, candidate_tiles):
        """candidate_tiles is a string
        returns a point-value
        of the string that candidate_tiles represent"""
        return self.string_score(self.test_solution + candidate_tiles)

    def make_solution_method_1(self):
        """returns a string that is worth as many points as possible"""

        def part_value(part):
            return part[1]

        def get_part(part):
            return part[0]

        with Pool(32) as p:
            while self.scrabble_tiles:

                possible_part_list = p.map(self.evaluate_part, set(permutations(self.scrabble_tiles,
                                                                                r=4)))  # doesn't work with wildcard tiles represented by dummy tiles
                best_part = max(possible_part_list, key=part_value)

                print(best_part)
                self.test_solution += "".join(get_part(best_part))
                for tile in get_part(best_part):
                    self.scrabble_tiles.remove(tile)
                print(self.test_solution)
        return self.test_solution

    def add_to_solution(self, part):
        self.test_solution += part
        for tile in part:  # remove used tiles from bag of scrabble tiles
            if tile.isupper():
                for owned_tile in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    self.scrabble_tiles.remove(owned_tile)
            else:
                self.scrabble_tiles.remove(tile)

    def generate_word_combinations(self, words, max_length):
        """words is a list of words. max_length is a positive integer
        returns a generator of strings composed of permutations of words
        for each length up to the length specified by maxlength"""
        return ("".join(word_tuple) for word_tuple in
                chain.from_iterable(permutations(words, r=length) for length in range(1, max_length + 1)))

    def get_feasible_parts(self, word_list):  # TODO: update get_feasible_parts to use a DAWG as well
        """returns the set of strings that can be made from the current set of tiles left"""
        current_tile_count = Counter(self.scrabble_tiles)
        return (words for words in word_list if
                all(current_tile_count[letter] >= Counter(words)[letter] for letter in words))

    def make_solution_method_2(self):
        """returns a string that is worth as many points as possible"""

        while self.scrabble_tiles:
            possible_part_list = self.get_feasible_parts(self.valid_scrabble_words)
            best_parts = nlargest(100, possible_part_list, self.evaluate_part)  # get top n words
            if best_parts:
                best_part = max(self.get_feasible_parts(self.generate_word_combinations(best_parts, 2)),
                                key=self.evaluate_part)
                self.add_to_solution(best_part)
                print(self.test_solution)
                print(self.string_score(self.test_solution))
            else:
                break

        return self.test_solution



if __name__ == '__main__':
    freeze_support()
    solver = Solve()

    best = "CAnondenominationalismspsychopathologicallyreawakeneddeoxidizersquarteragereviewerbuffobijugatetui"
    # run('solution = solver.make_solution_method_2()', sort='cumulative')
    # print(f"score is {solver.string_score(solution)}")
    # print(solution)
    # print(f"length of solution:{len(solution)}")  # our solution is the right length...
    # print(Counter(solution))
    # print(Counter(solution) == solver.scrabble_tile_frequencies)  # ... with the right letters
    # print(f"There is a new best? {solver.string_score(solution) > solver.string_score(best)}")
    print(solver.string_score(best))

# TODO: profile method 2 and possible update it to search through combinations of two valid scrabble words at a time
# best so far nondenominationalismspsychopathologicallyreawakeneddeoxidizersquarteragereviewerbuffobijugatetui

# psychopathologicallynondenominationalismsdeoxidizersreawakenedquarteragereviewerbuffobijugateutit
# best with wildcards added manually CAnondenominationalismspsychopathologicallyreawakeneddeoxidizersquarteragereviewerbuffobijugatetui
