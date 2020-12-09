"""
--- Day 9: Encoding Error ---

With your neighbor happily enjoying their video game, you turn your attention to an open data port on the little screen in the seat in front of you.

Though the port is non-standard, you manage to connect it to your computer through the clever use of several paperclips. Upon connection, the port outputs a series of numbers (your puzzle input).

The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, conveniently for you, is an old cypher with an important weakness.

XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one such pair.

For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be valid, the next number must be the sum of two of those numbers:

26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
49 would be a valid next number, as it is the sum of 24 and 25.
100 would not be valid; no two of the previous 25 numbers sum to 100.
50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.
Suppose the 26th number is 45, and the first number (no longer an option, as it is more than 25 numbers ago) was 20. Now, for the next number to be valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that add up to it:

26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
65 would not be valid, as no two of the available numbers sum to it.
64 and 66 would both be valid, as they are the result of 19+45 and 21+45 respectively.
Here is a larger example which only considers the previous 5 numbers (and has a preamble of length 5):

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
In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; the only number that does not follow this rule is 127.

The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?
"""
import sys
from collections import defaultdict
from itertools import combinations, islice
from typing import Set, List, Dict, Iterable, Tuple, Generator

DEBUG = False
data = [
    [
        (
            3,
            """1
2
3
4
101""",
        ),
        101,
    ],
    [
        (
            5,
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
        127,
    ],
]


def generate_initial_options(numbers: Iterable[int], window_size: int) -> Tuple[List[int], Dict[int, int]]:
    """
    Generate initial window of first {window_size} numbers and calculate sums of all their combinations
    """
    options = defaultdict(int)
    window = list(islice(numbers, window_size))
    for a, b in combinations(window, r=2):
        summ = a + b
        options[summ] += 1

    return window, options


def shift_window(window: List[int], options: Dict[int, int], new_num: int):
    """
    Shift window right, remove all sums from options that were result of excluded element, add new number to window
    """
    to_exclude = window[0]
    window = window[1:]
    for num in window:
        options[to_exclude + num] -= 1
        options[new_num + num] += 1

    window.append(new_num)
    return window, options


def main(number_lines: Generator[str, None, None], window_size=25):
    window, options = generate_initial_options(map(int, number_lines), window_size)
    while True:
        candidate = int(next(number_lines))
        if options[candidate] < 1:
            return candidate

        # candidate is a sum of first {window_size} numbers, checking to the next one
        window, options = shift_window(window, options, candidate)


def test():
    errors = False
    for (window_size, input), test_result in data:
        result = main(iter(input.split("\n")), window_size)

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
