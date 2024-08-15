from hop.ch6.list import *

import pytest
import unittest

class TestNode(unittest.TestCase):
    def test_head_tail(self):
        l = Node(1, Node(3, Node(2, None)))
        self.assertEqual(head(l), 1)
        self.assertEqual(head(tail(l)), 3)

    def test_insert_after(self):
        l1 = Node(1, Node(2, None))
        l2 = Node(1, Node(3, Node(2, None)))
        insert_after(l1, 3)
        self.assertEqual(l1, l2)

    def test_force(self):
        l = Node(1, None)
        with pytest.raises(Exception):
            l = force(tail(l))

    def test_stream_manual(self):
        i = 0
        def inc():
            nonlocal i
            i += 1
            return Node(i, inc)

        l1 = inc()
        self.assertIsInstance(l1, Node)
        self.assertEqual(head(l1), 1)

        l1 = force(tail(l1))
        self.assertIsInstance(l1, Node)
        self.assertEqual(head(l1), 2)

        l1 = force(tail(l1))
        self.assertIsInstance(l1, Node)
        self.assertEqual(head(l1), 3)

    def test_up_to(self):
        l = force(upto(3,5))
        self.assertEqual(head(l), 3)
        l = force(tail(l))
        self.assertEqual(head(l), 4)
        l = force(tail(l))
        self.assertEqual(head(l), 5)

    def test_up_from(self):
        l = upfrom(0)
        for _ in range(1000):
            l = force(tail(l))
        self.assertEqual(head(l), 1000)

    def test_transform(self):
        l = force(transform(lambda i: i*2, upto(1, 3)))
        self.assertEqual(head(l), 2)
        l = force(tail(l))
        self.assertEqual(head(l), 4)
        l = force(tail(l))
        self.assertEqual(head(l), 6)
        self.assertIsNone(tail(l))

    def test_filter(self):
        l = force(filter(lambda i: i%2 == 0, upto(1, 4)))
        self.assertEqual(head(l), 2)
        l = force(tail(l))
        self.assertEqual(head(l), 4)
        self.assertIsNone(tail(l))

    def test_iterate_function(self):
        l = force(iterate_function(lambda i: i*2, 1))
        for _ in range(10):
            l = force(tail(l))
        self.assertEqual(head(l), 1024)

    def test_bad_powers_of_two(self):
        def double(i: int):
            print(f"WARN: doubling {i}")
            return i*2

        l: Node[int] = Node(1, lambda: transform(double, l))
        for _ in range(10):
            l = force(tail(l))
        self.assertEqual(head(l), 1024)

    def test_merge(self):
        l1 = filter(lambda i: i%2 == 0, upto(1, 6))
        l2 = filter(lambda i: i%3 == 0, upto(1, 6))
        l = merge(l1, l2)
        # Nota Bene: 6 was deduplicated
        self.assertEqual(take(l, 1000), [2, 3, 4, 6])

    def test_stupid_merge_semantics(self):
        l1 = Node(1, Node(1, None)) 
        l2 = Node(1, Node(1, None))
        l = merge(l1, l2)
        self.assertEqual(take(l, 2), [1,1])


from hop.ch6.hamming import *

class TestHamming(unittest.TestCase):
    def test_is_hamming(self):
        self.assertTrue(is_hamming(2))
        self.assertTrue(is_hamming(3))
        self.assertTrue(is_hamming(5))

        self.assertTrue(not is_hamming(7))
        self.assertTrue(not is_hamming(11))
        self.assertTrue(not is_hamming(13))
        self.assertTrue(not is_hamming(17))

        self.assertTrue(is_hamming(20))
        self.assertTrue(not is_hamming(23))
        self.assertTrue(not is_hamming(28))
        self.assertTrue(is_hamming(32))


    def test_hamming_trivial(self):
        hs = hamming_trivial()
        self.assertEqual(take(hs, 10), [1,2,3,4,5,6,8,9,10,12])

    def test_hamming(self):
        self.assertEqual(take(hamming(), 10), [1,2,3,4,5,6,8,9,10,12])
        self.assertEqual(take(hamming(), 3000)[-1], 278942752080)

@pytest.mark.benchmark(group="hamming")
def test_first_3000_hammings(benchmark):
    benchmark(lambda: take(hamming(), 3000))

from hop.ch6.regex import *

class TestRegexGen(unittest.TestCase):
    def test_literal(self):
        l = literal("foo")
        self.assertEqual(head(l), "foo")
        self.assertIsNone(tail(l))

    def test_mingle(self):
        l1 = upto(1,3)
        l2 = upto(11,13)
        l = mingle2(l1, l2)
        self.assertEqual(take(l, 60), [1, 11, 2, 12, 3, 13])
