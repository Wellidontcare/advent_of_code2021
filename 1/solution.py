import numpy as np
import matplotlib.pyplot as plt


def count_increase(data):
    """TODO: Docstring for count_increase.

    :data: TODO
    :returns: TODO

    """
    return np.count_nonzero(np.diff(data) > 0)


def count_increase_sliding_mean(data):
    data_conv = np.convolve(data, [1, 1, 1], mode="valid")
    plt.plot(data_conv)
    plt.plot(np.diff(data))
    plt.plot(500 * (np.diff(data) > 0))
    return count_increase(data_conv)


if __name__ == "__main__":
    depths = np.loadtxt("input.txt")
    raw_count = count_increase(depths)
    smooth_count = count_increase_sliding_mean(depths)
    print(f"{smooth_count=}")
    print(f"{raw_count=}")
