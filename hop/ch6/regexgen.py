from hop.ch6.list import *

from typing import Sized, TypeVar

def literal(s: str) -> List[str]:
    return Node(s, None)

def mingle2(l1: List[T], l2: List[T]) -> List[T]:
    if l1 is None: return l2
    if l2 is None: return l1
    return Node(head(l1),
                Node(head(l2), 
                     lambda: mingle2(tail(l1), tail(l2))))

def union(*ls: List[T]) -> List[T]:
    match ls:
        case []: return None
        case [l]: return l
        case [None, *xs]: 
            return union(*xs)
        case [x, *xs] if x: 
            return Node(head(x), lambda: union(*(xs + [tail(x)])))

def precat(c: str, l: List[str]) -> List[str]:
    return transform(lambda s: c+s, l)

def postcat(l: List[str], c: str) -> List[str]:
    return transform(lambda s: s+c, l)

def concat(l1: List[str], l2: List[str]) -> List[str]:
    match l1, l2:
        case None, _: return None
        case _, None: return None
        case Node(h1, _), Node(h2, _):
            return Node(h1 + h2, lambda: union(
                    postcat(tail(l1), h2),
                    precat(h1, tail(l2)),
                    concat(tail(l1), tail(l2))))

def star(s: List[str]) -> List[str]:
    r = Node("", lambda: concat(r, s))
    return r

def plus(s: List[str]) -> List[str]:
    return concat(s, star(s))

def charclass(cs: str) -> List[str]:
    its = [literal(c) for c in cs]
    return union(*its)

S = TypeVar("S", bound=Sized)

def index_of_shortest(*ls: List[S]) -> Optional[int]:
    smallest_idx = None
    smallest_seen = None

    for i, l in enumerate(ls):
        match l:
            case Node(h, _):
                curr_len = len(h)
                if smallest_seen is None or curr_len < smallest_seen:
                    smallest_seen = curr_len
                    smallest_idx = i
    return smallest_idx

def union_v2(*ls: List[S]) -> List[S]:
    i = index_of_shortest(*ls)
    if i is None: return None

    x = ls[i]
    # SAFETY: by `i` being non-None, we know ls[i] must
    # have a head, and thus must have a len and thus is a Node.
    assert(x is not None)

    xs = [a for j,a in enumerate(ls) if i != j]

    return Node(head(x), lambda: union_v2(*([tail(x)] + xs)))
