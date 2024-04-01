import unittest

from task1 import calculateSeries

class Task1Test(unittest.TestCase):

    def test_calculateSeries(self):
        """function for testing first task"""
        x = 0.1
        eps = 0.0001
        result = calculateSeries(x, eps)
        self.assertEqual(4, result)


if __name__ == '__main__':
    unittest.main()