from hop.utils import Comparable

from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar

T,U = TypeVar("T", bound=Comparable), TypeVar("U", bound=Comparable)

type List[T] = Optional[Node[T]]

@dataclass
class Node(Generic[T]):
    h: T
    t: List[T] | Callable[[], List[T]]

def head(l: Node[T]) -> T:
    return l.h

def tail(l: Node[T]) -> List[T]:
    if callable(l.t):
        l.t = l.t()
    return l.t

def set_head(l: Node[T], new_head: T):
    l.h = new_head

def set_tail(l: Node[T], new_tail: List[T]):
    l.t = new_tail

def insert_after(n: Node[T], new_data: T):
    new_node = Node(new_data, n.t)
    set_tail(n, new_node)

def force(l: List[T]) -> Node[T]:
    if l is None:
        raise Exception("Can't force an exhausted List")
    return l
#

def upto(m: int, n: int) -> List[int]:
    if m <= n:
        return Node(m, lambda: upto(m+1, n))

def upfrom(n: int) -> List[int]:
    return Node(n, lambda: upfrom(n+1))

def take(l: List[T], n: int) -> list[T]:
    ret = []
    while n > 0 and l is not None:
        ret.append(head(l))
        l = tail(l)
        n -= 1
    return ret

# 

def transform(f: Callable[[T], U], l: List[T]) -> List[U]:
    match l:
        case None: return None
        case Node(h, _): 
            # Slightly annoying: we can't pattern-match on `t` because at the
            # moment only tail() forces the evaluation of a promise and `t`
            # might be a Callable. I wonder if there's a magical way to do
            # evaluate `t` implicitly...
            return Node(f(h), lambda: transform(f, tail(l)))

def filter(f: Callable[[T], bool], l: List[T]) -> List[T]:
    while True:
        match l:
            case None: return None
            case Node(h, _):
                l = tail(l)
                if f(h): return Node(h, lambda: filter(f, l))

def iterate_function(f: Callable[[T], T], x: T) -> List[T]:
    return Node(x, lambda: iterate_function(f, f(x)))

# 

def merge(l1: List[T], l2: List[T]) -> List[T]:
    match l1,l2:
        case l1, None: return l1
        case None, l2: return l2

        case Node(h1, _), Node(h2, _):
            if h1 < h2:
                return Node(h1, lambda: merge(tail(l1), l2))
            elif h1 == h2:
                # Editorial: these semantics are silly, because equal elements
                # are only deduplicated if the lists' elements are strictly
                # increasing; merge([1,1,1], [1,1,1]) will, itself, produce
                # [1,1,1].
                return Node(h1, lambda: merge(tail(l1), tail(l2)))
            else:
                return Node(h2, lambda: merge(l1, tail(l2)))
