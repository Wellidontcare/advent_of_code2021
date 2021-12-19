import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import ray


def read_input(path: str):
    with open(path) as file:
        return np.squeeze(
            np.array(
                [
                    np.array([int(num) for num in line.strip().split(",")])
                    for line in file.readlines()
                ],
                dtype=object,
            )
        )


def format_list(l: np.ndarray):
    return ",".join(str(f) for f in l.tolist())


def num_fish_in_gen_n(days, start_counter):
    return 2 ** days


def time_step(generations_tracker: np.ndarray):
    new_fish = []
    generations_tracker = generations_tracker - 1
    new_fish = [8 for f in generations_tracker if f == -1]
    generations_tracker[generations_tracker == -1] = 6
    generations_tracker = np.append(generations_tracker, new_fish)
    return generations_tracker.astype(int)


@ray.remote
def solve_by_iteration(num_days, initial_generation_state):
    for day in range(num_days):
        initial_generation_state = time_step(initial_generation_state)
    return len(initial_generation_state)


def solve_by_approximation(num_days, initial_generation_state):
    fun = lambda x, n: ((2 ** ((((x + (8 - n))) / 8))) * 6) / 8
    init_state = np.array(initial_generation_state)
    return np.sum(fun(num_days, init_state))


def solve_by_shifting(num_days, initial_generation_state):
    __import__("pudb").set_trace()
    days = np.zeros(9, dtype=int)
    for state in initial_generation_state:
        days[state] += 1
    for day in range(num_days):
        # print(days)
        days[-2] += days[0]
        days = np.roll(days, -1)
    return np.sum(days)


def solve_by_bruteforce(num_days, initial_generation_state):
    ray.init()
    tasks = [
        solve_by_iteration.remote(days, np.array([state]))
        for state in generations_tracker_i.copy()
    ]
    results = ray.get(tasks)
    return np.sum(results)


if __name__ == "__main__":
    days = 300
    generations_tracker_i = np.array(read_input("input.txt")).astype(int)
    print(solve_by_shifting(days, generations_tracker_i.copy()))
    print(solve_by_approximation(days, generations_tracker_i.copy()))
    # print(solve_by_iteration(days, generations_tracker_i.copy()))
