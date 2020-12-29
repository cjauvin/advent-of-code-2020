import re

s = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""

s = """
0: 2 1 3
1: 2 2 | 3 3
2: "a"
3: "b"
"""

# aaab, abbb


# '123': [('10', '20'), ('30', '40')]
# '124': 'a'
rules = {}

for line in s.strip().split("\n"):
    m1 = re.match("(\d+): (.+)", line)
    h = int(m1.group(1))  # head
    t = m1.group(2)  # tail
    if m2 := re.match('"(.)"', t):
        rules[h] = m2.group(1)
    else:
        rules[h] = [[int(x) for x in c.split()] for c in t.split("|")]  # c for clause


def parse_clause(seq, c):
    """
    c: list of heads
    """

    i = 0
    matched = True
    # All of these must match (AND)
    for h in c:
        print(">", h, parse_tail(seq[i:], rules[h]))
    # for h in c:
    #     b, d = parse_tail(seq[i:], rules[h])
    #     if b:
    #         i += d
    #     else:
    #         matched = False
    #         break
    # return matched


def parse_tail(seq, t):
    """
    t: char or list of clauses
    """
    if isinstance(t, str):
        return seq[0] == t, 1
    else:
        # One of these must match (OR)
        for c in t:
            parse_clause(seq, c)
            break


parse_tail("aaab", rules[0])

# def generate(t, prefix=""):
#     if isinstance(t, str):
#         print(f"t: {t}")
#         # return t
#         words.add(prefix + t)
#         return t
#     else:
#         for c in t:
#             print(f"clause: {c}")
#             # word = ""
#             # h in [4, 1, 5]

#             for h in c:
#                 print(f"h: {h}")
#                 res = generate(rules[h], prefix)
#             # print(word)


# parse("ababbb", rules["0"])

# 0: [4, 1, 5]
# print(generate(rules["0"]))

print()
