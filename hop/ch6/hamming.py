from hop.ch6.list import *

def is_hamming(n: int) -> bool:
    while n % 2 == 0:
        n = n // 2
    while n % 3 == 0:
        n = n // 3
    while n % 5 == 0:
        n = n // 5
    return n == 1

def hamming_trivial() -> List[int]:
    return filter(is_hamming, upfrom(1))

def scale(l: List[int], factor: int) -> List[int]:
    return transform(lambda i: i * factor, l)

def hamming() -> List[int]:
    h = None
    def scale_and_merge() -> List[int]:
        return merge(scale(h, 2),
                     merge(scale(h, 3), 
                           scale(h, 5)))
    h = Node(1, scale_and_merge)
    return h
