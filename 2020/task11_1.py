"""
--- Day 11: Seating System ---

Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

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
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

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
After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
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
        37,
    ]
]


def adjacent_area_rating(cursor_row: int, cursor_column: int, seat_map: List[List[str]], floor: Set[Tuple[int, int]]):
    rating = 0
    row_bounds = range(len(seat_map))
    column_bounds = range(0, len(seat_map[0]))
    for row in range(cursor_row - 1, cursor_row + 2):
        for column in range(cursor_column - 1, cursor_column + 2):
            if (row not in row_bounds) or (column not in column_bounds):
                # out of bounds
                continue

            if (row, column) in floor:
                # not a seat
                continue

            if (row, column) == (cursor_row, cursor_column):
                # cursor seat
                continue

            if seat_map[row][column] == "#":
                # is a occupied seat adjacent to cursor
                rating += 1

    return rating


def new_seat_state(state, rating):
    if state == "#" and rating >= 4:
        return "L"

    if state == "L" and rating == 0:
        return "#"

    return state


def main(seat_map_lines: List[str]):
    width = len(seat_map_lines[0])
    seat_map = []
    floor = set()
    for row_index, line in enumerate(seat_map_lines):
        floor |= {(row_index, index) for index, item in enumerate(line) if item == "."}
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
                if (cursor_row, cursor_column) in floor:
                    # not a seat
                    continue

                seat_rating = adjacent_area_rating(cursor_row, cursor_column, seat_map, floor)
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
