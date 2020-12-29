import math

s = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".strip()

g = [l.strip() for l in open("/home/christian/m/aoc2020/d03.txt").readlines()]

w = len(g[0])


def n_trees(r, d):
    j = 0
    n = 0
    for i in range(0, len(g), d):
        n += g[i][j % w] == "#"
        j += r
    return n


# Part 1
print(n_trees(3, 1))

# Part 2
print(math.prod(n_trees(r, d) for r, d in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]))
