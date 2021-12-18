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


def read_heightmap(path):
    with open(path) as file:
        return np.array([[int(n) for n in line.strip()] for line in file])


def find_minima(heightmap):
    padded_hm = np.pad(heightmap, (1, 1), mode="maximum")
    plt.show()
    h, w = heightmap.shape
    minim = []
    for y in range(1, h + 1):
        for x in range(1, w + 1):
            indices = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
            check = np.array([padded_hm[index] for index in indices])
            middle = padded_hm[y, x]
            if np.all(check > middle):
                minim.append(middle)
    print(np.sum(np.array(minim) + 1))


def solve_1():
    hm = read_heightmap("input.txt")
    find_minima(hm)


if __name__ == "__main__":
    solve_1()
