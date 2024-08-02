from hop.ch2.dispatch import read_config
from hop.ch2.calc import ast_to_string, evaluate, to_ast

import unittest


def test_example_conf():
    read_config("./tests/ch2/example.conf")


class Testcalc(unittest.TestCase):
    def test_calc(self):
        self.assertEqual(evaluate("42"), 42)
        self.assertEqual(evaluate("1 2 +"), 3)

        with self.assertRaises(Exception):
            evaluate("1 2 pow")

    def test_to_ast(self):
        self.assertEqual(to_ast("42"), 42)
        self.assertEqual(to_ast("1 2 +"), ('+', 1, 2))

    def test_to_ast(self):
        self.assertEqual(ast_to_string(to_ast("42")), "42")
        self.assertEqual(ast_to_string(to_ast("1 2 +")), "(1 + 2)")
