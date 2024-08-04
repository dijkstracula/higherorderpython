from typing import Callable, Optional, TypeVar

T, U = TypeVar("T"), TypeVar("U")

type Iterator[T] = Callable[[], Optional[T]]

def nextval(it: Iterator[T]) -> Optional[T]:
    return it()

def filter(it: Iterator[T], 
           p: Callable[[T], bool]) -> Iterator[T]:
    def doit():
        while True:
            t = it()
            if t == None:
                break
            if p(t):
                return t
    return doit

def upto(m: int, n: int) -> Iterator[int]:
    def doit():
        nonlocal m
        if m <= n:
            ret = m
            m += 1
            return ret
    return doit

def nats() -> Iterator[int]:
    n = 0
    def doit():
        nonlocal n
        ret = n
        n += 1
        return ret
    return doit

def map(f: Callable[[T], U],
        it: Iterator[T]) -> Iterator[U]:
    def doit():
        u = it()
        if u is not None:
            return f(u)
    return doit
