import re
from collections import Counter

s = [l.strip() for l in open("/home/christian/m/aoc2020/d02.txt").readlines()]


def is_valid(s):
    a, b, c, p = re.match("(\d+)-(\d+) (.+): (.+)", s).groups()
    return int(a) <= Counter(p)[c] <= int(b)


def is_valid2(s):
    a, b, c, p = re.match("(\d+)-(\d+) (.+): (.+)", s).groups()
    return (p[int(a) - 1] == c) + (p[int(b) - 1] == c) == 1


assert is_valid("1-3 a: abcde")
assert not is_valid("1-3 b: cdefg")
assert is_valid("2-9 c: ccccccccc")


p1 = sum(is_valid(x) for x in s)

assert is_valid2("1-3 a: abcde")
assert not is_valid2("1-3 b: cdefg")
assert not is_valid2("2-9 c: ccccccccc")

p2 = sum(is_valid2(x) for x in s)

print(p1, p2)
