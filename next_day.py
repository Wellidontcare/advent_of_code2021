#!/usr/bin/env python3

from pathlib import Path
import os
import shutil
import requests

if __name__ == "__main__":
    days = os.listdir()
    days = [d for d in days if d.isnumeric()]
    days = [int(d) for d in days]
    next_day = max(days) + 1
    session_path = Path("session.txt")
    if session_path.exists():
        with open("session.txt") as f:
            session_cookie = f.read()
    else:
        print(
            "Please provide your advent of code session cookie in a session.txt in the root directory!"
        )
        exit()
    shutil.copytree("template", Path(str(next_day)))

    session_path = Path("session.txt")
    if session_path.exists():
        with open("session.txt") as f:
            session_cookie = f.read()

    input_txt = None
    try:
        input_txt = requests.get(
            f"https://adventofcode.com/2021/day/{next_day}/input",
            cookies={"session": session_cookie.strip()},
        )
    except:
        pass

    if input_txt and input_txt.ok:
        with open(f"{next_day}/input.txt", "wb") as f:
            f.write(input_txt.content)
    else:
        print("Could not fetch input data! Everything else is set up!")

    print(f"A new day a new chance! Welcome to day {next_day}")
