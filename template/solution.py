import numpy as np
import cv2
import matplotlib.pyplot as plt
import clipboard


def read_file(path):
    with open(path) as f:
        return f.read()


def solve_1(data) -> int:
    return 0


def solve_2(data) -> int:
    return 0


if __name__ == "__main__":
    eval_sample = True

    sample_data = read_file("sample.txt")
    input_data = read_file("input.txt")

    width = 35
    data = sample_data if eval_sample else input_data
    if eval_sample:
        print(f"{'SAMPLE':-^{width}}")
    else:
        print(f"{'SOLUTION':-^{width}}")
    print("*:", end=" ")
    solution1 = solve_1(data)
    print(solution1)
    print("-" * width)
    print("**:", end=" ")
    solution2 = solve_2(data)
    print(solution2)
    print("-" * width)
    if not eval_sample:
        image = np.zeros((50, 400))
        image = cv2.putText(
            image,
            "Copy Solution 1 or 2 to clipboard? (1/2)",
            (20, 24),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (255, 255, 255),
            1,
        )
        image = cv2.putText(
            image,
            f"*: {solution1}",
            (20, 42),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (255, 255, 255),
            1,
        )
        image = cv2.putText(
            image,
            f"**: {solution2}",
            (200, 42),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (255, 255, 255),
            1,
        )
        cv2.imshow("Copy results?", image)
        key = cv2.waitKey()
        if key == ord("1"):
            clipboard.copy(str(solution1))
            print("* has been copied to clipboard!")
        elif key == ord("2"):
            clipboard.copy(str(solution2))
            print("** has been copied to clipboard!")
        else:
            print488("Nothing copied to clipboard!")
        cv2.destroyAllWindows()
