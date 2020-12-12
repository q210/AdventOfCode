"""
--- Part Two ---

As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

.............
.L.L.#.#.#.#.
.............
The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?
"""
import sys
from copy import deepcopy
from typing import List, Tuple, Set

DEBUG = False
data = [
    [
        """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""",
        26,
    ]
]


def neighbors_rating(cursor_row: int, cursor_column: int, seat_map: List[List[str]]):
    width = len(seat_map[0])
    height = len(seat_map)
    rating = 0
    # print('processing', cursor_row, cursor_column)
    for h_direction in [-1, 0, 1]:
        for v_direction in [-1, 0, 1]:
            step = 1
            # print('dir', h_direction, v_direction)
            while h_direction or v_direction:
                row = cursor_row + h_direction * step
                column = cursor_column + v_direction * step
                if not (row in range(0, height) and column in range(0, width)):
                    break

                seat_state = seat_map[row][column]
                step += 1

                if seat_state == ".":
                    continue

                if seat_state == "L":
                    break

                if seat_state == "#":
                    # is a occupied see adjacent to cursor
                    rating += 1
                    break

    # print('rating', rating)
    # sys.stdin.read(1)
    return rating


def new_seat_state(state, rating):
    if state == "#" and rating >= 5:
        return "L"

    if state == "L" and rating == 0:
        return "#"

    return state


def main(seat_map_lines: List[str]):
    width = len(seat_map_lines[0])
    seat_map = []
    for row_index, line in enumerate(seat_map_lines):
        seat_map.append(list(line.replace("L", "#")))

    # print('initial')
    # for row in seat_map:
    #     print(''.join(row))
    # print('forbidden', floor)

    while True:
        next_round_map = deepcopy(seat_map)
        occupied = 0
        for cursor_row in range(len(seat_map)):
            for cursor_column in range(width):
                if seat_map[cursor_row][cursor_column] == ".":
                    # not a seat
                    continue

                seat_rating = neighbors_rating(cursor_row, cursor_column, seat_map)
                seat_state = seat_map[cursor_row][cursor_column]
                next_round_map[cursor_row][cursor_column] = new_seat_state(seat_state, seat_rating)
                if next_round_map[cursor_row][cursor_column] == "#":
                    occupied += 1

        if next_round_map == seat_map:
            return occupied

        seat_map = next_round_map
        # print()
        # for row in seat_map:
        #     print(''.join(row))


def test():
    errors = False
    for input, test_result in data:
        result = main(input.strip().split("\n"))

        print(input, ", expected:", test_result, ", actual:", result, "\n")
        try:
            assert test_result == result
        except AssertionError as exc:
            print("ERROR", exc)
            errors = True

    if errors:
        print("\n\ngot errors!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        DEBUG = True

    if DEBUG:
        test()

    else:
        with open("task11_1.input") as f:
            print(main([line.strip() for line in f.readlines()]))
