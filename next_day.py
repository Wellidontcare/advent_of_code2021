#!/usr/bin/env python3

from pathlib import Path
import os
import shutil

if __name__ == "__main__":
    days = os.listdir()
    days.remove("next_day.py")
    days.remove("template")
    days = [int(d) for d in days]
    next_day = max(days) + 1
    Path.mkdir(Path(str(next_day)))
    shutil.copy("template/solution.py", Path(str(next_day)))
    print(f"A new day a new chance! Welcome to day {next_day}")
