"""
--- Part Two ---

For some reason, the sea port's computer system still can't communicate with your ferry's docking program. It must be using version 2 of the decoder chip!

A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts as a memory address decoder. Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the destination memory address in the following way:

If the bitmask bit is 0, the corresponding memory address bit is unchanged.
If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
If the bitmask bit is X, the corresponding memory address bit is floating.
A floating bit is not connected to anything and instead fluctuates unpredictably. In practice, this means the floating bits will take on all possible values, potentially causing many memory addresses to be written all at once!

For example, consider the following program:

mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
When this program goes to write to memory address 42, it first applies the bitmask:

address: 000000000000000000000000000000101010  (decimal 42)
mask:    000000000000000000000000000000X1001X
result:  000000000000000000000000000000X1101X
After applying the mask, four bits are overwritten, three of which are different, and two of which are floating. Floating bits take on every possible combination of values; with two floating bits, four actual memory addresses are written:

000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
000000000000000000000000000000111010  (decimal 58)
000000000000000000000000000000111011  (decimal 59)
Next, the program is about to write to memory address 26 with a different bitmask:

address: 000000000000000000000000000000011010  (decimal 26)
mask:    00000000000000000000000000000000X0XX
result:  00000000000000000000000000000001X0XX
This results in an address with three floating bits, causing writes to eight memory addresses:

000000000000000000000000000000010000  (decimal 16)
000000000000000000000000000000010001  (decimal 17)
000000000000000000000000000000010010  (decimal 18)
000000000000000000000000000000010011  (decimal 19)
000000000000000000000000000000011000  (decimal 24)
000000000000000000000000000000011001  (decimal 25)
000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
The entire 36-bit address space still begins initialized to the value 0 at every address, and you still need the sum of all values left in memory at the end of the program. In this example, the sum is 208.

Execute the initialization program using an emulator for a version 2 decoder chip. What is the sum of all values left in memory after it completes?
"""
import sys
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple, Set, Optional, Generator

DEBUG = False
data = [
    [
        """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""",
        208,
    ]
]


def all_addrs(mask_template: str, addr: int):
    x_number = 0
    mask_map = {}
    addr = list("0" * (len(mask_template) - addr.bit_length()) + "{0:b}".format(addr))[::-1]
    print(mask_template)
    print("".join(addr))
    for index, mask_bit in enumerate(mask_template[::-1]):
        if mask_bit == "1":
            addr[index] = "1"

        elif mask_bit == "X":
            addr[index] = "0"
            mask_map[x_number] = index
            x_number += 1

    combinations_num = 2 ** Counter(mask_template)["X"]
    addr = int("".join(addr[::-1]), 2)
    for combination in range(combinations_num):
        addr_variant = addr
        for index, bit in enumerate("{0:b}".format(combination)[::-1]):
            if bit == "1":
                addr_variant += 2 ** mask_map[index]

        yield addr_variant


def instructions(lines):
    mask = "X"
    for line in lines:
        lh, rh = line.split(" = ")
        if lh == "mask":
            mask = rh

        else:
            addr = lh[4:-1]
            for addr in all_addrs(mask, int(addr)):
                yield addr, int(rh)


def main(lines: Generator[str, None, None]):
    data = {}
    for addr, value in instructions(lines):
        data[addr] = value
        print("addr: {addr}, value: {value}".format(addr=addr, value=value))

    return sum(data.values())


def test():
    errors = False
    for input, test_result in data:
        result = main((line for line in input.strip().split("\n")))

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
        with open("task14_1.input") as f:
            print(main((line.strip() for line in f.readlines())))
