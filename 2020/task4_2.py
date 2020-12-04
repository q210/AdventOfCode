"""
--- Part Two ---

The line is moving more quickly now, but you overhear airport security talking about how passports with invalid data are getting through. Better add some data validation, quick!

You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.
Your job is to count the passports where all required fields are both present and valid according to the above rules. Here are some example values:

byr valid:   2002
byr invalid: 2003

hgt valid:   60in
hgt valid:   190cm
hgt invalid: 190in
hgt invalid: 190

hcl valid:   #123abc
hcl invalid: #123abz
hcl invalid: 123abc

ecl valid:   brn
ecl invalid: wat

pid valid:   000000001
pid invalid: 0123456789
Here are some invalid passports:

eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
Here are some valid passports:

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
Count the number of valid passports - those that have all required fields and valid values. Continue to treat cid as optional. In your batch file, how many passports are valid?
"""
import re
import sys
from collections import Counter

DEBUG = False
data = [
    [
        """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""",
        2,
    ],
    [
        """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017

iyr:2013 ecl:amb pid:028048884
hcl:#cfa07d byr:1929""",
        0,
    ],
    [
        """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm""",
        1,
    ],
    [
        """hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in byr:1931""",
        1,
    ],
    [
        """hgt:68in
byr:1933
iyr:2010 ecl:brn
pid:380075958
hcl:#623a2f cid:279
eyr:2025""",
        1,
    ],
    [
        """hgt:68in
byr:1933
iyr:2010 
ecl:brn
pid:380075958
hcl:#623a2f
eyr:2025""",
        1,
    ],
    [
        """byr:2021 ecl:grn pid:9284377919 iyr:2011 hgt:75cm hcl:#18171d eyr:2026
        
ecl:oth
byr:1926
hgt:63 iyr:1948 cid:61 hcl:a528d1 eyr:2034""",
        0,
    ],
    [
        """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007""",
        0,
    ],
    [
        """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""",
        4,
    ],
]

valid_ecl = set("amb blu brn gry grn hzl oth".split(" "))

validation = {
    "byr": lambda val: 1920 <= int(val) <= 2002,
    "iyr": lambda val: 2010 <= int(val) <= 2020,
    "eyr": lambda val: 2020 <= int(val) <= 2030,
    "hgt": lambda val: (150 <= int(val[:-2]) <= 193) if val.endswith("cm") else (59 <= int(val[:-2]) <= 76),
    "hcl": lambda val: (int(val[1:], 16) or True) if val.startswith("#") else False,
    "ecl": lambda val: val in valid_ecl,
    "pid": lambda val: re.fullmatch("\d{9}", val),
    "cid": lambda val: True,
}


def parse_keys(passport):
    """
    Return all keys with valid values from password data
    """
    value_pairs = passport.replace("\n", " ").split(" ")
    keys = set()
    for pair in value_pairs:
        if not pair:
            continue

        key, value = pair.split(":")
        key = key.strip()
        value = value.strip()

        try:
            if not validation[key](value):
                return []
        except ValueError:
            return []

        keys.add(key)

    return keys


def main(passports):
    valid_num = 0
    for passport in passports:
        keys = parse_keys(passport)

        if len(keys) == 8 or (len(keys) == 7 and "cid" not in keys):
            valid_num += 1

    print("total", len(passports))
    return valid_num


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
        with open("task4_1.input") as f:
            print(main(f.read().split("\n\n")))
