# Chapter 1: Recursion and Callbacks

from collections import Counter

from typing import Callable, Optional, TypeVar

T = TypeVar("T")


def binary(n: int) -> str:
    if n == 0 or n == 1:
        return str(n)
    return binary(n // 2) + str(n % 2)


def factorial(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return factorial(n - 1) * n


# 1.3. Hanoi

position = [" "] + ["A" for _ in range(3)]


def check_move(disk: int, start: str, end: str):
    global position

    if disk < 1 or disk >= len(position):
        raise Exception(f"Bad disk number {disk}: should be 1..{len(position)}")
    if position[disk] != start:
        raise Exception(f"Tried to move disk {disk} from {start}, but it is on {position[disk]}")

    for i in range(1, disk):
        if position[i] == start:
            raise Exception(f"Can't move {disk} from {start} because {i} is on top of it.")
        if position[i] == end:
            raise Exception(f"Can't move {disk} to {end} because {i} is already there.")
    move_disk(disk, start, end)
    position[disk] = end;


def move_disk(n: int, start: str, end: str):
    print(f"Move disk {n} from {start} to {end}.")


def hanoi(n: int = 3, start: str = "A", end: str = "B", extra: str = "C",
          move_disk: Callable[[int, str, str], None] = check_move):
    """Solve the Tower of Hanoi problem for a tower of N disks,
    of which the largest is disk `N`.  Move the entire tower from
    `start` to `end`, using `extra` as a workspace."""

    if n == 1:
        move_disk(n, start, end)
    else:
        hanoi(n - 1, start, extra, end, move_disk)
        move_disk(n, start, end)
        hanoi(n - 1, extra, end, start, move_disk)


# 1.4. Hierarchial data

import os
import os.path


def file_size(file: str) -> int:
    return os.path.getsize(file) // 1024


def dir_size(dir: str, results: list[int]) -> int:
    sz = os.path.getsize(dir) // 1024 + sum(results)
    print(f"DIR {dir} {sz}")
    return sz


type D = dict[str, int | D]


def file_rep(file: str) -> D:
    return {file: os.path.getsize(file) // 1024}


def dir_rep(dir: str, results: list[D]) -> D:
    contents = {}
    for r in results:
        contents = contents | r
    return {dir: contents}


def dir_walk(path: str,
             on_file: Callable[[str], T] = file_rep,
             on_dir: Callable[[str, list[T]], T] = dir_rep) -> T:
    if os.path.isdir(path):
        results = []
        for file in os.scandir(path):
            results.append(dir_walk(str(file.path), on_file, on_dir))
        return on_dir(path, results)

    elif os.path.isfile(path):
        return on_file(path)

    assert False


# 1.8. When Recursion Blows Up

def find_share(target: int, treasures: list[int]) -> Optional[list[int]]:
    if target == 0:
        return []
    if target < 0 or len(treasures) == 0:
        return None

    first, rest = treasures[0], treasures[1:]

    ret = find_share(target - first, rest)
    if ret is not None:
        return [first] + ret
    return find_share(target, rest)


def partition(treasures: list[int]) -> Optional[tuple[list[int], list[int]]]:
    share_1 = find_share(sum(treasures) // 2, treasures)
    if share_1 is None:
        return None
    share_2 = []

    s1_counts = Counter(share_1)
    for t in treasures:
        if t in s1_counts:
            s1_counts[t] -= 1
        else:
            share_2.append(t)
    return (share_1, share_2)
