"""
--- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.

Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go to open it, page 1 falls out. It's a large sheet of transparent paper! The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input). For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following pattern, where # is a dot on the paper and . is an empty, unmarked position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper and wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines). In this example, the first fold instruction is fold along y=7, which designates the line formed by all of the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping after the fold is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be seen through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....

Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the first fold. After the first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on your transparent paper?

--- Part Two ---

Finish folding the transparent paper according to the instructions. The manual says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?
"""
from collections import defaultdict
from aoc import utils


class Origami:
    def __init__(self, filename: str) -> None:
        self.width = 0
        self.height = 0

        self._by_row = defaultdict(set)
        self._by_col = defaultdict(set)
        self._instructions = []

        for line in utils.read_lines(filename, True):
            if line:
                parts = line.split(",")
                if len(parts) == 2:
                    x, y = int(parts[0]), int(parts[1])
                    if x + 1 > self.width:
                        self.width = x + 1
                    if y + 1 > self.height:
                        self.height = y + 1
                    self._by_row[y].add(x)
                    self._by_col[x].add(y)
                else:
                    parts = line.split("=")
                    self._instructions.append((parts[0].split(" ")[-1], int(parts[1])))

    def _fold(self, by_row, by_col, instruction_index, fold_count):
        if instruction_index >= len(self._instructions) or fold_count == 0:
            return by_row

        instruction = self._instructions[instruction_index]
        direction = instruction[0]
        fold_index = instruction[1]

        new_matrix = defaultdict(set)
        if direction == "y":
            for i in range(fold_index):
                above = fold_index - i - 1
                below = fold_index + i + 1
                new_row = by_row.get(above, set()).union(by_row.get(below, set()))
                new_matrix[above] = new_row
        else:
            for i in range(fold_index):
                left = fold_index - i - 1
                right = fold_index + i + 1
                new_col = by_col.get(left, set()).union(by_col.get(right, set()))
                new_matrix[left] = new_col

        reverse_matrix = defaultdict(set)
        for key, values in new_matrix.items():
            for value in values:
                reverse_matrix[value].add(key)

        if direction == "y":
            return self._fold(new_matrix, reverse_matrix, instruction_index + 1, fold_count - 1)
        return self._fold(reverse_matrix, new_matrix, instruction_index + 1, fold_count - 1)

    def fold(self, fold_count: int) -> dict:
        return self._fold(self._by_row, self._by_col, 0, fold_count)


def visible_dots_one_fold(filename: str) -> None:
    origami = Origami(filename)
    folded = origami.fold(1)

    count = 0
    for points in folded.values():
        count += len(points)
    print(count)


def get_code(filename: str) -> None:
    origami = Origami(filename)
    folded = origami.fold(-1)

    height = max(folded.keys()) + 1
    for row in range(height):
        line = ""
        width = max(folded[row]) + 1
        for col in range(width):
            line += "#" if col in folded[row] else "."
        print(line)


if __name__ == "__main__":
    test_filename = "2021/13-test.txt"
    filename = "2021/13.txt"

    visible_dots_one_fold(test_filename)
    get_code(test_filename)

    visible_dots_one_fold(filename)
    get_code(filename)
