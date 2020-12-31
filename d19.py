import re
import sys

s = """
0: 8 11
1: "a"
2: 1 24 | 14 4
3: 5 14 | 16 1
4: 1 1
5: 1 14 | 15 1
6: 14 14 | 1 14
7: 14 5 | 1 21
8: 42 8 | 42
9: 14 27 | 1 26
10: 23 14 | 28 1
11: 42 31 # | 42 11 31
12: 24 14 | 19 1
13: 14 3 | 1 12
14: "b"
15: 1 | 14
16: 15 1 | 14 14
17: 14 2 | 1 7
18: 15 15
19: 14 1 | 14 14
20: 14 14 | 1 15
21: 14 1 | 1 14
22: 14 14
23: 25 1 | 22 14
24: 14 1
25: 1 1 | 1 14
26: 14 22 | 1 20
27: 1 6 | 14 18
28: 16 1
31: 14 17 | 1 13
42: 9 14 | 10 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""


# s = """
# 0: 4 1 5
# 1: 2 3 | 3 2
# 2: 4 4 | 5 5
# 3: 4 5 | 5 4
# 4: "a"
# 5: "b"
# """

s = open("d19.txt").read()


rules = {}
inputs = []

for line in s.strip().split("\n"):
    line = line.strip()
    if not line:
        continue
    if ":" in line:
        m1 = re.match("(\\d+): ([^#]+)", line)
        h = int(m1.group(1))  # head
        t = m1.group(2)  # tail
        if m2 := re.match('"(.)"', t):
            rules[h] = m2.group(1)
        else:
            # set of tuples
            rules[h] = tuple(
                tuple(int(x) for x in c.split()) for c in t.split("|")
            )  # c for clause
    else:
        if line[0] != "#":
            inputs.append(line)


def parse_tail(seq, t):
    """
    t: char or list of clauses
    """
    if isinstance(t, str):
        return t if seq[0] == t else None
    else:
        # One of these must match (OR)
        for c in t:
            res = parse_clause(seq, c)
            if res:
                # print(c, res)
                return res
        return None


def parse_clause(seq, c):
    """
    c: list of heads
    """
    # All of these must match (AND)
    res = ""
    for h in c:
        new_res = parse_tail(seq[len(res) :], rules[h])
        if new_res:
            res += new_res
        else:
            res = None
            break
    return res


def is_valid(seq):
    res = parse_tail(seq, rules[0])
    return bool(res and len(res) == len(seq))


def generate(h):
    def expand(x, h, c):
        y = []
        found = False
        for hh in x:
            if hh == h and not found:
                y += list(c)
                found = True
            else:
                y.append(hh)
        return tuple(y)

    out = rules[h]

    while True:
        out2 = []
        for x in out:
            found = False
            for h in x:
                t = rules[h]
                if not isinstance(t, str):
                    found = True
                    break
            if found:
                for c in t:
                    y = expand(x, h, c)
                    out2.append(y)
            else:
                out2.append(x)
        if out == out2:
            break
        # print(".", end="", flush=True)
        out = out2

    return {"".join(rules[h] for h in x) for x in out}


# valid = generate(0)

tokens_31 = generate(31)
tokens_42 = generate(42)
# tokens_27 = generate(27)
# tokens_18 = generate(18)

# print()
# print(len(valid))
#
# print(sum(i in valid for i in inputs))

# print()
# for s in valid:
#     print(s)

# for s in valid:
#     assert is_valid(s)


def match_special(x):
    tokens = {42: {"tokens": tokens_42, "n": 0}, 31: {"tokens": tokens_31, "n": 0}}
    i = 0
    for tid in (42, 31):
        while True:
            found = False
            for t in tokens[tid]["tokens"]:
                if t == x[i : i + len(t)]:
                    found = True
                    i += len(t)
                    tokens[tid]["n"] += 1
                    break
            if not found:
                break

    return i == len(x) and tokens[31]["n"] > 0 and tokens[42]["n"] > tokens[31]["n"]


# x = "babbbbaabbbbbabbbbbbaabaaabaaa"
# print(match_special(x))
# print(is_valid(x))
# x = "babbbbaabbbbbbb"

print(sum(match_special(i) for i in inputs))

# match_special("aaabbbbbbaaaabaababaabababbabaaabbababababaaa")
