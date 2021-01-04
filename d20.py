import re

import numpy as np

# with open("d20_test.txt") as f:
with open("d20.txt") as f:
    s = f.read().split("\n")

monster_s = """
                  #
#    ##    ##    ###
 #  #  #  #  #  #
"""
monster = []
for i, line in enumerate(monster_s.strip("\n").split("\n")):
    for j, c in enumerate(line):
        if c == "#":
            monster.append((i, j))

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
    # return [np.fliplr(a), np.flipud(a)]
    vs = [a]
    for i in range(2):
        for _ in range(3):
            a = np.rot90(a)
            vs.append(a)
        if i == 0:
            a = np.fliplr(a)
            vs.append(a)
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


def search_for_monster(a, b, c):

    d = np.hstack((a[1:9, 1:9], b[1:9, 1:9], c[1:9, 1:9]))
    assert d.shape == (8, 24)
    # monster rect is 3 x 20
    for i in range(5):  # 8 - 3
        for j in range(4):  # 24 - 20
            mcs = {d[mi + i, mj + j] for mi, mj in monster}
            # print(mcs)
            if mcs == {"#"}:
                n = d[d == "#"].size
                return n - len(monster)
    return 0


def find_2_on_right(tid):
    # ts = set()
    ts = []
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
                                # if (tid, tid2, tid3) == (1951, 2311, 3079):
                                #     print(search_for_monster(a, b, c))
                                # ts.add((tid, tid2, tid3))
                                # ts.append((a, b, c))
                                ts.append({tid: a, tid2: b, tid3: c})
    return ts


print()

monster_tids = set()
total = 0

for tid, tile in tiles.items():
    for t in find_2_on_right(tid):
        if n := search_for_monster(*t.values()):
            print(tid, n, list(t.keys()))
            mtids = set(t.keys())
            if not (monster_tids & mtids):
                # print(tid, mtids)
                monster_tids |= mtids
                total += n
            else:
                print(">>", tid, mtids)

# for tid, tile in tiles.items():
#     if tid not in monster_tids:
#         tile2 = tile[1:9, 1:9]
#         total += tile2[tile2 == "#"].size

# print(total)
# print(len(monster_tids))
