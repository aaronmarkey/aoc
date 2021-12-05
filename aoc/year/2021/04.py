"""
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?

--- Part Two ---

On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?

"""
import operator
from typing import Callable, Optional, Tuple

from aoc import utils


class BingoBoard:
    def __init__(self, values: Tuple[int], size: int) -> None:
        self.values = values
        self.size = size

        self._row_hits = [0 for _ in range(self.size)]
        self._col_hits = [0 for _ in range(self.size)]
        self._marked_values = []
        self.attempts = 0
        self._is_winner = False
        self._winning_rows = []
        self._winning_cols = []

    @property
    def is_winner(self) -> bool:
        return self._is_winner

    @property
    def winning_numbers(self) -> Optional[Tuple[Tuple[int, ...], ...]]:
        if not self._is_winner:
            return None

        winning_numbers = []
        for row_index in self._winning_rows:
            row_start = row_index * self.size
            row_end = row_start + self.size
            winning_numbers.append(self.values[row_start:row_end])
        for col_index in self._winning_cols:
            numbers = []
            for row_index in range(self.size):
                value_index = row_index * self.size + col_index
                numbers.append(self.values[value_index])
                winning_numbers.append(tuple(numbers))
        return tuple(winning_numbers)

    @property
    def marked_numbers(self) -> Tuple[int]:
        return tuple(self._marked_values)

    def mark(self, value: int) -> None:
        try:
            position = self.values.index(value)
            row = int(position / self.size)
            col = position % self.size
            self._row_hits[row] += 1
            self._col_hits[col] += 1
            self._marked_values.append(value)

            if self._row_hits[row] >= self.size:
                self._is_winner = True
                self._winning_rows.append(row)
            if self._col_hits[col] >= self.size:
                self._is_winner = True
                self._winning_cols.append(col)
        except ValueError:
            pass
        self.attempts += 1


class BingoGame:
    def __init__(self, guesses: Tuple[int]) -> None:
        self.guesses = guesses

    def check_bingo_board(self, board: BingoBoard) -> Tuple[bool, int]:
        for guess in self.guesses:
            board.mark(guess)
            if board.is_winner:
                return True, guess
        return False, -1


def parser(filename: str) -> Tuple[Tuple[int], Tuple[Tuple[int], ...]]:
    guesses = None
    boards = []
    current_board = []
    for line in utils.read_lines(filename, True):
        if guesses is None:
            guesses = tuple(int(value) for value in line.split(","))
            continue
        if line:
            current_board.extend([int(value) for value in line.split()])
        elif not line and current_board:
            boards.append(tuple(board for board in current_board))
            current_board = []
    boards.append(tuple(board for board in current_board))

    return guesses, tuple(boards)


def determine_winning_score(filename: str, op: Callable) -> int:
    g, bs = parser(filename)
    bg = BingoGame(g)

    best_board = None
    winning_value = None

    for b in bs:
        board = BingoBoard(b, 5)
        is_winner, winning_guess = bg.check_bingo_board(board)
        if is_winner:
            if best_board is None or op(board.attempts, best_board.attempts):
                best_board = board
                winning_value = winning_guess

    return (sum(best_board.values) - sum(best_board.marked_numbers)) * winning_value


if __name__ == "__main__":
    test_filename = "2021/04-test.txt"
    filename = "2021/04.txt"

    print(determine_winning_score(test_filename, operator.lt))
    print(determine_winning_score(filename, operator.lt))
    print("---")
    print(determine_winning_score(test_filename, operator.gt))
    print(determine_winning_score(filename, operator.gt))
