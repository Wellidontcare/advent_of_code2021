import numpy as np
import cv2
import scipy.optimize as opt
import scipy.stats as stat
import scipy.linalg as lin
import scipy.sparse as sparse
import scipy.special as spec


def read_comma_separated(path, t):
    with open(path) as file:
        return [t(n) for n in file.read().strip().split(",")]


if __name__ == "__main__":
    sample = read_comma_separated("sample.txt", int)
