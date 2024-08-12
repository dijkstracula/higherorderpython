from dataclasses import dataclass
from types import FunctionType
from typing import Callable, Generic, Optional, TypeAlias, TypeVar

T = TypeVar("T")

type List[T] = Optional[Node[T]]

@dataclass
class Node(Generic[T]):
    h: T
    t: List[T] | Callable[[], List[T]]

def head(l: Node[T]) -> T:
    return l.h

def tail(l: Node[T]) -> List[T]:
    if callable(l.t):
        return l.t()
    return l.t

def set_head(l: Node[T], new_head: T):
    l.h = new_head

def set_tail(l: Node[T], new_tail: List[T]):
    l.t = new_tail

def insert_after(n: Node[T], new_data: T):
    new_node = Node(new_data, n.t)
    set_tail(n, new_node)

#

def upto(m: int, n: int) -> List[T]:
    if m <= n:
        return Node(m, lambda: upto(m+1, n))
