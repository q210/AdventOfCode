"""
--- Day 3: Toboggan Trajectory ---

With the toboggan login problems resolved, you set off toward the airport. While travel by toboggan might be easy, it's certainly not safe: there's very minimal steering and the area is covered in trees. You'll need to see which angles will take you near the fewest trees.

Due to the local geology, trees in this area only grow on exact integer coordinates in a grid. You make a map (your puzzle input) of the open squares (.) and trees (#) you can see. For example:

..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
These aren't the only trees, though; due to something you read about once involving arboreal genetics and biome stability, the same pattern repeats to the right many times:

..##.........##.........##.........##.........##.........##.......  --->
#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........#.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...##....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
You start on the open square (.) in the top-left corner and need to reach the bottom (below the bottom-most row on your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers rational numbers); start by counting all the trees you would encounter for the slope right 3, down 1:

From your starting position at the top-left, check the position that is right 3 and down 1. Then, check the position that is right 3 and down 1 from there, and so on until you go past the bottom of the map.

The locations you'd check in the above example are marked here with O where there was an open square and X where there was a tree:

..##.........##.........##.........##.........##.........##.......  --->
#..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........X.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...#X....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
In this example, traversing the map using this slope would cause you to encounter 7 trees.

Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?
"""
import sys
from collections import Counter

DEBUG = False
data = [
    [
        """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""",
        336,
    ],
    [
        """....
...#
...#""",
        0,
    ],
    [
        """...#....
.#..#.#.
.##...#.""",
        2,
    ],
    [
        """...#
.#.#
.##.""",
        16,
    ],
    [
        """....#.#..#.#.#.#......#....##.#
..##..#.#..#.##.....#.....#....
....#..#...#..#..####.##.#.##..
...............#.....##..##..#.
##...####..##.#..#...####...#.#
..#.#....##....##.........#...#
.#..#.##..............#.....###
##..##..#.....#..#...#....#....
.#.........#..#...#.#.#.....#..
......#...#..#.##..#.....#.#...
.#...#.#.#.##.##.....###...#...
..........#.......#...#....#..#
.....##..#.#...#...##.##.......
...#.###.#.#..##...#.#.........""",
        240,
    ],
]


def main(lines):
    slopes = [(1, False), (3, False), (5, False), (7, False), (1, True)]
    width = len(lines[0])
    results = 1

    for h_step, only_odd in slopes:
        trees_num = 0
        cursor = 0
        for index, line in enumerate(lines):
            if only_odd and index % 2:
                continue

            if line[cursor % width] == "#":
                trees_num += 1

            cursor += h_step

        print(trees_num)
        results *= trees_num

    return results


def test():
    errors = False
    for input, test_result in data:
        result = main(input.split("\n"))

        print(input, ", expected:", test_result, ", actual:", result)
        try:
            assert test_result == result
        except AssertionError as exc:
            print("ERROR", exc)
            errors = True

    if errors:
        print("got errors!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        DEBUG = True

    if DEBUG:
        test()

    else:
        with open("task3_1.input") as f:
            print(main([line.strip("\n") for line in f.readlines()]))
