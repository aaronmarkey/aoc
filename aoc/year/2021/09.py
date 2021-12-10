"""
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?

--- Part Two ---

Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678

The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678

The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?

"""
from enum import Enum
from functools import reduce
from math import sqrt
from typing import List, Tuple

from aoc import utils


def parse(filename: str) -> Tuple[List[int], int]:
    values = []
    width = -1
    for line in utils.read_lines(filename, True):
        values.extend([int(value) for value in line])
        width = len(line)
    return values, width


class Direction(Enum):
    left = 1
    right = 2
    up = 3
    down = 4


class VentMap:
    def __init__(self, vent_map: List[int], width: int) -> None:
        self.vent_map = vent_map
        self._width = width
        self._height = int(len(vent_map) / width)

        self._left_indexes = [self._width * row for row in range(self._height)]
        self._right_indexes = [index + self._width - 1 for index in self._left_indexes]

        self._low_points = self._calculate_low_points()

    @property
    def size(self) -> Tuple[int, int]:
        return self._width, self._height

    @property
    def low_points(self) -> Tuple[int, ...]:
        return self._low_points

    def _get_directions_for_index(self, index: int) -> Tuple[Direction, ...]:
        if index == 0:  # top left
            return (Direction.right, Direction.down)
        elif index == self._width - 1:  # top right
            return (Direction.left, Direction.down)
        elif index == len(self.vent_map) - 1:  # bottom right
            return (Direction.left, Direction.up)
        elif index == self._width * (self._height - 1):  # bottom left
            return (Direction.right, Direction.up)
        elif index < self._width - 1:  # top row
            return (Direction.left, Direction.right, Direction.down)
        elif index in self._left_indexes:  # left col
            return (Direction.right, Direction.up, Direction.down)
        elif index in self._right_indexes:  # right col
            return (Direction.left, Direction.up, Direction.down)
        elif self._width * (self._height - 1) < index and index < len(self.vent_map) - 1:  # bottom row
            return (Direction.left, Direction.right, Direction.up)
        return (Direction.left, Direction.right, Direction.up, Direction.down)

    def _adjacent_indexes_for_index(self, index: int) -> Tuple[int, ...]:
        indexes = []
        directions = self._get_directions_for_index(index)
        for direction in directions:
            value = index + self._width
            if direction == Direction.left:
                value = index - 1
            elif direction == Direction.right:
                value = index + 1
            elif direction == Direction.up:
                value = index - self._width
            indexes.append(value)
        return tuple(indexes)

    def _calculate_low_points(self) -> Tuple[int, ...]:
        low_points = []
        for vent_index, vent in enumerate(self.vent_map):
            adjacent_indexes = self._adjacent_indexes_for_index(vent_index)
            adjacent_values = [self.vent_map[idx] for idx in adjacent_indexes]
            if vent < sorted(adjacent_values)[0]:
                low_points.append(vent_index)
        return tuple(low_points)

    def _calculate_basin(self, point: int, basin: List[int]) -> Tuple[int, ...]:
        if point not in basin:
            basin.append(point)
            adjacent_points = self._adjacent_indexes_for_index(point)
            for adjacent_point in adjacent_points:
                adjacent_value = self.vent_map[adjacent_point]
                if adjacent_value >= self.vent_map[point] and adjacent_value != 9:
                    self._calculate_basin(adjacent_point, basin)
        return tuple(basin)

    def calculate_basins(self) -> Tuple[int, ...]:
        return tuple(self._calculate_basin(point, []) for point in self.low_points)


def calculate_map_low_points(filename: str) -> None:
    vent_map = VentMap(*parse(filename))
    print(sum([vent_map.vent_map[idx] + 1 for idx in vent_map.low_points]))


def calculate_map_basins(filename: str) -> None:
    vent_map = VentMap(*parse(filename))
    print(reduce(lambda x, y: x * y, sorted([len(basin) for basin in vent_map.calculate_basins()], reverse=True)[0:3]))


if __name__ == "__main__":
    test_filename = "2021/09-test.txt"
    filename = "2021/09.txt"

    calculate_map_low_points(test_filename)
    calculate_map_low_points(filename)

    calculate_map_basins(test_filename)
    calculate_map_basins(filename)
