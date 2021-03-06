"""
--- Part Two ---

Ding! The "fasten seat belt" signs have turned on. Time to find your seat.

It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.

Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

What is the ID of your seat?
"""
import sys
from collections import Counter

DEBUG = False
data = []


def main(boarding_passes):
    min_num = None
    max_num = 0
    summ = 0
    for bpass in boarding_passes:
        bpass = bpass.strip()
        row_num = int(bpass[:7].replace("B", "1").replace("F", "0"), 2)
        col_num = int(bpass[7:].replace("R", "1").replace("L", "0"), 2)

        result = row_num * 8 + col_num
        if result > max_num:
            max_num = result

        if min_num is None or result < min_num:
            min_num = result

        summ += result

    return (max_num - min_num + 1) * (max_num + min_num) / 2 - summ


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
        with open("task5_1.input") as f:
            print(main(f.readlines()))
