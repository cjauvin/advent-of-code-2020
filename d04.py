import re

s = """
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
"""

s = s.split("\n\n")

s = open("d04.txt").read().split("\n\n")

fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}

n_valid = 0
for r in s:
    xs = set(re.findall("(\w+):(?:[\w#]+)", r))
    d = fields - xs
    if d in (set(), {"cid"}):
        n_valid += 1

print(n_valid)
