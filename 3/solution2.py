import numpy as np

# oxygen rating:
# most common bit -> keep all that match
# next bit -> most common bit -> keep all that match


if __name__ == "__main__":
    lines = None
    with open("input.txt") as file:
        lines = [line.strip() for line in file]
    to_matrix = [[float(num) for num in line] for line in lines]

    nums = np.array(to_matrix).astype("int64")
    pos = 0
    while nums.shape[0] > 1:
        mcb = (1 * (np.sum(nums, axis=0) >= (nums.shape[0] / 2)))[pos]
        nums = nums[nums[:, pos] == mcb]
        pos += 1

    nums = np.squeeze(nums)
    print(nums)
    oxygen_str = "".join([str(int(x)) for x in (nums)])
    nums = np.array(to_matrix).astype("int64")
    pos = 0
    while nums.shape[0] > 1:
        lcb = (1 * (np.sum(nums, axis=0) < (nums.shape[0] / 2)))[pos]
        nums = nums[nums[:, pos] == lcb]
        pos += 1
    nums = np.squeeze(nums)
    print(nums)
    co2_scrubber_str = "".join([str(int(x)) for x in (nums)])
    print(f"{oxygen_str=}")
    print(f"{co2_scrubber_str=}")
    oxygen = int(oxygen_str, base=2)
    co2 = int(co2_scrubber_str, base=2)
    print(oxygen * co2)
