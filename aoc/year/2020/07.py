"""
--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)

--- Part Two ---
It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
"""
# https://adventofcode.com/2020/day/7/input


from functools import reduce

from aoc import utils


class Node:
    def __init__(self, name):
        self.name = name
        self.parents = set()
        self.children = set()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"<Node: {self.name}>"


class DirectedGraph:
    def __init__(self):
        self._node_map = {}

    def _make_node(self, name):
        return Node(name)

    def add_node(self, node_name):
        node = self._make_node(node_name)
        if node_name not in self._node_map:
            self._node_map[node_name] = node

    def add_parent(self, node_name, parent_name):
        parent = self._node_map[parent_name]
        self._node_map[node_name].parents.add(parent)

    def add_child(self, node_name, child_name, child_count):
        child = self._node_map[child_name]
        self._node_map[node_name].children.add((child, child_count))

    def _get_ancestors(self, node, ancestors):
        for parent in node.parents:
            ancestors.append(parent)
            self._get_ancestors(parent, ancestors)
        return ancestors

    def _get_nested_count(self, node):
        total = 0
        if len(node.children) > 0:
            for child in node.children:
                (child_node, child_count) = child
                total += child_count
                total += child_count * self._get_nested_count(child_node)
        return total

    def get_unique_ancestors(self, node_name):
        node = self._node_map[node_name]
        return set(self._get_ancestors(node, []))

    def get_nested_count(self, node_name):
        node = self._node_map[node_name]
        return self._get_nested_count(node)


def get_bag_name(bag_str):
    name = bag_str.replace("bags", "").replace(".", "").replace("bag", "")
    return name.strip()


def get_child_bag(bag_str):
    bag_name = get_bag_name(bag_str)
    return bag_name.split(" ", 1)


def get_bags(line):
    bag = None
    parts = line.split("contain")
    bag = get_bag_name(parts[0])
    if parts[1].strip() == "no other bags.":
        return bag, []
    children = parts[1].split(",")

    bag_children = []
    for child in children:
        count, name = get_child_bag(child)
        bag_children.append((int(count), name))
    return bag, bag_children


def build_graph(filepath):
    graph = DirectedGraph()
    for line in utils.read_lines(filepath):
        bag, children = get_bags(line)
        graph.add_node(bag)
        for child in children:
            (count, name) = child
            graph.add_node(name)
            graph.add_child(bag, name, count)
            graph.add_parent(name, bag)
    return graph


def part_one(filepath, name):
    graph = build_graph(filepath)
    unique_ancestors = graph.get_unique_ancestors("shiny gold")
    return len(unique_ancestors)


def part_two(filepath, name):
    graph = build_graph(filepath)
    return graph.get_nested_count(name)


if __name__ == "__main__":
    filepath = "2020/07.txt"
    name = "shiny gold"
    print(part_one(filepath, name))
    print(part_two(filepath, name))
