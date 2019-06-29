

def string_score(solution):
    def score(word):
        letter_scores = {'e': 1, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'r': 1, 't': 1, 'l': 1, 's': 1, 'u': 1,
                         'd': 2, 'g': 2,
                         'b': 3, 'c': 3, 'm': 3, 'p': 3,
                         'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                         'k': 5,
                         'j': 8, 'x': 8,
                         'q': 10, 'z': 10}
        return sum(letter_scores[letter] for letter in word)

    with open('enable1.txt', 'r') as valid_words:
        return sum(score(valid_word.strip()) for valid_word in valid_words if valid_word.strip() in solution)


print(string_score("aa"))

