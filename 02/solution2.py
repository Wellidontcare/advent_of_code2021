import numpy as np

if __name__ == "__main__":
    directions = {
        "forward": np.array([1, 0, 0]),
        "down": np.array([0, 0, 1]),
        "up": np.array([0, 0, -1]),
    }
    position = np.array([0.0, 0.0, 0.0])
    with open("input.txt") as file:
        for line in file:
            instruction = line.strip().split(" ")
            direction, ammount = instruction
            position += directions[direction] * float(ammount)
            if "forward" in direction:
                position[1] += position[2] * float(ammount)

    horizontal, vertical, aim = position
    print(f"{vertical=}, {horizontal=}")
    print(f"{horizontal*vertical=}")
