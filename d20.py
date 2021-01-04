import re

import numpy as np

# fn = "d20_test.txt"
fn = "d20.txt"

with open(fn) as f:
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

N = int(np.sqrt(len(tiles)))


def get_side(a, which):
    if which == "up":
        return tuple(a[0, :])
    elif which == "right":
        return tuple(a[:, -1])
    elif which == "down":
        return tuple(a[-1, :])
    elif which == "left":
        return tuple(a[:, 0])


def get_sides(a):
    return {get_side(a, d) for d in ["up", "right", "down", "left"]}


def get_variants(a):
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
    for b in get_variants(a):
        sides |= get_sides(b)
    return sides


def is_side_unique(tid, s):
    for tid2, tile2 in tiles.items():
        if tid == tid2:
            continue
        if s in get_variant_sides(tile2):
            return False
    return True


def get_corners():
    corners = []
    for tid, tile in tiles.items():
        for a in get_variants(tile):
            if is_side_unique(tid, get_side(a, "up")) and is_side_unique(
                tid, get_side(a, "left")
            ):
                corners.append({"tid": tid, "tile": a})
                break
    return corners


def build_image():
    for c in get_corners():

        g = [[{}] * N for _ in range(N)]

        g[0][0] = c
        used_tids = {c["tid"]}

        valid = True
        for i in range(N):
            for j in range(N):
                if i == 0 and j == 0:
                    continue
                elif j == 0:
                    target_side = get_side(g[i - 1][j]["tile"], "down")
                    target_dir = "up"
                else:
                    target_side = get_side(g[i][j - 1]["tile"], "right")
                    target_dir = "left"

                found = False
                for tid, tile in tiles.items():
                    if tid in used_tids:
                        continue
                    for b in get_variants(tile):
                        if get_side(b, target_dir) == target_side:
                            g[i][j] = {"tid": tid, "tile": b}
                            used_tids.add(tid)
                            found = True
                            break
                    if found:
                        break

                valid = found

                if not valid:
                    break

            if not valid:
                break

        if valid:
            break

    for i in range(N):
        for j in range(N):
            assert g[i][j], [i, j]

    rows = []
    for i in range(N):
        row = np.hstack([g[i][j]["tile"][1:9, 1:9] for j in range(N)])
        rows.append(row)
    im = np.vstack(rows)

    assert im.shape == (8 * N, 8 * N)

    return im


def search_for_monsters(im):
    # Here in theory I should loop over the variants of `im`, but it seems
    # that it is not necessary
    n_monsters = 0
    # monster rect is 3 x 20
    for i in range(8 * N - 3):
        for j in range(8 * N - 20):
            mcs = {im[mi + i, mj + j] for mi, mj in monster}
            if mcs == {"#"}:
                n_monsters += 1
    return im[im == "#"].size - (n_monsters * len(monster))


part1 = 1
for t in get_corners():
    part1 *= t["tid"]
print("Part 1:", part1)

im = build_image()
print("Part 2:", search_for_monsters(im))
