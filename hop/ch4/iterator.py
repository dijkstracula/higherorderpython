import io
 
from typing import Callable, Optional, TypeVar

T, U = TypeVar("T"), TypeVar("U")

type Iterator[T] = Callable[[], Optional[T]]

def nextval(it: Iterator[T]) -> Optional[T]:
    return it()

def igrep(p: Callable[[T], bool],
          it: Iterator[T]) -> Iterator[T]:
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

def imap(f: Callable[[T], U],
         it: Iterator[T]) -> Iterator[U]:
    def doit():
        u = it()
        if u is not None:
            return f(u)
    return doit

def from_fd(f: io.TextIOBase) -> Iterator[str]:
    def doit():
        line = f.readline()
        if line != "":
            return line.strip()
    return doit

def list_iterator(l: list[T]) -> Iterator[T]:
    i = 0
    def doit():
        nonlocal i
        if i < len(l):
            t = l[i]
            i += 1
            return t
    return doit

def append(*args: Iterator[T]) -> Iterator[T]:
    i = 0
    def doit():
        nonlocal i
        while i < len(args):
            t = args[i]()
            if t is not None:
                return t
            i += 1
    return doit
