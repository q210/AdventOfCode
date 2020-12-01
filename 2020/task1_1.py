"""
To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
"""
import sys

DEBUG = False
data = [
    [
        """1721
979
366
299
675
1456""",
        514579,
    ],
    ["2020", 0],
]


def main(list_of_number_strings, limit=2020):
    numbers = [int(num_str.strip()) for num_str in list_of_number_strings if num_str]

    expected = set()
    for number in numbers:
        if number > limit:
            continue

        if number == limit:
            return 0

        elif number in expected:
            return number * (limit - number)

        expected.add(limit - number)

    return 0


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
        with open("task1_1.input") as f:
            print(main(f.readlines()))
