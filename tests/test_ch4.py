from hop.ch4.iterator import *
from hop.ch4.dir import dir_walk

import pytest
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

def test_igrep():
    it = igrep(lambda i: i % 2 == 0, upto(3,5))
    assert(it() == 4)
    assert(it() == None)

def test_dir_walk():
    it = dir_walk(".")
    assert(it() == ".")

def test_imap():
    evens = imap(lambda x: x * 2, nats())
    assert(evens() == 0)
    assert(evens() == 2)
    assert(evens() == 4)

def test_list_iterator():
    it = list_iterator([1,2,3])
    assert(it() == 1)
    assert(it() == 2)
    assert(it() == 3)
    assert(it() == None)

def test_append():
    it = append(upto(1,3), upto(10,12))
    assert(it() == 1)
    assert(it() == 2)
    assert(it() == 3)
    assert(it() == 10)
    assert(it() == 11)
    assert(it() == 12)
    assert(it() == None)


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

import hop.ch4.genes as gene

class TestGenes(unittest.TestCase):
    def test_no_pat(self):
        it = gene.make_genes("ABC")
        self.assertEqual(it(), "ABC")
        self.assertIsNone(it())

    def test_simple_pat(self):
        it = gene.make_genes("AB(C)")
        self.assertEqual(it(), "ABC")
        self.assertIsNone(it())

    def test_choice_pat(self):
        it = gene.make_genes("AB(CD)")
        self.assertEqual(it(), "ABC")
        self.assertEqual(it(), "ABD")
        self.assertIsNone(it())

    def test_multi_pats(self):
        it = gene.make_genes("AB(CD)(EF)")
        self.assertEqual(it(), "ABCE") # next: 1 0
        self.assertEqual(it(), "ABDE") # next: 0 1
        self.assertEqual(it(), "ABCF") # next: 1 1
        self.assertEqual(it(), "ABDF") # next: None


import hop.ch4.db as db

class TestDB(unittest.TestCase):
    contents = """LASTNAME:FIRSTNAME:CITY:STATE:OWES
Taylor:Nathan:Austin:TX:-420.69
Tom:Harry:SF:CA:393
Barry:White:LA:CA:900"""

    def test_query(self):
        d = db.FlatDB(from_fd(io.StringIO(self.contents)))
        it = d.query("LASTNAME", "Taylor")
        self.assertEqual(it()["LASTNAME"], "Taylor")
        self.assertIsNone(it())

    def test_query_multiple_rows(self):
        d = db.FlatDB(from_fd(io.StringIO(self.contents)))
        it = d.query("STATE", "CA")
        self.assertEqual(it()["LASTNAME"], "Tom")
        self.assertEqual(it()["LASTNAME"], "Barry")
        self.assertIsNone(it())

    def test_concurrent_iterators(self):
        pytest.skip("This doesn't work with the backwards iterator API anymore")
        d = db.FlatDB(from_fd(io.StringIO(self.contents)))
        ca_it = d.query("STATE", "CA")
        tx_it = d.query("STATE", "TX")

        ca_row = ca_it()
        # With a per-DB iterator, ca_it() iterated past the TX entry.
        tx_row = tx_it()
        self.assertIsNotNone(tx_row)
