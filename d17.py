from collections import defaultdict

s = """
.#.
..#
###
"""

s = """
#...#.#.
..#.#.##
..#..#..
.....###
...#.#.#
#.#.##..
#####...
.#.#.##.
"""

s = s.strip().split("\n")


# def n_active(g, p):
#     n = 0
#     for i in [-1, 0, 1]:
#         for j in [-1, 0, 1]:
#             for k in [-1, 0, 1]:
#                 if (i, j, k) == (0, 0, 0):
#                     continue
#                 n += g[(p[0] + i, p[1] + j, p[2] + k)] == "#"
#     return n


# def prn(g, k):
#     lines = []
#     for i in range(3):
#         lines.append("".join(g[(i, j, k)] for j in range(3)))
#     print("\n" + "\n".join(lines))


# size = len(s)

# g = defaultdict(lambda: ".")
# for i in range(size):
#     for j in range(size):
#         g[(i, j, 0)] = s[i][j]

# # prn(g, 0)
# # print(n_active(g, (0, 0, 0)))

# print(sum([1 for v in g.values() if v == "#"]))

# for _ in range(6):

#     size += 1

#     h = defaultdict(lambda: ".")
#     for i in range(-size, size):
#         for j in range(-size, size):
#             for k in range(-size, size):
#                 p = (i, j, k)
#                 n = n_active(g, p)
#                 # print(f"{p=}, {n=}")
#                 if g[p] == "#":
#                     h[p] = "#" if n in [2, 3] else "."
#                 else:
#                     h[p] = "#" if n == 3 else "."
#                 # print(f"{p=}, {n=}, {g[p]} -> {h[p]}")

#     g = h

#     print(sum([1 for v in g.values() if v == "#"]))


def n_active(g, p):
    n = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                for l in [-1, 0, 1]:
                    if (i, j, k, l) != (0, 0, 0, 0) and g[
                        (p[0] + i, p[1] + j, p[2] + k, p[3] + l)
                    ] == "#":
                        n += 1
    return n


size = len(s)

g = defaultdict(lambda: ".")
for i in range(size):
    for j in range(size):
        g[(i, j, 0, 0)] = s[i][j]


print(sum([1 for v in g.values() if v == "#"]))

for _ in range(6):

    size += 1

    h = defaultdict(lambda: ".")
    for i in range(-size, size):
        for j in range(-size, size):
            for k in range(-size, size):
                for l in range(-size, size):
                    p = (i, j, k, l)
                    n = n_active(g, p)
                    if g[p] == "#":
                        h[p] = "#" if n in [2, 3] else "."
                    else:
                        h[p] = "#" if n == 3 else "."

    g = h

    print(sum([1 for v in g.values() if v == "#"]))
