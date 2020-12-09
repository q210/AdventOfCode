"""
--- Part Two ---

The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.

Again consider the above example:

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
In this list, adding up all of the numbers from 15 through 40 produces the invalid number from step 1, 127. (Of course, the contiguous set of numbers in your actual list might be much longer.)

To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example, these are 15 and 47, producing 62.

What is the encryption weakness in your XMAS-encrypted list of numbers?
"""
import sys
from collections import defaultdict
from itertools import combinations, islice
from typing import Set, List, Dict, Iterable, Tuple, Generator

DEBUG = False
data = [
    [
        (
            108,
            """1
2
3
4
101
102""",
        ),
        104,
    ],
    [
        (
            127,
            """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""",
        ),
        62,
    ],
]


def shrink_candidates(candidates: List[int], current_sum: int, target_sum: int):
    for index, num in enumerate(candidates):
        current_sum -= num
        if current_sum <= target_sum:
            return candidates[index + 1 :], current_sum

    raise RuntimeError


def main(number_lines: Generator[str, None, None], target_sum=29221323):
    current_sum = 0
    candidates = []
    for num in map(int, number_lines):
        candidates.append(num)
        current_sum += num
        # print(candidates, current_sum, target_sum)

        if current_sum > target_sum:
            # need to shrink candidates window from the left side, cause right now their sum is too much
            candidates, current_sum = shrink_candidates(candidates, current_sum, target_sum)

        if current_sum == target_sum:
            # this is enough
            candidates = sorted(candidates)
            return candidates[0] + candidates[-1]


def test():
    errors = False
    for (target_sum, input), test_result in data:
        result = main(iter(input.split("\n")), target_sum)

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
        with open("task9_1.input") as f:
            print(main((line.strip() for line in f.readlines())))
