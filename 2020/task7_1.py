"""
--- Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)
"""
import sys
from collections import Counter, defaultdict
from functools import reduce

DEBUG = False
data = [
    [
        """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""",
        4,
    ],
    [
        """white bag contain 1 shiny gold bag.
black bag contain 1 blue bag.
yellow bag contain 3 white bags.""",
        2,
    ],
    [
        """white bag contain 1 shiny gold bag.
black bag contain 1 blue bag.
yellow bag contain 3 white bags.
shiny gold bag contain 1 blue bag.
maroon bag contain 1 black bag, 2 white bags.""",
        3,
    ],
]


def main(rules, target_color="shiny gold"):
    rules_map = defaultdict(list)
    for rule in rules:
        root_color, leaves_str = rule.strip(".").replace(" bags", "").replace(" bag", "").split(" contain ")

        if root_color == target_color:
            continue

        if leaves_str == "no other":
            leaves = []
        else:
            leaves = [bag_str.split(" ", 1)[-1] for bag_str in leaves_str.split(", ")]

        for leave_color in leaves:
            rules_map[leave_color].append(root_color)

    result_color_set = set()
    colors_to_check = set(rules_map[target_color])

    while colors_to_check:
        next_colors_to_check = []
        for color in colors_to_check:
            if color in rules_map:
                next_colors_to_check += rules_map[color]

        result_color_set |= colors_to_check
        colors_to_check = set(next_colors_to_check)

    return len(result_color_set)


def test():
    errors = False
    for input, test_result in data:
        result = main(input.split("\n"))

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
        with open("task7_1.input") as f:
            print(main([line.strip() for line in f.readlines()]))
