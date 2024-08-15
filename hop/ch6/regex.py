from hop.ch6.list import *

def literal(s: str) -> List[str]:
    return Node(s, None)

def mingle2(l1: List[T], l2: List[T]) -> List[T]:
    if l1 is None: return l2
    if l2 is None: return l1
    return Node(head(l1),
                Node(head(l2), 
                     lambda: mingle2(tail(l1), tail(l2))))
