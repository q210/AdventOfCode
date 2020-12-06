"""
--- Part Two ---

As you finish the last group's customs declaration, you notice that you misread one word in the instructions:

You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which everyone answered "yes"!

Using the same example as above:

abc

a
b
c

ab
ac

a
a
a
a

b
This list represents answers from five groups:

In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
In the second group, there is no question to which everyone answered "yes".
In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c, they don't count.
In the fourth group, everyone answered yes to only 1 question, a.
In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.

For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?
"""
import sys
from collections import Counter
from functools import reduce

DEBUG = False
data = [
    [
        """abcx
abcy
abcz""",
        3,
    ],
    [
        """abc

a
b
c

ab
ac

a
a
a
a

b""",
        6,
    ],
]


def main(groups_data):
    to_group_uniq = lambda acc, person_choice: set(person_choice) if acc is None else set(person_choice) & acc
    calc_group_uniq_count = lambda group: len(reduce(to_group_uniq, group.split("\n"), None))

    return sum(map(calc_group_uniq_count, groups_data))


def test():
    errors = False
    for input, test_result in data:
        result = main(input.split("\n\n"))

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
        with open("task6_1.input") as f:
            print(main(f.read().split("\n\n")))
