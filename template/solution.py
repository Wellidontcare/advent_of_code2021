import numpy as np
import cv2
import matplotlib.pyplot as plt


def read_file(path):
    with open(path) as f:
        return f.read()


def solve_1(data):
    pass


def solve_2(data):
    pass


if __name__ == "__main__":
    eval_sample = True

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
