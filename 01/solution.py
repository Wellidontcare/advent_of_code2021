import numpy as np
import matplotlib.pyplot as plt


def count_increase(data):
    """TODO: Docstring for count_increase.

    :data: TODO
    :returns: TODO

    """
    return np.count_nonzero(np.diff(data) > 0)

def count_increase_sliding_mean(data):
    data_conv = np.correlate(data, [1, 1, 1], mode="valid")
    # plt.plot(data_conv)
    # plt.plot(np.diff(data))
    # plt.plot(500 * (np.diff(data) > 0))
    print(data_conv)
    return count_increase(data_conv)


def solve_1(data):
    print(count_increase(data))


def solve_2(data):
    print(count_increase_sliding_mean(data))


if __name__ == "__main__":
    eval_sample = False

    sample_data = None
    input_data = np.loadtxt("input.txt")

    data = sample_data if eval_sample else input_data
    

    print("----------------------------")
    print("Result for *:")
    solve_1(data)
    print("-----------------------------")
    print("Result for **:")
    solve_2(data)
    print("-----------------------------")
