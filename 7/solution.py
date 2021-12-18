import numpy as np
import scipy.optimize as opt
import scipy as sci


def read_input(path):
    """TODO: Docstring for read_input.

    :path: TODO
    :returns: TODO

    """
    with open(path) as file:
        return [int(n) for n in file.read().strip().split(",")]


def sum_over(n):
    return (n / 2) * (n + 1)


# Works for the solution :)
def naive_align(positions):
    positions = np.array(positions)
    fuel_consumption = []
    for aligned_pos in range(np.max(positions)):
        offsets = abs(positions - aligned_pos)
        fuel_consumption.append(np.sum(offsets))
        # print(fuel_consumption)
    print(np.min(fuel_consumption))


def special_align(positions):
    sum_over_vec = np.vectorize(sum_over)
    positions = np.array(positions)
    fuel_consumption = []
    for aligned_pos in range(np.max(positions)):
        offsets = abs(positions - aligned_pos)
        fuel_consumption.append(np.sum(sum_over_vec(offsets)))
        # print(fuel_consumption)
    print(np.min(fuel_consumption))


if __name__ == "__main__":
    sample = read_input("input.txt")
    special_align(sample)
