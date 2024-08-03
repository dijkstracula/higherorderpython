from hop.ch1 import find_share
from hop.ch3.fib import *

import unittest

#def test_unhashable_key():
#    def f(s: set[int]) -> int:
#        return len(s)
#    m = memoize(f) # Pyright error: "Hashable is incompatable with set[int]"
#    m(set())       # Runtime execption: "unhashable type: set"

class TestFib(unittest.TestCase):
    def test_fib(self):
        self.assertEqual(fib(10), 55)

    def test_fib_cached(self):
        # TODO: quantify cache hit vs miss, maybe?
        f = fib_cached()
        for i in range(22):
            self.assertEqual(f(i), fib(i))
            self.assertEqual(f(i), fib(i))

    def test_memoize(self):
        # TODO: quantify cache hit vs miss, maybe?
        f = memoize(fib)
        for i in range(22):
            self.assertEqual(f(i), fib(i))
            self.assertEqual(f(i), fib(i))

    def test_memoize_keygen(self):
        # v2 calls memoize_keygen as well as memoize
        f = memoize_keygen_v2(fib)
        for i in range(22):
            self.assertEqual(f(i), fib(i))
            self.assertEqual(f(i), fib(i))

    def test_memoize_keygen_inline(self):
        f = memoize_keygen_inline(fib)
        for i in range(22):
            self.assertEqual(f(i), fib(i))
            self.assertEqual(f(i), fib(i))

import pytest

@pytest.mark.benchmark(group="fib")
def test_fib_naive(benchmark):
    benchmark(fib, 22)

@pytest.mark.benchmark(group="fib")
def test_fib_cached(benchmark):
    f = fib_cached()
    benchmark(f, 22)

@pytest.mark.benchmark(group="fib")
def test_fib_memoized(benchmark):
    f = memoize(fib)
    benchmark(f, 22)

@pytest.mark.benchmark(group="fib")
def test_fib_keygen_noop(benchmark):
    f = memoize_keygen(fib)
    benchmark(f, 22)

@pytest.mark.benchmark(group="fib")
def test_fib_keygen(benchmark):
    f = memoize_keygen(fib, lambda x: int(str(x)))
    benchmark(f, 22)

@pytest.mark.benchmark(group="fib")
def test_fib_keygen_inlined(benchmark):
    f = memoize_keygen_inline(fib, "int(str(t))")
    benchmark(f, 22)

@pytest.mark.benchmark(group="fib")
def test_fib_keygen_inlined_noop(benchmark):
    f = memoize_keygen_inline(fib)
    benchmark(f, 22)

def test_find_share():
    curried: Callable[[list[int]], None | list[int]] = lambda l: find_share(53, l)

    treasures = list(range(1, 11))
    f = memoize_keygen_inline(curried, "tuple(t)")
    assert f(treasures) == find_share(53, treasures)


@pytest.mark.benchmark(group="find_share")
def test_find_share_memoed(benchmark):
    curried: Callable[[list[int]], None | list[int]] = lambda l: find_share(53, l)

    treasures = list(range(1, 11))
    f = memoize_keygen_inline(curried, "tuple(t)")
    benchmark(f, treasures)


@pytest.mark.benchmark(group="find_share")
def test_find_share_naive(benchmark):
    treasures = list(range(1, 11))
    benchmark(find_share, 53, treasures)
