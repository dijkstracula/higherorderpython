from hop.ch4.iterator import Iterator

from dataclasses import dataclass

from typing import Iterator as PyIt

def partition_eager(n: int) -> list[list[int]]:
    if n == 0:
        return []
    ret = [[n]]
    for i in reversed(range(1, n)):
        for subpart in partition_eager(n-i):
            if i >= subpart[0]:
                ret.append([i] + subpart)
    return ret 

def partition_eager_acc(n: int) -> list[list[int]]:
    def iter(n: int, i: int, ret: list[list[int]]):
        if i >= 1:
            subret = [[n-i]]
            iter(n-i, (n-i-1), subret)
            for subpart in subret:
                if i >= subpart[0]:
                    ret.append([i] + subpart)
            iter(n, i-1, ret)

    ret = [[n]] 
    iter(n, n-1, ret)
    return ret

def partition_gen(n: int) -> PyIt[list[int]]:
    yield [n]
    for i in reversed(range(1, n)):
        for subpart in partition_gen(n-i):
            if i >= subpart[0]:
                yield [i] + subpart

@dataclass
class WorkItem:
    n: int
    i: int
    subpart: list[int]

def make_partition(n: int) -> Iterator[list[int]]:
    stack: list[WorkItem] = [WorkItem(n, n-1, [n])]

    def doit():
        while len(stack) > 0:
            item = stack.pop()
            n, i, ret = stack.n, stack.i, stack.subpart
            raise Exception("Argh")


    return doit

