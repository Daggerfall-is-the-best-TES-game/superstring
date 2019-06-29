from random import sample


valid_scrabble_words = {word.strip() for word in open('enable1.txt', 'r')}
scrabble_tile_frequencies = {'?': 2,
                             'e': 12, 'a': 9, 'i': 9, 'o': 8, 'n': 6, 'r': 6, 't': 6, 'l': 4, 's': 4, 'u': 4,
                             'd': 4, 'g': 3,
                             'b': 2, 'c': 2, 'm': 2, 'p': 2,
                             'f': 2, 'h': 2, 'v': 2, 'w': 2, 'y': 2,
                             'k': 1,
                             'j': 1, 'x': 1,
                             'q': 1, 'z': 1}
scrabble_tiles = [tile for tile in scrabble_tile_frequencies for x in range(scrabble_tile_frequencies[tile])]


def string_score(solution):
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

    return sum(score(word) for word in valid_scrabble_words if word in solution)  #TODO: word in solution must be modified to account for wildcards


test_solution = ""
while scrabble_tiles:
    best_tile = scrabble_tiles[0]
    for tile in set(scrabble_tiles):
        new_solution = test_solution + tile
        if string_score(new_solution) > string_score(test_solution):
            best_tile = tile
    test_solution += best_tile
    scrabble_tiles.remove(best_tile)
    print(test_solution)


print(string_score(test_solution))