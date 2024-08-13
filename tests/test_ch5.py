from hop.ch5.partitions import *

import pytest
import unittest

def test_find_share():
    assert(partition_all(10, []) == [])
    assert(partition_all(0, [1,2,3]) == [[]])
    assert(partition_all(1, [1,2,3]) == [[1]])
    assert(partition_all(3, [1,2,3]) == [[1,2], [3]])

def test_make_partitioner():
    # TODO: I feel like this behaviour is more philosophical...
    it = make_partitioner(0, [0,0])
    assert(it() == [])
    assert(it() == None)

    it = make_partitioner(3, [1,2,3])
    # shut up, pyright
    assert(set(it() or []) == set([1,2]))
    assert(set(it() or []) == set([3]))
    assert(it() == None)

from hop.ch5.intpart import *

class TestIntPartition(unittest.TestCase):
    def test_eager(self):
        self.assertEqual(partition_eager(1), [[1]])
        self.assertEqual(partition_eager(2), [[2], [1,1]])
        self.assertEqual(partition_eager(3), [[3], 
                                              [2,1], 
                                              [1,1,1]])
        self.assertEqual(partition_eager(4), [[4], 
                                              [3,1], 
                                              [2,2] ,[2,1,1], 
                                              [1,1,1,1]])

    def test_acc(self):
        for i in range(2, 6):
            self.assertEqual(partition_eager(i), partition_eager_acc(i))

    def test_gen(self):
        for i in range(2, 6):
            self.assertEqual(partition_eager(i), list(partition_gen(i)))

    def test_iterator(self):
        pytest.skip("I don't know how to do this one :/")
        it = make_partition(3)
        self.assertEqual(it(), [3])
        self.assertEqual(it(), [2,1])

from hop.ch5.tailcall import *
from itertools import product

class TestTailCalls(unittest.TestCase):
    def test_flatten_tree(self):
        t = BinTreeNode(BinTreeNode(None, 2, None),
                        3,
                        BinTreeNode(None, 4, None))
        t = BinTreeNode(BinTreeNode(None, 0, None),
                        1,
                        t)
        self.assertEqual(flatten_tree(t), [0,1,2,3,4])
        self.assertEqual(flatten_tree_v2(t), [0,1,2,3,4])
        self.assertEqual(flatten_tree_v3(t), [0,1,2,3,4])

    def test_gcd(self):
        for m, n in product(range(100), range(100)):
            self.assertEqual(gcd(m,n), gcd_tc(m,n))

    def test_binary(self):
        for n in range(32):
            self.assertEqual(binary(n), binary_acc(n))

    def test_fib(self):
        for i in range(10):
            self.assertEqual(fib(i), fib_v2(i))
            self.assertEqual(fib_v2(i), fib_v3(i))
            self.assertEqual(fib_v3(i), fib_v3_opto(i))


import pytest

@pytest.mark.benchmark(group="fib-iter")
def test_fib_recursive(benchmark):
    benchmark(fib_v2, 22)

@pytest.mark.benchmark(group="fib-iter")
def test_fib_iterative(benchmark):
    benchmark(fib_v3, 22)

@pytest.mark.benchmark(group="fib-iter")
def test_fib_iterative_optimized(benchmark):
    benchmark(fib_v3_opto, 22)
