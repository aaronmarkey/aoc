"""
--- Day 1: Report Repair ---
After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

--- Part Two ---
The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?
"""
# https://adventofcode.com/2020/day/1/input

from aoc import utils


def get_left_right(left, right, value):
    for left_num in reversed(left):
        for right_num in right:
            if left_num + right_num == value:
                return left_num, right_num
    return None, None


def get_numbers(filepath):
    data = []
    for line in utils.read_lines(filepath):
        num = line.strip()
        if num:
            data.append(int(num))
    return data


def get_parts(data, value):
    mid = int(value / 2)

    mid_idx = -1
    for idx, num in enumerate(data):
        mid_idx = idx
        if num == mid or num > mid:
            break

    left = data[: mid_idx + 1]
    right = data[mid_idx:]

    left_num, right_num = get_left_right(left, right, value)

    if left_num and right_num:
        return left_num, right_num
    return None, None


def part_one(filepath, value):
    data = get_numbers(filepath)
    data.sort()
    left, right = get_parts(data, value)

    if left and right:
        return left, right, left * right
    return None, None, None


def part_two(filepath, value):
    data = get_numbers(filepath)
    data.sort()

    for idx, num in enumerate(data):
        difference = value - num
        sub_data = data[: idx + 1] + data[idx + 1 :]
        left, right = get_parts(sub_data, difference)
        if left and right:
            return num, left, right, num * left * right
    return None, None, None, None


if __name__ == "__main__":
    value = 2020
    filepath = "2020/01.txt"
    print(part_one(filepath, value))
    print(part_two(filepath, value))
