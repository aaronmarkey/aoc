"""
--- Day 5: Doesn't He Have Intern-Elves For This? ---
Santa needs help figuring out which strings in his text file are naughty or nice.

A nice string is one with all of the following properties:

It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
For example:

ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...), a double letter (...dd...), and none of the disallowed substrings.
aaa is nice because it has at least three vowels and a double letter, even though the letters used by different rules overlap.
jchzalrnumimnmhp is naughty because it has no double letter.
haegwjzuvuyypxyu is naughty because it contains the string xy.
dvszwmarrgswjxmb is naughty because it contains only one vowel.

--- Part Two ---
Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
For example:

qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that repeats with exactly one letter between them (zxz).
xxyxx is nice because it has a pair that appears twice and a letter that repeats with one between, even though the letters used by each rule overlap.
uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo), but no pair that appears twice.
How many strings are nice under these new rules?
"""
# https://adventofcode.com/2015/day/5/input

import re

from aoc import utils


def part_one(filepath):
    double_letters = re.compile(r"(.)\1{1,}")
    three_vowels = re.compile(r"^(.*[aeiou].*){3,}$")
    does_not_have = re.compile(r"^((?!ab|cd|pq|xy).)*$")

    valid_count = 0

    for line in utils.read_lines(filepath, strip=True):
        has_double_letters = double_letters.search(line) is not None
        has_three_vowels = three_vowels.search(line) is not None
        has_does_not_have = does_not_have.search(line) is not None
        if has_double_letters and has_three_vowels and has_does_not_have:
            valid_count += 1

    return valid_count


def part_two(filepath):
    double_pairs = re.compile(r"([a-z][a-z]).*\1")
    skip_letter = re.compile(r"([a-z]).{1}\1")

    valid_count = 0

    for line in utils.read_lines(filepath, strip=True):
        has_double_pairs = double_pairs.search(line) is not None
        has_skip_letter = skip_letter.search(line) is not None
        if has_double_pairs and has_skip_letter:
            valid_count += 1

    return valid_count


if __name__ == "__main__":
    filepath = "2015/05.txt"
    print(part_one(filepath))
    print(part_two(filepath))
