import re

import numpy as np

with open("d20_test.txt") as f:
    # with open("d20.txt") as f:
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


def get_sides(a):
    return set(map(tuple, [a[0, :], a[-1, :], a[:, 0], a[:, -1]]))


def get_variants(a):
    return (a, np.fliplr(a), np.flipud(a))
    vs = [a]
    # for _ in range(1):
    for _ in range(3):
        a = np.rot90(a)
        vs.append(a)
        # a = np.flipud(a)
        # vs.append(a)
    return vs


def get_variant_sides(a):
    sides = set()
    # sides |= get_sides(a)
    sides |= get_sides(np.fliplr(a))
    sides |= get_sides(np.flipud(a))
    # for _ in range(2):
    #     for i in range(3):
    #         a = np.rot90(a)
    #         sides |= get_sides(a)
    #     a = np.flipud(a)
    #     sides |= get_sides(a)
    return sides


def part1():
    n = 1
    for tid, tile in tiles.items():
        n_unique = 0
        for s in get_variant_sides(tile):
            for tid2, tile2 in tiles.items():
                if tid == tid2:
                    continue
                if s in get_variant_sides(tile2):
                    break
            else:
                n_unique += 1
        if n_unique == 4:
            print(tid, n_unique)
            n *= tid
    return n


# print(part1())


def find_2_on_right(tid):
    for a in get_variants(tiles[tid]):
        a_right = tuple(a[:, -1])
        for tid2, tile2 in tiles.items():
            if tid2 == tid:
                continue
            for b in get_variants(tile2):
                b_left = tuple(b[:, 0])
                b_right = tuple(b[:, -1])
                if a_right == b_left:
                    for tid3, tile3 in tiles.items():
                        if tid2 == tid3 or tid == tid3:
                            continue
                        for c in get_variants(tile3):
                            c_left = tuple(c[:, 0])
                            if b_right == c_left:
                                # print(tid, tid2, tid3)
                                return (tid, tid2, tid3)
    return None


# tid = 2473
# tile = tiles[tid]
# neighbors = set()
# for s in get_variant_sides(tile):
#     for tid2, tile2 in tiles.items():
#         if tid2 == tid:
#             continue
#         if s in get_variant_sides(tile2):
#             neighbors.add(tid2)
# print(neighbors)

# find_2_on_right(1951)
# find_2_on_right(2729)
# find_2_on_right(2971)
# print(find_2_on_right(3079))

for tid, tile in tiles.items():
    if t := find_2_on_right(tid):
        print(t)
