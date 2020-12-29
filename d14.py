import re
from collections import defaultdict
from itertools import combinations

s = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

s = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

s = open("d14.txt").read()


def apply_mask(v, mask):
    b = f"{v:036b}"
    return int("".join([b[i] if mask[i] == "X" else mask[i] for i in range(36)]), 2)


def decode_address(addr, mask):
    b = f"{addr:036b}"
    c = "".join([b[i] if mask[i] == "0" else mask[i] for i in range(36)])
    floating_pos = [i for i in range(36) if c[i] == "X"]
    n_floating = len(floating_pos)
    addrs = []
    for j in range(2 ** n_floating):
        k = f"{j:0{n_floating}b}"
        d = list(c)
        for pi, p in enumerate(floating_pos):
            d[p] = k[pi]
        addrs.append(int("".join(d), 2))
    return addrs


assert decode_address(42, "000000000000000000000000000000X1001X") == [26, 27, 58, 59]


prog = []
for line in s.strip().split("\n"):
    if m := re.match("mask = (.+)", line):
        prog.append(m.group(1))
    else:
        m = re.match("mem\[(\d+)\] = (\d+)", line)
        prog.append((int(m.group(1)), int(m.group(2))))


mem1 = defaultdict(int)
mem2 = defaultdict(int)

for ins in prog:
    if isinstance(ins, str):
        mask = ins
    else:
        addr, val = ins
        mem1[addr] = apply_mask(val, mask)
        for alt_addr in decode_address(addr, mask):
            mem2[alt_addr] = val

print(sum(mem1.values()))
print(sum(mem2.values()))
