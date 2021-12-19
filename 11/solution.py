import numpy as np
import cv2
import matplotlib.pyplot as plt
import time


def read_file(path):
    with open(path) as f:
        return f.read()


class octo:
    energy_level = -1
    neighbours = None
    flashed = False
    flash_count = 0

    def __init__(self, energy):
        self.energy_level = energy
        self.neighbours = []

    def try_flash(self):
        if self.flashed:
            return
        if self.energy_level > 9:
            self.flashed = True
            self.flash_count += 1
            for n in self.neighbours:
                n.energy_level += 1
                n.try_flash()

    def __repr__(self):
        deco = "|" if self.energy_level == 0 else " "
        return deco + f"{self.energy_level}" + deco

    def __add__(self, level):
        self.energy_level += level
        return self

    def __gt__(self, other):
        return self.energy_level > other

    def __ne__(self, other):
        return self.energy_level != other

    def __eq__(self, other):
        return self.energy_level == other


def build_octo_grid(data):
    octo_grid = np.array([[octo(n) for n in line] for line in data], dtype=octo)
    # octo_grid = np.(octo_grid, 1, constant_values=[-1])
    h, w = data.shape
    for y in range(h):
        for x in range(w):
            oc = octo_grid[y, x]
            oc.neighbours = []
            if y - 1 >= 0:
                oc.neighbours.append(octo_grid[y - 1, x])
                if x + 1 < w:
                    oc.neighbours.append(octo_grid[y - 1, x + 1])
                if x - 1 >= 0:
                    oc.neighbours.append(octo_grid[y - 1, x - 1])
            if x - 1 >= 0:
                oc.neighbours.append(octo_grid[y, x - 1])
                if y + 1 < h:
                    oc.neighbours.append(octo_grid[y + 1, x - 1])

            if y + 1 < h:
                oc.neighbours.append(octo_grid[y + 1, x])
                if x + 1 < w:
                    oc.neighbours.append(octo_grid[y + 1, x + 1])
            if x + 1 < w:
                oc.neighbours.append(octo_grid[y, x + 1])
    return octo_grid


def step(octo_grid):
    for o in octo_grid.flat:
        o.flashed = False
    octo_grid = octo_grid + 1
    for o in octo_grid.flat:
        o.try_flash()
    for o in octo_grid.flat:
        if o.flashed:
            o.energy_level = 0


def data_to_matrix(data):
    return np.array([[int(x) for x in line] for line in data.strip().split("\n")])


def solve_1(data):
    data = data_to_matrix(data)
    octo_grid = build_octo_grid(data)
    for i in range(1000):
        # print(octo_grid)
        step(octo_grid)
        # time.sleep(0.1)
        # iprint("\033c")
    print(np.sum([o.flash_count for o in octo_grid.flat]))


def solve_2(data):
    data = data_to_matrix(data)
    octo_grid = build_octo_grid(data)
    for i in range(100000):
        step(octo_grid)
        if np.all(octo_grid == 0):
            break
    print(i + 1)


if __name__ == "__main__":
    eval_sample = False

    sample_data = read_file("sample.txt")
    input_data = read_file("input.txt")

    data = sample_data if eval_sample else input_data
    print("-----------------------")
    print("Results for *:")
    solve_1(data)
    print("-----------------------")
    print("Results for **:")
    solve_2(data)
    print("-----------------------")
