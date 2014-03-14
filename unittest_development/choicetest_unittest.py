
""" Exploring unit tests.
    Unit tests for unittest for choice.py. 

"""
__author__ = "Mike McFarlane (mike@mikemcfarlane.co.uk)"
__version__ = "$Revision: 0 $"
__date__ = "$Date: 11-04-14"
__copyright__ =  "Copyright (c) Mike McFarlane 2014"
__license__ = "TBC"

import choice
import unittest
import numpy as np

class RangeTests(unittest.TestCase):
    def test_range(self):
        a = choice.choice2([1])
        b = 0
        self.assertGreaterEqual(a, b)
        
    def test_bad_range(self):
        a = choice.choice2([2])
        b = 0
        self.assertGreaterEqual(a, b)
        
    def test_large_range(self):
        a = choice.choice2([0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01])
        b = 0
        self.assertGreaterEqual(a, b)
    
    def test_large_bad_range(self):      
        a = choice.choice2([0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.1])
        b = 0
        self.assertGreaterEqual(a, b)
        
    def test_huge_matrix(self):
        arraySize = 1000
        array = np.random.random(arraySize)
        arraySum = np.sum(array)
        arrayNormalised = array / arraySum
        testValue = choice.choice2(arrayNormalised)
        result = 0
        self.assertGreaterEqual(testValue, result)
        
    def test_multirow_matrix(self):
        a = choice.choice2([[0.5, 0.5], [0.5, 0.5]])
        b = 0
        self.assertGreaterEqual(a, b)
    

if __name__ == "__main__":
    unittest.main()