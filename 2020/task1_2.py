"""
The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria as in task1_1.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?
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
        241861950,
    ],
    ["2020", 0],
    ["""1
1930
80
20
10
5""", 1544000]
]


def main(list_of_number_strings, limit=2020):
    numbers = [int(num_str.strip()) for num_str in list_of_number_strings if num_str]

    expected = {}
    for index, number in enumerate(numbers):
        if number > limit:
            continue

        if number == limit:
            return 0

        elif number in expected:
            return number * (limit - number - expected[number][0]) * (limit - number - expected[number][1])

        j = index - 1
        while index > 0 and j >= 0:
            option_in_list = numbers[j]
            if number + option_in_list > limit:
                j -= 1
                continue

            expected_in_list = limit - number - option_in_list
            expected[expected_in_list] = [number, option_in_list]
            expected[option_in_list] = [number, expected_in_list]
            print('base:', number, ', option in list:', option_in_list, ', expecting in list:', expected_in_list)
            j -= 1

    return 0


def test():
    errors = False
    for input, test_result in data:
        result = main(input.split('\n'))

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
