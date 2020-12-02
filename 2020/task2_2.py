"""
--- Part Two ---

While it appears you validated the passwords correctly, they don't seem to be what the Official Toboggan Corporate Authentication System is expecting.

The shopkeeper suddenly realizes that he just accidentally explained the password policy rules from his old job at the sled rental place down the street! The Official Toboggan Corporate Policy actually works a little differently.

Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy enforcement.

Given the same example list from above:

1-3 a: abcde is valid: position 1 contains a and position 3 does not.
1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
How many passwords are valid according to the new interpretation of the policies?
"""
import sys
from collections import Counter

DEBUG = False
data = [
    [
        """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""",
        1,
    ],
    ["2-3 d: add", 0],
    [
        """1-3 d: qwe
4-5 a: abcawawa
2-4 r: qwrrrqqqrqrq
1-3 w: www
2-4 y: awyaxya
2-4 b: abcb
2-4 a: abca""",
        3,
    ],
]


def main(lines):
    valid_passwords_num = 0
    for line in lines:
        count_str, letter_dirty, password = line.strip().split(" ")
        letter = letter_dirty[0]
        first_index, second_index = count_str.split("-")

        if (password[int(first_index) - 1] == letter) != (password[int(second_index) - 1] == letter):
            valid_passwords_num += 1

        print(
            f"password: {password}, "
            f"policy: {first_index}-{second_index} {letter}, "
            f"first occ: {password[int(first_index) - 1] == letter}, "
            f"second occ {password[int(second_index) - 1] == letter}"
        )

    return valid_passwords_num


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
        with open("task2_1.input") as f:
            print(main(f.readlines()))
