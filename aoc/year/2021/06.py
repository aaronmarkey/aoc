"""--- Day 6: Lanternfish ---

The sea floor is getting steeper. Maybe the sleigh keys got carried this way?

A massive school of glowing lanternfish swims past. They must spawn quickly to reach such large numbers - maybe exponentially quickly? You should model their growth rate to be sure.

Although you know nothing about this specific species of lanternfish, you make some guesses about their attributes. Surely, each lanternfish creates a new lanternfish once every 7 days.

However, this process isn't necessarily synchronized between every lanternfish - one lanternfish might have 2 days left until it creates another lanternfish, while another might have 4. So, you can model each fish as a single number that represents the number of days until it creates a new lanternfish.

Furthermore, you reason, a new lanternfish would surely need slightly longer before it's capable of producing more lanternfish: two more days for its first cycle.

So, suppose you have a lanternfish with an internal timer value of 3:

	After one day, its internal timer would become 2.
	After another day, its internal timer would become 1.
	After another day, its internal timer would become 0.
	After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
	After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.

A lanternfish that creates a new fish resets its timer to 6, not 7 (because 0 is included as a valid timer value). The new lanternfish starts with an internal timer of 8 and does not start counting down until the next day.

Realizing what you're trying to do, the submarine automatically produces a list of the ages of several hundred nearby lanternfish (your puzzle input). For example, suppose you were given the following list:

3,4,3,1,2

This list means that the first fish has an internal timer of 3, the second fish has an internal timer of 4, and so on until the fifth fish, which has an internal timer of 2. Simulating these fish over several days would proceed as follows:

Initial state: 3,4,3,1,2  = 13
After  1 day:  2,3,2,0,1  = 8
After  2 days: 1,2,1,6,0,8  = 10 - 18
After  3 days: 0,1,0,5,6,7,8 = 19 - 27
After  4 days: 6,0,6,4,5,6,7,8,8 = 34 - 50
After  5 days: 5,6,5,3,4,5,6,7,7,8 = 48 - 56
After  6 days: 4,5,4,2,3,4,5,6,6,7 - 46
After  7 days: 3,4,3,1,2,3,4,5,5,6 - 36
After  8 days: 2,3,2,0,1,2,3,4,4,5 - 26
After  9 days: 1,2,1,6,0,1,2,3,3,4,8 = 23 - 31
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8 = 27 - 35
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8

Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, while each other number decreases by 1 if it was present at the start of the day.

In this example, after 18 days, there are a total of 26 fish. After 80 days, there would be a total of 5934.

Find a way to simulate lanternfish. How many lanternfish would there be after 80 days?

--- Part Two ---

Suppose the lanternfish live forever and have unlimited food and space. Would they take over the entire ocean?

After 256 days in the example above, there would be a total of 26984457539 lanternfish!

How many lanternfish would there be after 256 days?

"""
from collections import defaultdict
from typing import Tuple

from aoc import utils


def parse(filename: str) -> Tuple[int, ...]:
	data = utils.read_file(filename)
	return tuple(int(x) for x in data.strip().split(","))


def simulate_lanternfish(fishes: Tuple[int, ...], days: int) -> int:
	NEW_REPRO_RATE = 8
	OLD_REPRO_RATE = 6

	fish_map = [0 for _ in range(NEW_REPRO_RATE + 1)]
	for fish in fishes:
		fish_map[fish] += 1

	count = len(fishes)
	number_of_fish_to_add = 0
	for day in range(days):
		new_map = [0 for _ in range(NEW_REPRO_RATE + 1)]

		for idx, fish_count in enumerate(fish_map):
			if idx == 0:
				number_of_fish_to_add += fish_count
			else:
				new_map[idx-1] = fish_count

		if number_of_fish_to_add > 0:
			new_map[OLD_REPRO_RATE] += number_of_fish_to_add
			new_map[NEW_REPRO_RATE] += number_of_fish_to_add
			count += number_of_fish_to_add
			number_of_fish_to_add = 0
		fish_map = new_map
	return count




if __name__ == "__main__":
	test_filename = "2021/06-test.txt"
	filename = "2021/06.txt"

	days_18 = 18
	days_80 = 80
	days_256 = 256

	test_sim_18 = simulate_lanternfish(parse(test_filename), days_18)
	test_sim_80 = simulate_lanternfish(parse(test_filename), days_80)
	test_sim_256 = simulate_lanternfish(parse(test_filename), days_256)
	print(f"{days_18} test: {test_sim_18}")
	print(f"{days_80} test: {test_sim_80}")
	print(f"{days_256} test: {test_sim_256}")

	sim_18 = simulate_lanternfish(parse(filename), days_18)
	sim_80 = simulate_lanternfish(parse(filename), days_80)
	sim_256 = simulate_lanternfish(parse(filename), days_256)
	print(f"{days_18}: {sim_18}")
	print(f"{days_80}: {sim_80}")
	print(f"{days_256}: {sim_256}")
