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

    def test_stream_manual(self):
        i = 0
        def inc():
            nonlocal i
            i += 1
            return Node(i, inc)

        l1 = inc()
        self.assertIsInstance(l1, Node)
        self.assertEqual(head(l1), 1)

        l1 = tail(l1); assert l1
        self.assertIsInstance(l1, Node)
        self.assertEqual(head(l1), 2)

        l1 = tail(l1); assert l1
        self.assertIsInstance(l1, Node)
        self.assertEqual(head(l1), 3)

    def test_up_to(self):
        l = upto(3,5); assert l
        self.assertEqual(head(l), 3)
        l = tail(l); assert l
        self.assertEqual(head(l), 4)
        l = tail(l); assert l
        self.assertEqual(l, 5)
