from hop.ch4.iterator import *
from hop.ch4.dir import dir_walk

import unittest

def test_nextval():
    it = upto(3, 5)
    assert(nextval(it) == 3)

def test_upto():
    it = upto(3, 5)
    assert(it() == 3)
    assert(it() == 4)
    assert(it() == 5)
    assert(it() == None)
    assert(it() == None)

def test_filter():
    it = filter(upto(3,5), lambda i: i % 2 == 0)
    assert(it() == 4)
    assert(it() == None)

def test_dir_walk():
    it = dir_walk(".")
    assert(it() == ".")

def test_map():
    evens = map(lambda x: x * 2, nats())
    assert(evens() == 0)
    assert(evens() == 2)
    assert(evens() == 4)

import hop.ch4.perm as perm

class TestPermute(unittest.TestCase):
    def test_n_to_pat(self):
        self.assertEqual(perm.n_to_pat(0, 4), [0,0,0,0])
        self.assertEqual(perm.n_to_pat(1, 4), [0,0,1,0])
        self.assertEqual(perm.n_to_pat(2, 4), [0,1,0,0])
        self.assertEqual(perm.n_to_pat(3, 4), [0,1,1,0])
        self.assertEqual(perm.n_to_pat(4, 4), [0,2,0,0])

    def test_pattern_to_perm(self):
        self.assertEqual(
                perm.pattern_to_permutation([0,0,0,0], 
                                            ["A", "B", "C", "D"]), 
                ["A", "B", "C", "D"])

        self.assertEqual(
                perm.pattern_to_permutation([0,1,0,0], 
                                            ["A", "B", "C", "D"]), 
                ["A", "C", "B", "D"])

    def test_perm(self):
        it = perm.permute([1,2,3])
        res = []
        for _ in range(6):
            p = it()
            if p == None:
                break
            res.append(p)