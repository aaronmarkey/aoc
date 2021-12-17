"""
Poorly.

--- Day 15: Chiton ---

You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can barely still fit, though; the main problem is that the walls of the cave are covered in chitons, and it would be best not to bump any of them.

The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input). For example:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).

What is the lowest total risk of any path from the top left to the bottom right?
"""
from typing import Any, Optional

from aoc import utils


Matrix = tuple[tuple[int, ...], ...]


def parse(filename: str) -> Matrix:
    data = []
    for line in utils.read_lines(filename, True):
        data.append(tuple(int(x) for x in line))
    return tuple(data)


def one_to_two(index: int, width: int) -> tuple[int, int]:
    return (int(index / width), (index % width))


def two_to_one(index: tuple[int, int], width: int) -> int:
    return index[0] * width + index[1]


def calculate_neighbor_indexes(index: int, ignore: tuple[int, ...], width: int, height: int) -> tuple[int, ...]:
    neighbors = set()
    ignore = set([one_to_two(i, width) for i in ignore + (index,)])
    matrix_index = one_to_two(index, width)

    for row in range(-1, 2):
        for col in range(-1, 2):
            new_row = matrix_index[0] + row
            new_col = matrix_index[1] + col

            if 0 <= new_row and new_row < height and 0 <= new_col and new_col < width:
                if new_row == matrix_index[0] or new_col == matrix_index[1]:
                    neighbors.add((new_row, new_col))

    neighbors -= ignore
    return tuple(two_to_one(n, width) for n in neighbors)


class Node:
    def __init__(self, id_: int, value: int) -> None:
        self.id = id_
        self.value = value
        self.distance_from_start = -1
        self.previous_node: Optional[Node] = None

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False


class Cave:
    def __init__(self, matrix: Matrix) -> None:
        self._matrix = matrix

    def _create_node(self, index: tuple[int, int], width) -> Node:
        row = int(index[0] / len(self._matrix))
        col = int(index[1] / len(self._matrix[0]))

        matrix_position_row = index[0] - (len(self._matrix) * row)
        matrix_position_col = index[1] - (len(self._matrix[0]) * col)

        value = self._matrix[matrix_position_row][matrix_position_col] + row + col
        if value > 9:
            value = value % 9

        return Node(two_to_one(index, width), value)

    def _shortest_distance(self, width: int, height: int) -> int:
        all_nodes: dict[int:Node] = {}

        unvisited = set()
        for row in range(height):
            for col in range(width):
                unvisited.add(two_to_one((row, col), width))

        current_node = self._create_node((0, 0), width)
        current_node.distance_from_start = 0
        all_nodes[0] = current_node

        while unvisited:
            neighbor_indexes = calculate_neighbor_indexes(current_node.id, tuple(), width, height)
            for neighbor_index in neighbor_indexes:
                if neighbor_index in unvisited:
                    if neighbor_index not in all_nodes:
                        all_nodes[neighbor_index] = self._create_node(one_to_two(neighbor_index, width), width)
                    neighbor_node = all_nodes[neighbor_index]
                    tentative_distance = current_node.distance_from_start + neighbor_node.value
                    if (
                        neighbor_node.distance_from_start == -1
                        or tentative_distance < neighbor_node.distance_from_start
                    ):
                        neighbor_node.distance_from_start = tentative_distance
                        neighbor_node.previous_node = current_node

            unvisited.remove(current_node.id)

            next_id = -1
            for node_id in unvisited:
                if next_id == -1 or (
                    node_id in all_nodes
                    and all_nodes[node_id].distance_from_start < all_nodes[next_id].distance_from_start
                ):
                    next_id = node_id
            if next_id != -1:
                current_node = all_nodes[next_id]

        return all_nodes[len(all_nodes) - 1].distance_from_start

    def shortest_distance(self) -> int:
        return self._shortest_distance(len(self._matrix[0]), len(self._matrix))

    def shortest_distance_repeat(self, repeat: int) -> int:
        return self._shortest_distance(len(self._matrix[0]) * repeat, len(self._matrix) * repeat)


def shortest_distance(filename: str) -> None:
    data = parse(filename)
    cave = Cave(data)
    print(cave.shortest_distance())


def shortest_distance_repeat(filename: str, repeat: int) -> None:
    data = parse(filename)
    cave = Cave(data)
    print(cave.shortest_distance_repeat(repeat))


if __name__ == "__main__":
    test_filename = "2021/15-test.txt"
    filename = "2021/15.txt"
    repeat = 5

    shortest_distance(test_filename)
    shortest_distance(filename)
    shortest_distance_repeat(test_filename, repeat)
    shortest_distance_repeat(filename, repeat)
