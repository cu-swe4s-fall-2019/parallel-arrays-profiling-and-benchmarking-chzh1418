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

    def test_sample_info_hash(self):
        sample_info = 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt'
        group = 'SMTS'
        A = plot_gtex.sample_info_hash_table(group, sample_info)
        self.assertEqual(A[1][3], 'Muscle')

    def test_sample_info_hash_groups(self):
        sample_info = 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt'
        group = 'SMTS'
        A = plot_gtex.sample_info_hash_table(group, sample_info)
        self.assertEqual(len(A[1]), 31)

    def test_sample_info_hash_table(self):
        sample_info = 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt'
        group = 'SMTS'
        A = plot_gtex.sample_info_hash_table(group, sample_info)
        self.assertEqual(A[0].search('Blood')[0], 'GTEX-1117F-0003-SM-58Q7G')

    def test_sample_info_hash_table_wrong(self):
        sample_info = 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt'
        group = 'SMTS'
        A = plot_gtex.sample_info_hash_table(group, sample_info)
        self.assertNotEqual(A[0].search('Blood')[1],
                            'GTEX-1117F-0003-SM-58Q7G')


if __name__ == '__main__':
    unittest.main()
