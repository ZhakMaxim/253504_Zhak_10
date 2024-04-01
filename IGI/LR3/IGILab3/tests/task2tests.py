import unittest
from task2 import findMaxInList

class Task2Test(unittest.TestCase):

    def test_findMaxInList(self):
        """function for testing second task"""
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = findMaxInList(lst)
        self.assertEqual(9, result)


if __name__ == '__main__':
    unittest.main()
