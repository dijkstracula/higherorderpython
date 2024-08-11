from dataclasses import dataclass

from hop.ch4.iterator import Iterator

def partition_all(target: int, treasures: list[int]) -> list[list[int]]:
    if target == 0:
        return [[]]
    if target < 0 or len(treasures) == 0:
        return []

    first, rest = treasures[0], treasures[1:]

    subpartitions = [[first] + x for x in partition_all(target - first, rest)]
    subpartitions.extend(partition_all(target, rest))
    return subpartitions

@dataclass
class WorkItem:
    target: int
    treasures: list[int]
    share: list[int]

def make_partitioner(target: int, treasures: list[int]) -> Iterator[list[int]]:
    worklist = list([WorkItem(target, treasures, [])])

    def doit():
        nonlocal worklist
        while len(worklist) > 0:
            w = worklist.pop()
            (target, treasures, share) = w.target, w.treasures, w.share

            if target == 0:
                return share
            if target > 0 and len(treasures) > 0:
                first, rest = treasures[0], treasures[1:]
               
                if target == first:
                    return [first] + share

                if len(rest) > 0:
                    worklist.append(WorkItem(target, rest, share))
                    if target > first:
                        worklist.append(WorkItem(target - first, rest, [first] + share))
    return doit
