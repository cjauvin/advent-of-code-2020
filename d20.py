import re

import numpy as np

with open("d20_test.txt") as f:
    s = f.read().split("\n")

tiles = {}
for line in s:
    if m := re.match("Tile (\d+):", line):
        curr = int(m.group(1))
        tiles[curr] = []
    elif line:
        tiles[curr].append(line)

for tid, tile in tiles.items():
    tiles[tid] = np.asarray([list(row) for row in tile])


def get_variants(a):
    b = []
    for _ in range(2):
        for i in range(3):
            a = np.rot90(a)
            b.append(a)
        a = np.flipud(a)
        b.append(a)
    return b


def get_sides(a):
    return a[0, :], a[-1, :], a[:, 0], a[:, -1]


def get_variant_sides(a):
    s = set()
    for r in [a[0, :], a[-1, :], a[:, 0], a[:, -1]]:
        s.add(tuple(r))
    for _ in range(2):
        for i in range(3):
            a = np.rot90(a)
            for r in [a[0, :], a[-1, :], a[:, 0], a[:, -1]]:
                s.add(tuple(r))
        a = np.flipud(a)
        for r in [a[0, :], a[-1, :], a[:, 0], a[:, -1]]:
            s.add(tuple(r))
    return s


rows = set()


for tid, tile in tiles.items():
    for a in get_variants(tile):
        for r in get_sides(a):
            rows.add(tuple(r))
    # s = {tuple(a.reshape(100)) for a in get_variants(tile)}
    # print(len(s))

for tid, tile in tiles.items():
    n_unique = 0
    for r in get_variant_sides(tile):
        found = False
        for tid2, tile2 in tiles.items():
            if tid == tid2:
                continue
            for r2 in get_variant_sides(tile2):
                if r == r2:
                    found = True
                    break
            if found:
                break
        if not found:
            n_unique += 1
    print(tid, n_unique)
