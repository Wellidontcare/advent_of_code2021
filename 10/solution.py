import numpy as np
import cv2
import scipy.optimize as opt
import scipy.stats as stat
import scipy.linalg as lin
import scipy.sparse as sparse
import scipy.special as spec
import matplotlib.pyplot as plt

score = {")": 3, "]": 57, "}": 1197, ">": 25137}
completion_score = {")": 1, "]": 2, "}": 3, ">": 4}
match = {")": "(", "]": "[", "}": "{", ">": "<"}
match_r = dict(map(reversed, match.items()))
open_char = "([{<"


def read_lines(path):
    with open(path) as file:
        return [l.strip() for l in file]


def read_comma_separated(path, t):
    with open(path) as file:
        return [t(n) for n in file.read().strip().split(",")]


def build_completion(line):
    chars = []
    for char in line:
        if char not in open_char:
            chars.pop()
        else:
            chars.append(char)
    completion = [match_r[chars.pop()] for i in range(len(chars))]
    return completion


def calculate_completion_score(completion):
    score = 0
    for char in completion:
        score *= 5
        score += completion_score[char]
    return score


def check(line):
    chars = []
    for char in line:
        if char not in open_char:
            if chars.pop() != match[char]:
                return score[char]
        else:
            chars.append(char)
    return 0


def solve_1():
    """TODO: Docstring for solve_1.
    :returns: TODO

    """
    sample = read_lines("input.txt")
    s = 0
    for line in sample:
        s += check(line)
    print(s)


def solve_2():
    sample = read_lines("input.txt")
    incomplete_lines = [l for l in sample if check(l) == 0]
    scores = [
        calculate_completion_score(build_completion(line)) for line in incomplete_lines
    ]
    print(int(np.median(scores)))


if __name__ == "__main__":
    solve_2()
