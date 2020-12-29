s = """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""

xs = list(map(int, open("d09.txt").read().strip().split("\n")))


def is_valid(n, win):
    for i in win:
        for j in win:
            if i != j and i + j == n:
                return True
    return False


# xs = list(map(int, filter(None, s.split("\n"))))

N = 25
# N = 5

for i in range(N, len(xs)):
    b = is_valid(xs[i], xs[i - N : i])
    # print(i, xs[i], b)
    if not b:
        break

g = xs[i]

found = False
for i in range(len(xs)):
    for n in range(2, len(xs) - i):
        ys = xs[i : i + n]
        if sum(ys) == g:
            print(min(ys) + max(ys))
            found = True
            break
    if found:
        break
