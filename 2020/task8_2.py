"""
--- Part Two ---

After some careful analysis, you believe that exactly one instruction is corrupted.

Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions were harmed in the corruption of this boot code.)

The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

For example, consider the same program from above:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find another jmp instruction and loop forever.

However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions are visited in this order:

nop +0  | 1
acc +1  | 2
jmp +4  | 3
acc +3  |
jmp -3  |
acc -99 |
acc +1  | 4
nop -4  | 5
acc +6  | 6
After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).

Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
"""
import sys
from collections import defaultdict

DEBUG = False
data = [
    [
        """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""",
        8,
    ],
    [
        """acc +1
nop +0
acc +1
jmp -2""",
        2,
    ],
    [
        """acc +1
nop +0
acc +1
jmp +4
acc +100
jmp +2
jmp -1
acc +3
jmp -1""",
        5,
    ],
]

# <instruction code> : (<instruction value>, <current accumulator>, <current instruction index>) -> (<new instruction index>, <new accumulator>, <potentially instruction swapped from nop to jmp and it's impact>)
rules = {
    "acc": lambda value, acc, cursor: (cursor + 1, acc + value, None),
    "jmp": lambda value, acc, cursor: (cursor + value, acc, (cursor, -1 * value, f"nop {value}", acc)),
    "nop": lambda value, acc, cursor: (cursor + 1, acc, (cursor, value, f"jmp {value}", acc)),
}


def process(instructions, cursor=0, acc=0):
    processed = set()
    potentials = []
    while cursor not in processed:
        if cursor == len(instructions):
            # finishing after all instructions are processed
            return True, acc, []

        instruction, value = instructions[cursor].split(" ")
        processed.add(cursor)
        # print(cursor, instructions[cursor])
        cursor, acc, potential = rules[instruction](int(value), acc, cursor)
        if potential:
            # potential for swap - a nop or jump
            potentials.append(potential)

    # found a loop, returning potentials for swap sorted by impact (how much instructions swap will allow us to skip)
    return False, acc, sorted(potentials, key=lambda item: item[1], reverse=True)


def main(instructions):
    # first finding all possible candidates for swapping between nop and jump
    _, _, potentials = process(instructions)
    # then trying out the swaps one at a time
    for index, (cursor_state, new_value, new_instruction, acc_state) in enumerate(potentials):
        original_instruction = instructions[cursor_state]
        instructions[cursor_state] = new_instruction
        success, acc, _ = process(instructions, cursor=cursor_state + 1, acc=acc_state)
        instructions[cursor_state] = original_instruction
        if success:
            # print(index, cursor_state)
            # print(sorted([item[0] for item in potentials], reverse=True))
            return acc

    return None


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
        with open("task8_1.input") as f:
            print(main([line.strip() for line in f.readlines()]))
