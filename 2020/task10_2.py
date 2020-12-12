"""
--- Part Two ---

To completely determine whether you have enough adapters, you'll need to figure out how many different ways they can be arranged. Every arrangement needs to connect the charging outlet to your device. The previous rules about when adapters can successfully connect still apply.

The first example above (the one that starts with 16, 10, 15) supports the following arrangements:

(0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, (22)
(0), 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 5, 7, 10, 12, 15, 16, 19, (22)
(0), 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 6, 7, 10, 12, 15, 16, 19, (22)
(0), 1, 4, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 7, 10, 12, 15, 16, 19, (22)
(The charging outlet and your device's built-in adapter are shown in parentheses.) Given the adapters from the first example, the total number of arrangements that connect the charging outlet to your device is 8.

The second example above (the one that starts with 28, 33, 18) has many arrangements. Here are a few:

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49, (52)

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 49, (52)

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 46, 48, 49, (52)

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 46, 49, (52)

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 47, 48, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
46, 48, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
46, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
47, 48, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
47, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
48, 49, (52)
In total, this set of adapters can connect the charging outlet to your device in 19208 distinct arrangements.

You glance back down at your bag and try to remember why you brought so many adapters; there must be more than a trillion valid ways to arrange them! Surely, there must be an efficient way to count the arrangements.

What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?
"""
import sys
from typing import List

DEBUG = False
data = [
    [[16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4], 8,],
    [
        [
            28,
            33,
            18,
            42,
            31,
            14,
            46,
            20,
            48,
            47,
            24,
            23,
            49,
            45,
            19,
            38,
            39,
            11,
            1,
            32,
            25,
            35,
            8,
            17,
            7,
            9,
            4,
            2,
            34,
            10,
            3,
        ],
        19208,
    ],
    [[1, 2, 3, 5], 6],
    [[1, 2, 3, 5, 8, 9, 10, 12], 18],
    [[3, 4, 5, 6], 4],
    [[3, 4, 5, 7], 3],
    [[1, 2, 3, 4], 7],
    [[1, 2, 3, 4, 5], 13],
    [[3, 4, 5, 7, 8, 9, 11], 13],
    [[3, 4, 5, 7, 9, 10, 11], 9],
    [[3, 6], 1],
    [[3, 4, 6], 2],
]


def main(number_lines: List[int]):
    """
    To find a solution, imagine that you have 5 adapters with outputs of [1, 2, 3, 4, 5] jolts
     and a wall socket with 0 jolts output.
    To connect 1-jolt adapter to the wall according to the rules you have only 1 option - direct connection.
    To connect 2-jolt adapter to the wall you have 2 options - 1-jolt adapter or a direct connection.
    To connect 3-jolt adapter to the wall you have 4 options - 2 ways to connect through 2-jolt adapter,
     1 way through 1-jolt adapter or a direct connection.
    To connect 4-jolt adapter your choice is only through 3-, 2-, or 1- jolt adapters.
    Direct connection has incorrect input parameters.
    That means that you have 4 + 2 + 1 options to connect 4 jolt adapter to the wall.
    The same with 5-jolt adapter - only through 4-, 3-, 2- adapters, and so on and so on.

    If your personal input doesn't have some specific adapters - that's okay,
     that means you just have zero options of connecting through them.
    According to the rules you always will have at least one of 3 adapters needed anyway.

    Written this way the puzzle is pretty straightforward.
    """
    numbers = sorted(number_lines)
    combination_count = {0: 1}  # initial connect option - direct connection
    for num in numbers:
        combination_count[num] = 0
        combination_count[num] += combination_count.get(num - 1, 0)
        combination_count[num] += combination_count.get(num - 2, 0)
        combination_count[num] += combination_count.get(num - 3, 0)

    return combination_count[numbers[-1]]


def test():
    errors = False
    for input, test_result in data:
        result = main(input)

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
        with open("task10_1.input") as f:
            print(main([int(line.strip()) for line in f.readlines()]))
