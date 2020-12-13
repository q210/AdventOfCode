"""
--- Part Two ---

The shuttle company is running a contest: one gold coin for anyone that can find the earliest timestamp such that the first bus ID departs at that time and each subsequent listed bus ID departs at that subsequent minute. (The first line in your input is no longer relevant.)

For example, suppose you have the same list of bus IDs as above:

7,13,x,x,59,x,31,19
An x in the schedule means there are no constraints on what bus IDs must depart at that time.

This means you are looking for the earliest timestamp (called t) such that:

Bus ID 7 departs at timestamp t.
Bus ID 13 departs one minute after timestamp t.
There are no requirements or restrictions on departures at two or three minutes after timestamp t.
Bus ID 59 departs four minutes after timestamp t.
There are no requirements or restrictions on departures at five minutes after timestamp t.
Bus ID 31 departs six minutes after timestamp t.
Bus ID 19 departs seven minutes after timestamp t.
The only bus departures that matter are the listed bus IDs at their specific offsets from t. Those bus IDs can depart at other times, and other bus IDs can depart at those times. For example, in the list above, because bus ID 19 must depart seven minutes after the timestamp at which bus ID 7 departs, bus ID 7 will always also be departing with bus ID 19 at seven minutes after timestamp t.

In this example, the earliest timestamp at which this occurs is 1068781:

time     bus 7   bus 13  bus 59  bus 31  bus 19
1068773    .       .       .       .       .
1068774    D       .       .       .       .
1068775    .       .       .       .       .
1068776    .       .       .       .       .
1068777    .       .       .       .       .
1068778    .       .       .       .       .
1068779    .       .       .       .       .
1068780    .       .       .       .       .
1068781    D       .       .       .       .
1068782    .       D       .       .       .
1068783    .       .       .       .       .
1068784    .       .       .       .       .
1068785    .       .       D       .       .
1068786    .       .       .       .       .
1068787    .       .       .       D       .
1068788    D       .       .       .       D
1068789    .       .       .       .       .
1068790    .       .       .       .       .
1068791    .       .       .       .       .
1068792    .       .       .       .       .
1068793    .       .       .       .       .
1068794    .       .       .       .       .
1068795    D       D       .       .       .
1068796    .       .       .       .       .
1068797    .       .       .       .       .
In the above example, bus ID 7 departs at timestamp 1068788 (seven minutes after t). This is fine; the only requirement on that minute is that bus ID 19 departs then, and it does.

Here are some other examples:

The earliest timestamp that matches the list 17,x,13,19 is 3417.
67,7,59,61 first occurs at timestamp 754018.
67,x,7,59,61 first occurs at timestamp 779210.
67,7,x,59,61 first occurs at timestamp 1261476.
1789,37,47,1889 first occurs at timestamp 1202161486.
However, with so many bus IDs in your list, surely the actual earliest timestamp will be larger than 100000000000000!

What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list?
"""
import sys
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from itertools import count
from typing import List, Tuple, Set, Optional

DEBUG = False
data = [
    [
        """
939
7,13,x,x,59,x,31,19
""",
        1068781,
    ],
    [
        """
939
17,x,13,19
""",
        3417,
    ],
    [
        """
939
67,7,59,61
""",
        754018,
    ],
    [
        """
939
67,x,7,59,61
""",
        779210,
    ],
    [
        """
939
67,7,x,59,61
""",
        1261476,
    ],
    [
        """
939
1789,37,47,1889
""",
        1202161486,
    ],
]


def main(timestamp_line: str, buses_str: str):
    """
    WARNING: not mine, got this solution from reddit!

    Finding the solution for busses one by one.
    The idea is that once you find a satisfying value for each bus,
    you can then make the step value be the lowest common multiple of its current value and that bus.
    Fortunately the bus numbers were all mutually prime, so we didn't need to implement
    lowest common multiple and could simply multiply the step value.
    """

    buses = [(index, int(bus_id)) for index, bus_id in enumerate(buses_str.split(",")) if bus_id != "x"]
    step = 1
    result = buses[0][1]
    for index, bus_id in buses:
        result = next(c for c in count(result, step) if (c + index) % bus_id == 0)
        step *= bus_id

    return result


def test():
    errors = False
    for input, test_result in data:
        result = main(*input.strip().split("\n"))

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
        with open("task13_1.input") as f:
            print(main(*[line.strip() for line in f.readlines()]))
