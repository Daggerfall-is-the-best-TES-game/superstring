## Goal of The project
In short, the aim was to find the highest scoring scrabble string that can be made from the given set of 100 tiles in scrabble.
The details regarding the specific rules of the challenge are given in [this 538 Riddler column.](https://web.archive.org/web/20190629142859/https://fivethirtyeight.com/features/whats-your-best-scrabble-string/)
## Algorithm
I believe this problem is a type of [knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem). As such, it is difficult to find the absolute optimal solution, so an approximate one might be satisfactory. The program works as follows:

* It precomputes the value of every word in the scrabble dictionary and saves this to a file. This saves a lot of time on future runs.
* It stores every word in the scrabble dictionary in a [DAWG](https://en.wikipedia.org/wiki/Deterministic_acyclic_finite_state_automaton). This is a very efficient data structure that allows the program to quickly find all of the sub-words within a given word, which is essential for scoring scrabble strings.
* Then the program goes into a loop where it:
    1. calculates the list of scrabble words that can be made with the tiles remaining
    2. makes a list of the top N words based on their point values when added to the solution string being made, where N is a number that decreases as the program builds up the solution string
    3. picks a random permutation of 2 words from that list and adds them to the solution
    4. The loop iteration ends when no more words can be made with the remaining tiles
## Results
The program found the string forethoughtfulnessesdecarboxylationsprepackagedimmaterializedoverelaboratedjinniavowingyowequint,
which is worth 1373 points. With some hand optimization, the word can be extended with the two wildcard tiles and an unused letter 'i' to form 
AforethoughtfulnessesdecarboxylationsprepackagedimmaterializedoverelaboratedjinniavowingyowequintiN, where the capital letters represent
the wildcard tiles. This string is worth 1423 points. This is not necessarily the optimal use of wildcards, even for this particular word, but it was good enough for me. 