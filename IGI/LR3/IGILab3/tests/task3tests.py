import unittest
from task3 import calculateCountOfSymbolsBetweenGanO

class Task3Test(unittest.TestCase):

    def test_calculateCountOfSymbolsBetweenGanO(self):
        """function for testing third task"""
        string = 'asdfg12345o'
        result = calculateCountOfSymbolsBetweenGanO(string)
        self.assertEqual(5, result)


if __name__ == '__main__':
    unittest.main()