from random import shuffle, choice
from collections import Counter
from itertools import permutations
from multiprocessing import Pool, freeze_support
from cProfile import run


class Solve:

    def __init__(self):
        self.valid_scrabble_words = {word.strip() for word in open('enable1.txt', 'r')}
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
        self.letter_scores = {'?': 0,
                              'e': 1, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'r': 1, 't': 1, 'l': 1, 's': 1, 'u': 1,
                              'd': 2, 'g': 2,
                              'b': 3, 'c': 3, 'm': 3, 'p': 3,
                              'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                              'k': 5,
                              'j': 8, 'x': 8,
                              'q': 10, 'z': 10}
        self.word_scores = {word: self.string_score(word) for word in self.valid_scrabble_words}

    def string_score(self, solution):
        """solution is a string that is worth points
        returns the point value of the string"""
        return sum(self.letter_scores[letter] for word in self.valid_scrabble_words for letter in word if
                   word in solution)  # TODO: word in solution must be modified to account for wildcards

    def evaluate_part(self, candidate_tiles):
        """candidate_tiles is a tuple of 1 character strings which form a word when concatenated
        returns a tuple where the first item is candidate_tiles, and the second item is the point-value
        of the string that candidate_tiles represent"""
        return candidate_tiles, self.word_scores[self.test_solution + "".join(candidate_tiles)]

    def make_solution_method_1(self):
        """returns a string that is worth as many points as possible"""

        def part_value(part):
            return part[1]

        def get_part(part):
            return part[0]

        with Pool(8) as p:
            while self.scrabble_tiles:

                possible_part_list = p.map(self.evaluate_part, set(permutations(self.scrabble_tiles, r=2)))
                best_part = max(possible_part_list, key=part_value)

                print(best_part)
                self.test_solution += "".join(get_part(best_part))
                for tile in get_part(best_part):
                    self.scrabble_tiles.remove(tile)
                print(self.test_solution)
        return self.test_solution

    def get_feasible_parts(
            self):  # TODO: update get_feasible_parts so that it precomputes a list of possible words in an manner organized such that it is easy to eliminate parts that are no longer feasible when certain letters are no longer available
        """returns a set of tuples of 1 character strings which form a valid scrabble word when concatenated
        that can be made from the current set of tiles left"""
        current_tile_count = Counter(self.scrabble_tiles)
        return {tuple(word) for word in self.valid_scrabble_words if
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
    solver = Solve()
    run('solution = solver.make_solution_method_2()', sort='cumulative')

    print(solver.string_score(solution))
    print(solution)
    print(len(solution))  # our solution is the right length...
    print(Counter(solution))
    print(Counter(solution) == solver.scrabble_tile_frequencies)  # ... with the right letters

# TODO: profile method 2 and possible update it to search through combinations of two valid scrabble words at a time
# best so far carboxymethylcellulosesforeshadowerspreformattingreawakenednonunionizedequipagedagobavatutiti
