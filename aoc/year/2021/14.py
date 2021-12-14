"""
--- Day 14: Extended Polymerization ---

The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has polymerization equipment that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves should even have the necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C

The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

    The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
    The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
    The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.

Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times; taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?

--- Part Two ---

The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more steps of the pair insertion process; a total of 40 steps should do it.

In the above example, the most common element is B (occurring 2192039569602 times) and the least common element is H (occurring 3849876073 times); subtracting these produces 2188189693529.

Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?

"""
from collections import defaultdict
from typing import Dict, Tuple

from aoc import utils


def parse(filename: str) -> Tuple[str, Dict[str, str]]:
    template = ""
    insertion_pairs = {}

    for line in utils.read_lines(filename, True):
        if line:
            parts = line.split("->")
            if len(parts) == 1:
                template = parts[0].strip()
            else:
                insertion_pairs[parts[0].strip()] = parts[1].strip()
    return template, insertion_pairs


class Polymerization:
    def __init__(self, template: str, insertion_pairs: Dict[str, str]) -> None:
        self._template = template
        self._insertion_pairs = insertion_pairs

    def _formulate(
        self, current_pairs: Dict[str, int], elements: Dict[str, int], steps: int, current_step: int
    ) -> None:
        if current_step == steps:
            return

        new_pairs = defaultdict(int)
        for i_pair, i_element in self._insertion_pairs.items():
            pair_count = current_pairs.get(i_pair, 0)
            elements[i_element] += pair_count
            new_pairs[f"{i_pair[0]}{i_element}"] += pair_count
            new_pairs[f"{i_element}{i_pair[1]}"] += pair_count

        self._formulate(new_pairs, elements, steps, current_step + 1)

    def formulate(self, steps: int) -> Dict[str, int]:
        elements = defaultdict(int)
        for letter in self._template:
            elements[letter] += 1
        current_pairs = defaultdict(int)
        for i in range(len(self._template) - 1):
            current_pairs[f"{self._template[i]}{self._template[i + 1]}"] += 1

        self._formulate(current_pairs, elements, steps, 0)
        return elements


def calcumate_element_spread(filename: str, steps: int) -> None:
    template, pairs = parse(filename)
    poly = Polymerization(template, pairs)
    elements = poly.formulate(steps)

    most = max(elements.values())
    least = min(elements.values())
    print(most - least)


if __name__ == "__main__":
    test_filename = "2021/14-test.txt"
    filename = "2021/14.txt"
    steps_part_one = 10
    steps_part_two = 40

    calcumate_element_spread(test_filename, steps_part_one)
    calcumate_element_spread(filename, steps_part_one)

    calcumate_element_spread(test_filename, steps_part_two)
    calcumate_element_spread(filename, steps_part_two)
