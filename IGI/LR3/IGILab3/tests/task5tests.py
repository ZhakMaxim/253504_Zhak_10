import unittest
from task5 import calculateSumBetweenFirstAndLastPositiveElement, findMinPositiveElement

lst = [0.123, -7.23, 0, 4, 9, 1, 0.123]

class Task5Test(unittest.TestCase):

    def test_calculateSumBetweenFirstAndLastPositiveElement(self):
        """function for testing fifth task"""
        result = calculateSumBetweenFirstAndLastPositiveElement(lst)
        self.assertEqual(14.77, result)

    def test_findMinPositiveElement(self):
        """function for testing fifth task"""
        result = findMinPositiveElement(lst)
        self.assertEqual(0.123, result)


if __name__ == '__main__':
    unittest.main()