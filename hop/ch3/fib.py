#3.1. Caching Fixes Recursion

from typing import Callable, Hashable, Optional, TypeVar

# Cache miss: K + f
# Cache hit:  K
# Expected overhead for hit rate h: 
#   h*K + (1-h)(K + f)
#   h*K + (1-h)K + (1-h)f
#   (1-h+h)K + (1-h)f
#   K + (1-h)f

# Difference of memoised function vs non-memoised:
# f - K + (1-h)f
# f - K + f - hf
# K - hf
# "As the overhead of the cache hit increases, the difference is lessened"
# "As the overhead of the function increases, the difference increases"
# "As the hit rate increases, the difference increases"

# "If K < hf, the memoised version will be a net win."

def fib(month: int) -> int:
    if month <= 2:
        return 1
    return fib(month-1) + fib(month-2)

def fib_cached() -> Callable[[int], int]:
    cache = {}
    def doit(month: int) -> int:
        if month in cache:
            return cache[month]
        res = fib(month)
        cache[month] = res
        return res
    return doit

K,T,U = TypeVar("K", bound=Hashable), TypeVar("T"), TypeVar("U")

def memoize(f: Callable[[K], U]) -> Callable[[K], U]:
    cache: dict[K, U] = {}
    def doit(t: K) -> U:
        if t in cache:
            return cache[t]
        u = f(t)
        cache[t] = u
        return u
    return doit

def memoize_keygen(f: Callable[[T], U], 
            keygen: Callable[[T], K]=lambda x:x) -> Callable[[T], U]:
    cache: dict[K, U] = {}
    def doit(t: T) -> U:
        k = keygen(t)
        if k in cache:
            return cache[k]
        u = f(t)
        cache[k] = u
        return u
    return doit

def memoize_keygen_v2(f: Callable[[T], U], 
            keygen: Optional[Callable[[T], K]]=None) -> Callable[[T], U]:
    if keygen is not None:
        return memoize_keygen(f, keygen)
    return memoize(f)

# 

import dis

def beta_reduce(f: Callable[[T], K]):
    # 1. Get the internal representation of the function. 
    bc = dis.dis(f)

    # 2. What do we know about bc?  Because of type safety guarantees we know itt
    pass

def memoize_keygen_inline(f: Callable[[T], U], 
                          keygen_body: str="t") -> Callable[[T], U]:
    cache: dict[T, U] = {}
    locals = {"cache": cache, "f": f}

    exec(f"""
def doit(t):
    k = {keygen_body}
    if k in cache:
        return cache[k]
    u = f(t)
    cache[k] = u
    return u""", locals, None)
    return locals["doit"]

