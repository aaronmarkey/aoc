"""
--- Day 3: Perfectly Spherical Houses in a Vacuum ---
Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and then an elf at the North Pole calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^), south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off, and Santa ends up visiting some houses more than once. How many houses receive at least one present?

For example:

> delivers presents to 2 houses: one at the starting location, and one to the east.
^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.

--- Part Two ---
The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.
"""
# https://adventofcode.com/2015/day/3/input

from dataclasses import dataclass

from aoc import utils


@dataclass
class Point:
    x: int
    y: int

    @property
    def key(self):
        return (self.x, self.y)


def get_letters(filepath):
    data = utils.read_file(filepath)
    for char in data:
        yield char


def update_point(point, char):
    if char == "<":
        point.x += -1
    elif char == ">":
        point.x += 1
    elif char == "^":
        point.y += 1
    elif char == "v":
        point.y += -1


def part_one(filepath):
    houses = set()
    point = Point(x=0, y=0)
    houses.add(point.key)
    for char in get_letters(filepath):
        update_point(point, char)
        houses.add(point.key)
    return len(houses)


def part_two(file_path):
    houses = set()
    santa_point = Point(x=0, y=0)
    robo_point = Point(x=0, y=0)
    houses.add(santa_point.key)
    for idx, char in enumerate(get_letters(filepath)):
        if idx % 2 == 0:
            update_point(santa_point, char)
            houses.add(santa_point.key)
        else:
            update_point(robo_point, char)
            houses.add(robo_point.key)
    return len(houses)


if __name__ == "__main__":
    filepath = "2015/03.txt"
    print(part_one(filepath))
    print(part_two(filepath))
