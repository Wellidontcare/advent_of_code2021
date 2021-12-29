import numpy as np
from ctypes import c_uint32

if __name__ == "__main__":
    lines = None
    with open("input.txt") as file:
        lines = [line.strip() for line in file]
    to_matrix = [[float(num) for num in line] for line in lines]
    gamma = 1 * (np.sum(np.array(to_matrix), axis=0) > (len(lines) / 2))
    gamma_str = "".join([str(int(x)) for x in gamma])
    epsilon_str = "".join(["0" if x == "1" else "1" for x in gamma_str])
    gamma_val = int(gamma_str, base=2)
    epsilon_val = int(epsilon_str, base=2)
    print(f"{int(epsilon_val):b}")
    print(f"{int(gamma_val):b}")
    print(f"{gamma_str}")
    print(f"{epsilon_str}")
    print(f"{gamma_val*epsilon_val=}")
