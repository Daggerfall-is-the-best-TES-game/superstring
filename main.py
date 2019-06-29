from random import shuffle, choice
from itertools import permutations
from multiprocessing import Pool, freeze_support


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

    def string_score(self, solution):
        def score(word):
            letter_scores = {'?': 0,
                             'e': 1, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'r': 1, 't': 1, 'l': 1, 's': 1, 'u': 1,
                             'd': 2, 'g': 2,
                             'b': 3, 'c': 3, 'm': 3, 'p': 3,
                             'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                             'k': 5,
                             'j': 8, 'x': 8,
                             'q': 10, 'z': 10}
            return sum(letter_scores[letter] for letter in word)

        return sum(score(word) for word in self.valid_scrabble_words if
                   word in solution)  # TODO: word in solution must be modified to account for wildcards

    def evaluate_part(self, candidate_tiles):
        return candidate_tiles, self.string_score(self.test_solution + "".join(candidate_tiles))

    def make_solution(self):
        if __name__ == '__main__':
            freeze_support()

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


if __name__ == '__main__':
    freeze_support()
    solver = Solve()
    solution = solver.make_solution()

    print(solver.string_score(solution))
    print(solution)
    print(len(solution))
