import numpy as np
import cv2
import scipy.optimize as opt
import scipy.stats as stat
import scipy.linalg as lin
import scipy.sparse as sparse
import scipy.special as spec
import matplotlib.pyplot as plt


def read_comma_separated(path, t):
    with open(path) as file:
        return [t(n) for n in file.read().strip().split(",")]


def read_7_seg_display(path):
    with open(path) as file:
        lines = file.read().strip().split("\n")
        ten_combinations = [l.split("|")[0] for l in lines]
        four_digit_output = [l.split("|")[1] for l in lines]
    return ten_combinations, four_digit_output


def render_digit(code):
    raw_num = """
     dddd
    e    a
    e    a
     ffff
    g    b
    g    b
     cccc 
    """
    possible = "abcdefg"
    for seg in code:
        seg = mapping[seg]
        raw_num = raw_num.replace(seg, "o")
        possible = possible.replace(seg, "")
    for seg in possible:
        raw_num = raw_num.replace(seg, ".")
    return raw_num


def solve_1():
    ten, four = read_7_seg_display("input.txt")
    ten = [t.strip().split(" ") for t in ten]
    four = [f.strip().split(" ") for f in four]
    num_seg = [2, 3, 4, 7]
    hist = np.zeros(8)
    for f in four:
        for x in f:
            hist[len(x)] += 1
    print(np.sum([hist[[2, 3, 4, 7]]]))


def solve_mapping(ten_digits):
    digits = ten_digits.strip().split(" ")
    one = next(filter(lambda d: len(d) == 2, digits))
    four = next(filter(lambda d: len(d) == 4, digits))
    seven = next(filter(lambda d: len(d) == 3, digits))
    eight = next(filter(lambda d: len(d) == 7, digits))
    a = (set(one) ^ set(seven)).pop()
    two_three_five = list(filter(lambda d: len(d) == 5, digits))
    three_canditates = [(set(eight) - set(d)) - set(one) for d in two_three_five]
    be = next(filter(lambda x: len(x) == 2, three_canditates))
    b = (be & set(four)).pop()
    e = (be ^ set(b)).pop()
    cf = set(one)
    two = [f for f in two_three_five if e in set(f)][0]
    c = (set(two) & set(one)).pop()
    f = (cf - set(c)).pop()
    d = (set(four) - set([b, c, f])).pop()
    g = (set(eight) - set([a, b, c, d, e, f])).pop()
    return {a: "a", b: "b", c: "c", d: "d", e: "e", f: "f", g: "g"}


def map_chars(mapping, chars):
    return "".join([mapping[char] for char in chars])


def chars_to_num(chars):
    mapping = [
        "abcefg",
        "cf",
        "acdeg",
        "acdfg",
        "bcdf",
        "abdfg",
        "abdefg",
        "acf",
        "abcdefg",
        "abcdfg",
    ]
    chars = "".join(sorted(chars))
    return mapping.index(chars)


def solve_2():
    ten, four = read_7_seg_display("input.txt")
    values = []
    for t, fo in zip(ten, four):
        mapping = solve_mapping(t)
        num = []
        for f in fo.strip().split(" "):
            num.append(chars_to_num(map_chars(mapping, f)))
        values.append(int("".join(str(a) for a in num)))

    print(sum(values))


if __name__ == "__main__":
    solve_2()
