from collections import defaultdict

s = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

# s = """
# .......#.
# ...#.....
# .#.......
# .........
# ..#L....#
# ....#....
# .........
# #........
# ...#.....
# """

# s = """
# .............
# .L.L.#.#.#.#.
# .............
# """

# s = """
# .##.##.
# #.#.#.#
# ##...##
# ...L...
# ##...##
# #.#.#.#
# .##.##.
# """

# s = """
# #.LL.LL.L#
# #LLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLLL.L
# #.LLLLL.L#
# """

s = open("d11.txt").read()

g = s.strip().split("\n")
h = len(g)
w = len(g[0])

d = defaultdict(lambda: ".")
for i in range(h):
    for j in range(w):
        d[(i, j)] = g[i][j]


def n_adj_occupied(d, i, j):
    n = 0
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            if a == 0 and b == 0:
                continue
            n += d[(i + a, j + b)] == "#"
    return n


def n_occupied_radial(d, i, j):
    n = 0
    for q in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        p = (i, j)
        while True:
            p = (p[0] + q[0], p[1] + q[1])
            seat = d[p] in ["#", "L"]
            if seat or p[0] < 0 or p[0] >= h or p[1] < 0 or p[1] >= w:
                break
        n += d[p] == "#"
    return n


# assert d[(4, 3)] == "L"
# assert n_occupied_radial(d, 4, 3) == 8

# assert d[(1, 1)] == "L"
# assert n_occupied_radial(d, 1, 1) == 1

# assert d[(3, 3)] == "L"
# assert n_occupied_radial(d, 3, 3) == 0

# assert d[(0, 3)] == "L"
# assert n_occupied_radial(d, 0, 3) == 0

changed = True
while changed:

    print(sum(d[(i, j)] == "#" for j in range(w) for i in range(h)))

    e = defaultdict(lambda: ".")
    changed = False
    for i in range(h):
        for j in range(w):
            # n = n_adj_occupied(d, i, j)
            n = n_occupied_radial(d, i, j)
            if d[(i, j)] == "L" and n == 0:
                e[(i, j)] = "#"
                changed = True
            elif d[(i, j)] == "#" and n >= 5:
                e[(i, j)] = "L"
                changed = True
            else:
                e[(i, j)] = d[(i, j)]
    d = e

    print("\n" + "\n".join(["".join(d[(i, j)] for j in range(w)) for i in range(h)]))
