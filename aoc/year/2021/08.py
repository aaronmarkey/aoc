"""
--- Day 8: Seven Segment Search ---

You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

 0, 6, 9
 a, g

So, to render a 1, only segments c and f would be turned on; the rest would be off. To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on each display. The submarine is still trying to display numbers by producing output on signal wires a through g, but those wires are connected to segments randomly. Worse, the wire/segment connections are mixed up separately for each four-digit display! (All of the digits within a display use the same connections, though.)

So, you might know that only signal wires b and g are turned on, but that doesn't mean segments b and g are turned on: the only digit that uses two segments is 1, so it must mean segments c and f are meant to be on. With just that information, you still can't tell which wire (b/g) goes to which segment (c/f). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of all ten unique signal patterns you see, and then write down a single four digit output value (your puzzle input). Using the signal patterns, you should be able to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf

(The entry is wrapped here to two lines so it fits; in your notes, it will all be on a single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally the four digit output value. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are). The unique signal patterns correspond to the ten different ways the submarine tries to render a digit using the current wire/segment connections. Because 7 is the only digit that uses three segments, dab in the above example means that to render a 7, signal lines d, a, and b are on. Because 4 is the only digit that uses four segments, eafb means that to render a 4, signal lines e, a, f, and b are on.

Using this information, you should be able to work out which combination of signal wires corresponds to each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, all of the digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce

Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?

--- Part Two ---

Through a little deduction, you should now be able to determine the remaining digits. Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf

After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc

So, the unique signal patterns would correspond to the following digits:

    acedgfb: 8
    cdfbe: 5
    gcdfa: 2
    fbcad: 3
    dab: 7
    cefabd: 9
    cdfgeb: 6
    eafb: 4
    cagedb: 0
    ab: 1

Then, the four digits of the output value can be decoded:

    cdfeb: 5
    fcadb: 3
    cdfeb: 5
    cdbaf: 3

Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:

    fdgacbe cefdb cefbgd gcbe: 8394
    fcgedb cgb dgebacf gc: 9781
    cg cg fdcagb cbg: 1197
    efabcd cedba gadfec cb: 9361
    gecf egdcabf bgf bfgea: 4873
    gebdcfa ecba ca fadegcb: 8418
    cefg dcbef fcge gbcadfe: 4548
    ed bcgafe cdgba cbgef: 1625
    gbdfcae bgc cg cgb: 8717
    fgae cfgab fg bagce: 4315

Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the four-digit output values. What do you get if you add up all of the output values?

"""
from collections import defaultdict
from functools import reduce
from typing import List

from aoc import utils


class Display:

    _segment_count_for_number = {
        0: 6,
        1: 2,
        2: 5,
        3: 5,
        4: 4,
        5: 5,
        6: 6,
        7: 3,
        8: 7,
        9: 6,
    }
    _numbers_for_segment_count = defaultdict(list)
    for key, value in _segment_count_for_number.items():
        _numbers_for_segment_count[value].append(key)

    def __init__(self, signals: List[str], output: List[str]) -> None:
        self.signals = signals
        self.output = output
        self._init_output()

    def _init_output(self) -> None:
        self._output_segments = [len(o) for o in self.output]
        self._signal_to_number = {}
        self._number_to_signal = {}
        self._correct_display_output = []

        self._process_signals()
        self._transform()

    def _signal_to_key(self, signal: str) -> str:
        return "".join(sorted(signal))

    def _process_signals(self) -> None:
        fives = []
        sixes = []
        for signal in self.signals:
            possible_numbers = self._numbers_for_segment_count[len(signal)]
            len_of_signal = len(signal)
            if len(possible_numbers) == 1:
                # 1, 4, 7, 8
                self._signal_to_number[self._signal_to_key(signal)] = possible_numbers[0]
                self._number_to_signal[possible_numbers[0]] = self._signal_to_key(signal)
            elif len_of_signal == 5:
                fives.append(signal)
            else:
                sixes.append(signal)

        fives_sets = [set(signal) for signal in fives]
        five_common = reduce(lambda x, y: x & y, fives_sets)
        for idx, five_set in enumerate(fives_sets):
            # 2, 3, 5
            unique = set(five_set) - five_common
            if self._signal_to_key(unique) == self._number_to_signal[1]:
                self._signal_to_number[self._signal_to_key(fives[idx])] = 3
                self._number_to_signal[3] = self._signal_to_key(fives[idx])
            elif len(unique & set(self._number_to_signal[4])) == 2:
                self._signal_to_number[self._signal_to_key(fives[idx])] = 5
                self._number_to_signal[5] = self._signal_to_key(fives[idx])
            else:
                self._signal_to_number[self._signal_to_key(fives[idx])] = 2
                self._number_to_signal[2] = self._signal_to_key(fives[idx])

        for signal in sixes:
            # 0, 6, 9
            if len(set(signal) & set(self._number_to_signal[4])) == 4:
                self._signal_to_number[self._signal_to_key(signal)] = 9
                self._number_to_signal[9] = self._signal_to_key(signal)
            elif len(set(signal) & set(self._number_to_signal[5])) == 5:
                self._signal_to_number[self._signal_to_key(signal)] = 6
                self._number_to_signal[6] = self._signal_to_key(signal)
            else:
                self._signal_to_number[self._signal_to_key(signal)] = 0
                self._number_to_signal[0] = self._signal_to_key(signal)

    def _transform(self) -> None:
        for output in self.output:
            try:
                final = self._signal_to_number[self._signal_to_key(output)]
            except KeyError:
                final = -1
            self._correct_display_output.append(final)

    def get_output_count(self, number: int) -> int:
        if number in [1, 4, 7, 8]:
            segments_for_number = self._segment_count_for_number[number]
            return sum([1 if x == segments_for_number else 0 for x in self._output_segments])
        return -1

    @property
    def correct_display_output(self) -> List[int]:
        return self._correct_display_output


def parse(filename: str):
    for line in utils.read_lines(filename, True):
        signal, output = tuple(x.strip() for x in line.split("|"))
        yield tuple(s for s in signal.split(" ")), tuple(o for o in output.split(" "))


def get_displays(filename: str) -> List[Display]:
    displays = []
    for signal, output in parse(filename):
        displays.append(Display(signal, output))
    return displays


def calculate_easy_output(filename: str) -> int:
    easy_numbers = [1, 4, 7, 8]
    displays = get_displays(filename)

    output_total = 0
    for display in displays:
        for number in easy_numbers:
            output_total += display.get_output_count(number)
    print(output_total)


def calculate_display_output(filename: str) -> int:
    displays = get_displays(filename)

    total = 0
    for display in displays:
        total += int("".join([str(x) for x in display.correct_display_output]))
    print(total)


if __name__ == "__main__":
    test_filename = "2021/08-test.txt"
    filename = "2021/08.txt"

    calculate_easy_output(test_filename)
    calculate_easy_output(filename)

    calculate_display_output(test_filename)
    calculate_display_output(filename)
