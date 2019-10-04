import os
import sys
import unittest
import math
import statistics
import data_viz
import plot_gtex
import random


class TestPlotGtex(unittest.TestCase):
    """ Unittest of plot_gtex"""
    def test_linear_search(self):
        # successfull search
        A = ['a', 'b', 'c', 'd', 'e', 'f']
        LS = plot_gtex.linear_search('c', A)
        self.assertEqual('c', A[LS])

    def test_linear_search_fail(self):
        # No hits in the list
        A = [1, 2, 3, 4, 5, 6]
        LS = plot_gtex.linear_search(7, A)
        self.assertEqual(-1, LS)

    # def test_linear_search_rand(self):
    def test_binary_search(self):
        # Successful search
        A = [['a', 1], ['b', 2], ['c', 3], ['d', 4], ['e', 5], ['f', 7]]
        BS = plot_gtex.binary_search('e', A)
        self.assertEqual(5, BS)

    def test_binary_search_fail(self):
        # No hits in the list
        A = ['1', '2', '3', '4', '5', '6']
        BS = plot_gtex.binary_search('7', A)
        self.assertEqual(-1, BS)


if __name__ == '__main__':
    unittest.main()
