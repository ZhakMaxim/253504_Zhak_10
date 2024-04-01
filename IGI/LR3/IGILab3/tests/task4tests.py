import unittest
from task4 import calculateEveryLetterAmount, calculateWordsDelimitedBySpaces, findAllPhrasesSeparatedByCommas, string

class Task4Test(unittest.TestCase):

    def test_calculateWordsDelimitedBySpaces(self):
        """function for testing forth task"""
        result = calculateWordsDelimitedBySpaces()
        self.assertEqual(49, result)

    def test_calculateEveryLetterAmount(self):
        """function for testing forth task"""
        result = calculateEveryLetterAmount(string)
        dict_result = {'s': 16, 'o': 12, 'h': 17, 'e': 31, 'w': 9, 'a': 16, 'c': 5, 'n': 15, 'i': 17, 'd': 13, 'r': 12,
                       'g': 5, 'm': 3, 'l': 10, 'u': 7, 'f': 4, 't': 14, 'y': 7, 'v': 1, 'p': 6, 'k': 3, 'b': 5}

        self.assertEqual(result, dict_result)

    def test_findAllPhrasesSeparatedByCommas(self):
        """function for testing forth task"""
        result = findAllPhrasesSeparatedByCommas()
        list_result = ['So she was considering in her own mind', ' as well as she could',
                       ' for the hot day made her feel very sleepy and stupid',
                       ' whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies',
                       ' when suddenly a White Rabbit with pink eyes ran close by her.']
        self.assertEqual(result, list_result)

if __name__ == '__main__':
    unittest.main()