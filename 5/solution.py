import numpy as np
import matplotlib.pyplot as plt
import cv2


def get_horizontal_lines(lines):
    """TODO: Docstring for get_horizontal_lines.

    :start: TODO
    :end: TODO
    :returns: TODO

    """
    h_lines = [li for li in lines if li[0, 1] == li[1, 1]]
    return h_lines


def get_vertical_lines(lines):
    v_lines = [li for li in lines if li[1, 0] == li[0, 0]]
    return v_lines


if __name__ == "__main__":
    start = []
    end = []
    with open("input.txt", "r") as file:
        for line in file:
            start.append([int(x) for x in line.split("->")[0].split(",")])
            end.append([int(x) for x in line.split("->")[1].split(",")])
    lines = np.array(list(zip(start, end)))
    print(start)
    print(end)
    v_lines = get_vertical_lines(lines)
    h_lines = get_horizontal_lines(lines)
    image = np.zeros((np.max(lines) + 5, np.max(lines) + 5))
    image_add = np.zeros_like(image)
    for s, e in lines:
        image_add += cv2.line(image.copy(), tuple(s), tuple(e), (1, 1, 1))
    # for s, e in v_lines:
    #    image_add += cv2.line(image.copy(), tuple(s), tuple(e), (1, 1, 1))
    # for s, e in h_lines:
    #    image_add += cv2.line(image.copy(), tuple(s), tuple(e), (1, 1, 1))
    plt.matshow(image_add)
    print(np.count_nonzero(image_add >= 2))

    plt.show()
