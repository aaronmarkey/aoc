"""
--- Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

	An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
	An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

--- Part Two ---

Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

    An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.

Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....

You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?

"""
import os
from collections import defaultdict
from typing import Generator, Tuple

from aoc import utils


def parse(filename: str) -> Generator[Tuple[Tuple[int, int], Tuple[int, int]], None, None]:
    for line in utils.read_lines(filename, True):
        start, end = [point.strip() for point in line.split("->")]
        yield tuple([tuple(int(value) for value in start.split(",")), tuple(int(value) for value in end.split(","))])


class HydrothermalMap:
    def __init__(self) -> None:
        self._vent_map = defaultdict(int)
        self.size_x = 0
        self.size_y = 0

    @property
    def size(self) -> Tuple[int, int]:
        return self.size_x, self.size_y

    def _update_size(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        xs = sorted([start[0], end[0]])
        if xs[-1] + 1 > self.size_x:
            self.size_x = xs[-1] + 1
        ys = sorted([start[1], end[1]])
        if ys[-1] + 1 > self.size_y:
            self.size_y = ys[-1] + 1

    def add_line(self, start: Tuple[int, int], end: Tuple[int, int], *, allow_diagonals: bool) -> None:
        points = []
        if start[0] == end[0]:
            sv, ev = sorted([start[1], end[1]])
            points = [(start[0], y) for y in range(sv, ev + 1)]
        elif start[1] == end[1]:
            sv, ev = sorted([start[0], end[0]])
            points = [(x, start[1]) for x in range(sv, ev + 1)]
        elif allow_diagonals:
            points.append(start)
            current_x, current_y = start
            move = True
            while move:
                if start[0] > end[0]:
                    current_x -= 1
                else:
                    current_x += 1
                if start[1] < end[1]:
                    current_y += 1
                else:
                    current_y -= 1
                current_point = (current_x, current_y)
                points.append(current_point)
                if current_point == end:
                    move = False

        for point in points:
            self._vent_map[point] += 1
        self._update_size(start, end)

    def number_of_dangerous_spots_for_threshold(self, threshold: int) -> int:
        return len(list(filter(lambda x: x >= threshold, self._vent_map.values())))

    def __str__(self) -> str:
        blank_spot = "."
        value = ""
        for y in range(self.size_y):
            for x in range(self.size_x):
                value += str(self._vent_map.get((x, y), blank_spot))
            value += os.linesep
        return value


if __name__ == "__main__":
    test_filename = "2021/05-test.txt"
    filename = "2021/05.txt"
    danger_threshold = 2

    test_map = HydrothermalMap()
    for value in parse(test_filename):
        test_map.add_line(value[0], value[1], allow_diagonals=False)
    print(test_map.number_of_dangerous_spots_for_threshold(danger_threshold))
    print(test_map)

    test_map2 = HydrothermalMap()
    for value in parse(test_filename):
        test_map2.add_line(value[0], value[1], allow_diagonals=True)
    print(test_map2.number_of_dangerous_spots_for_threshold(danger_threshold))
    print(test_map2)

    real_map = HydrothermalMap()
    for value in parse(filename):
        real_map.add_line(value[0], value[1], allow_diagonals=False)
    print(real_map.number_of_dangerous_spots_for_threshold(danger_threshold))

    real_map2 = HydrothermalMap()
    for value in parse(filename):
        real_map2.add_line(value[0], value[1], allow_diagonals=True)
    print(real_map2.number_of_dangerous_spots_for_threshold(danger_threshold))
