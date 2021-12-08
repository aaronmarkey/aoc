"""
--- Day 7: The Treachery of Whales ---

A giant whale has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!

Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! They seem to be preparing to blast a hole in the ocean floor; sensors indicate a massive underground cave system just beyond where they're aiming!

The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?

There's one major catch - crab submarines can only move horizontally.

You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.

For example, consider the following horizontal positions:

16,1,2,0,4,2,7,1,2,14

This means there's a crab with horizontal position 16, a crab with horizontal position 1, and so on.

Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position 2:

    Move from 16 to 2: 14 fuel
    Move from 1 to 2: 1 fuel
    Move from 2 to 2: 0 fuel
    Move from 0 to 2: 2 fuel
    Move from 4 to 2: 2 fuel
    Move from 2 to 2: 0 fuel
    Move from 7 to 2: 5 fuel
    Move from 1 to 2: 1 fuel
    Move from 2 to 2: 0 fuel
    Move from 14 to 2: 12 fuel

This costs a total of 37 fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).

Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they spend to align to that position?

--- Part Two ---

The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?

As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.

As each crab moves, moving further becomes more expensive. This changes the best horizontal position to align them all on; in the example above, this becomes 5:

    Move from 16 to 5: 66 fuel
    Move from 1 to 5: 10 fuel
    Move from 2 to 5: 6 fuel
    Move from 0 to 5: 15 fuel
    Move from 4 to 5: 1 fuel
    Move from 2 to 5: 6 fuel
    Move from 7 to 5: 3 fuel
    Move from 1 to 5: 10 fuel
    Move from 2 to 5: 6 fuel
    Move from 14 to 5: 45 fuel

This costs a total of 168 fuel. This is the new cheapest possible outcome; the old alignment position (2) now costs 206 fuel instead.

Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! How much fuel must they spend to align to that position?


16,1,2,0,4,2,7,1,2,14
0,1,1,2,2,2,6,7,14,16


95167367 -- too high
"""
import statistics
from typing import Tuple

from aoc import utils


def parse(filename: str) -> Tuple[int, ...]:
    data = utils.read_file(filename)
    return tuple(int(x) for x in data.strip().split(","))


def calculate_fuel_simple(filename: str) -> int:
    position = 0
    crabs = parse(filename)

    crabs = sorted(list(crabs))
    position = int(statistics.median(crabs))

    fuel = 0
    for crab in crabs:
        fuel += abs(crab - position)
    return fuel


def calculate_fuel_complex(filename: str) -> int:
    position = 0
    crabs = parse(filename)

    avg = statistics.mean(crabs)
    avg_low = int(avg)
    avg_high = int(avg + 1)

    fuel_low = fuel_high = 0
    for crab in crabs:
        fuel_low += sum([i + 1 for i in range(abs(crab - avg_low))])
        fuel_high += sum([i + 1 for i in range(abs(crab - avg_high))])
    return fuel_high if fuel_high < fuel_low else fuel_low


if __name__ == "__main__":
    test_filename = "2021/07-test.txt"
    filename = "2021/07.txt"

    print(calculate_fuel_simple(test_filename))
    print(calculate_fuel_simple(filename))

    print(calculate_fuel_complex(test_filename))
    print(calculate_fuel_complex(filename))
