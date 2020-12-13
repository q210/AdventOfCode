"""
--- Part Two ---

Before you can give the destination to the captain, you realize that the actual action meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.
The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.

For example, using the same instructions as above:

F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?
"""
import sys
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple, Set, Optional

DEBUG = False
data = [
    [
        """
F10
N3
F7
L270
F11
""",
        286,
    ]
]


def main(instructions: List[str]):
    position = [0, 0]  # east, north
    waypoint = [10, 1]  # east, north

    for instruction in instructions:
        code = instruction[0]
        value = int(instruction[1:])

        if code in "WSEN":
            direction = "WSEN".index(code) - 2
            waypoint[direction] += value * (-1 if direction < 0 else 1)

        elif code in "LR":
            if (value // 90) % 2:
                if (value // 90) % 3 == 0:
                    code = "L" if code == "R" else "R"

                waypoint = [(-1 if code == "L" else 1) * waypoint[1], (-1 if code == "R" else 1) * waypoint[0]]

            elif (value // 180) % 2:
                waypoint = [-1 * waypoint[0], -1 * waypoint[1]]

        else:
            # forward
            for index in range(2):
                position[index] += waypoint[index] * value

        print(instruction, position, waypoint)

    return abs(position[0]) + abs(position[1])


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
        with open("task12_1.input") as f:
            print(main([line.strip() for line in f.readlines()]))
