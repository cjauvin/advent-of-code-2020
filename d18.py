import math
import operator


def f(seq):
    def _f(seq):
        curr_op = None
        curr_val = None
        i = 0
        while True:
            c = seq[i]
            if c == "(":
                sub_val, n = _f(seq[i + 1 :])
                curr_val = curr_op(curr_val, sub_val) if curr_op else sub_val
                i += n
            elif c == ")":
                i += 2
                break
            elif c in ["+", "*"]:
                curr_op = operator.add if c == "+" else operator.mul
                i += 1
            else:
                curr_val = curr_op(curr_val, int(c)) if curr_val else int(c)
                i += 1
            if i == len(seq):
                break
        return curr_val, i

    return _f(list(seq.replace(" ", "")))[0]


def g(seq):
    def _g(seq):
        stack = []
        curr_op = None
        i = 0
        while True:
            c = seq[i]
            if c == "(":
                sub_val, n = _g(seq[i + 1 :])
                if curr_op == "+":
                    stack.append(stack.pop() + sub_val)
                else:
                    stack.append(sub_val)
                i += n
            elif c == ")":
                i += 2
                break
            elif c in ["+", "*"]:
                curr_op = c
                i += 1
            else:
                if curr_op == "+":
                    stack.append(stack.pop() + int(c))
                else:
                    stack.append(int(c))
                i += 1
            if i == len(seq):
                break
        return math.prod(stack), i

    return _g(list(seq.replace(" ", "")))[0]


assert f("1 * 2 + 3") == 5
assert f("1 * 2 + (2 * 3)") == 8
assert f("(1 + (2 * 3))") == 7
assert f("2 * 3 + (4 * 5)") == 26
assert f("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert f("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert f("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

assert g("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert g("2 * 3 + (4 * 5)") == 46
assert g("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert g("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert g("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340

lines = open("d18.txt").read().strip().split("\n")

print(sum(map(f, lines)))
print(sum(map(g, lines)))
