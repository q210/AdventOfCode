"""
--- Day 4: Passport Processing ---

You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport. While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't actually valid documentation for travel in most of the world.

It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport scanners, and the delay could upset your travel itinerary.

Due to some questionable network security, you realize you might be able to solve both of these problems at the same time.

The automatic passport scanners are slow because they're having trouble detecting which passports have all required fields. The expected fields are as follows:

byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the Height field).

The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat this "passport" as valid.

The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so this passport is invalid.

According to the above rules, your improved system would report 2 valid passports.

Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?
"""
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
cid:279
eyr:2025""",
        0,
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
]


def main(passports):
    valid_num = 0
    for passport in passports:
        value_pairs = passport.replace("\n", " ").split(" ")
        keys = {pair.split(":")[0].strip() for pair in value_pairs}

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
