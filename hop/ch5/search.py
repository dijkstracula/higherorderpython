from hop.ch4.iterator import Iterator 

from typing import Callable, TypeVar, no_type_check_decorator

T = TypeVar("T")

def make_dfs_search(root: T, children: Callable[[T], T]) -> Iterator[T]:
    stack: list[T] = [root]

    def doit():
        if len(stack) > 0:
            item = stack.pop()
            stack.append(children(item))
            return item

    return doit
