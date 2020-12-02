"""
--- Day 2: Password Philosophy ---
Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via toboggan.

The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers; we can't log in!" You ask if you can take a look.

Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the Official Toboggan Corporate Policy that was in effect when they were chosen.

To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted database) and the corporate policy when that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
Each line gives the password policy and then the password. The password policy indicates the lowest and highest number of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.

In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of their respective policies.

How many passwords are valid according to their policies?

--- Part Two ---
While it appears you validated the passwords correctly, they don't seem to be what the Official Toboggan Corporate Authentication System is expecting.

The shopkeeper suddenly realizes that he just accidentally explained the password policy rules from his old job at the sled rental place down the street! The Official Toboggan Corporate Policy actually works a little differently.

Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy enforcement.

Given the same example list from above:

1-3 a: abcde is valid: position 1 contains a and position 3 does not.
1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
How many passwords are valid according to the new interpretation of the policies?
"""
# https://adventofcode.com/2020/day/2/input

from dataclasses import dataclass

from aoc import utils


@dataclass
class Rule:
    min: int
    max: int
    char: str

    @staticmethod
    def from_rule_str(rule):
        char = rule[-1]
        min_max = rule.split(" ")[0]
        min, max = map(lambda x: int(x), min_max.split("-"))
        return Rule(char=char, min=min, max=max)

    def is_valid_password_for_sled(self, password):
        count = sum([1 for char in password if char == self.char])
        return self.min <= count and count <= self.max
        
    def is_valid_password_for_santa(self, password):
        pos_min = password[self.min - 1] == self.char
        pos_max = password[self.max - 1] == self.char
        return pos_min ^ pos_max


def part_one_and_two(filpath):
    sled_count = 0
    santa_count = 0
    for line in utils.read_lines(filepath):
        rule_part, pwd_part = line.split(":")
        rule = Rule.from_rule_str(rule_part)
        if rule.is_valid_password_for_sled(pwd_part.strip()):
            sled_count += 1
        if rule.is_valid_password_for_santa(pwd_part.strip()):
            santa_count += 1
    return sled_count, santa_count


if __name__ == "__main__":
    filepath = "2020/02.txt"
    sled, santa = part_one_and_two(filepath)
    print(sled)
    print(santa)