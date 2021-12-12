"""
--- Day 12: Passage Pathing ---

With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this cave anytime soon is by finding a path yourself. Not just a path - the only way to know if you've found the best path is to find all of them.

Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves (your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end

This is a list of how all of the caves are connected. You start in the cave named start, and your destination is the cave named end. An entry like b-d means that cave b is connected to cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
    \   /
     end

Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end

(Each line in the above list corresponds to a single path; the caves visited by that path are listed in the order they are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited twice (once on the way to cave d and a second time when returning from cave d), and since cave b is small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc

The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end

Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW

How many paths through this cave system are there that visit small caves at most once?

--- Part Two ---

After reviewing the available paths, you realize you might have time to visit a single small cave twice. Specifically, big caves can be visited any number of times, a single small cave can be visited at most twice, and the remaining small caves can be visited at most once. However, the caves named start and end can only be visited exactly once each: once you leave the start cave, you may not return to it, and once you reach the end cave, the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end

The slightly larger example above now has 103 paths through it, and the even larger example now has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?
"""
from collections import defaultdict
from copy import deepcopy
from enum import Enum
from typing import Any, Dict, List, Set, Tuple

from aoc import utils


class CaveType(Enum):
    start = 1
    end = 2
    big = 3
    small = 4


class Cave:
    START = "start"
    END = "end"

    def __init__(self, id_: str) -> None:
        self.id = id_
        self._hash = int("".join(str(ord(char)) for char in self.id))

        if self.id == self.START:
            self.type = CaveType.start
        elif self.id == self.END:
            self.type = CaveType.end
        elif self.id.isupper():
            self.type = CaveType.big
        else:
            self.type = CaveType.small

    def __hash__(self) -> str:
        return self._hash

    def __eq__(self, other: Any) -> bool:
        return self.id == other

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return str(self)


class CaveNetwork:
    def __init__(self) -> None:
        self._network: Dict[Cave, Set[Cave]] = {}

    def add_edge(self, start, end) -> None:
        if start not in self._network:
            self._network[start] = set()
        if end not in self._network:
            self._network[end] = set()
        self._network[start].add(end)
        self._network[end].add(start)

    def _navigate_to_cave(
        self,
        cave: Cave,
        smalls_visited: Dict,
        max_small: int,
        max_limit_reached: bool,
        current_path: List[Cave],
        valid_paths: List[List[Cave]],
    ) -> None:
        current_path.append(cave)
        if cave.type == CaveType.small:
            smalls_visited[cave] += 1
            if smalls_visited[cave] >= max_small:
                max_limit_reached = True
        if cave.type == CaveType.end:
            valid_paths.append(current_path)
            return

        for next_cave in self._network[cave]:
            if next_cave != cave and next_cave.type != CaveType.start:
                if next_cave.type != CaveType.small or (smalls_visited[next_cave] == 0 or not max_limit_reached):
                    self._navigate_to_cave(
                        next_cave,
                        deepcopy(smalls_visited),
                        max_small,
                        max_limit_reached,
                        deepcopy(current_path),
                        valid_paths,
                    )

    def valid_paths(self, max_small_visits: int) -> Tuple[Tuple[Cave, ...], ...]:
        valid_paths = []
        small_visited = defaultdict(int)
        self._navigate_to_cave(Cave("start"), small_visited, max_small_visits, False, [], valid_paths)
        return valid_paths


def parse(filename: str):
    for line in utils.read_lines(filename, True):
        start, end = line.split("-")
        yield Cave(start), Cave(end)


def calculate_valid_paths(filename: str, limit: int) -> None:
    network = CaveNetwork()
    for start, end in parse(filename):
        network.add_edge(start, end)

    print(len(network.valid_paths(limit)))


if __name__ == "__main__":
    test_filename = "2021/12-test.txt"
    filename = "2021/12.txt"

    calculate_valid_paths(test_filename, 1)
    calculate_valid_paths(filename, 1)

    calculate_valid_paths(test_filename, 2)
    calculate_valid_paths(filename, 2)
