from hop.ch4.iterator import Iterator

from typing import Optional, TypeVar
T = TypeVar("T")

def n_to_pat(n: int, length: int) -> list[int]:
    ret = []
    for i in range(1, length+1):
        ret = [n % i] + ret
        n = n // i
    return ret

def pattern_to_permutation(
        pattern: list[int],
        items: list[T]) -> list[T]:
    # This is dumb: can we construct the result without
    # doing destructive operations on items?
    items = [x for x in items]
    ret = []
    for i in pattern:
        print(i, items)
        ret.append(items.pop(i))
    print()
    return ret


def permute(items: list[T]) -> Iterator[list[T]]:
    n = 0
    def doit():
        nonlocal n
        pat = n_to_pat(n, len(items))
        n += 1
        return pattern_to_permutation(pat, items)

    return doit

