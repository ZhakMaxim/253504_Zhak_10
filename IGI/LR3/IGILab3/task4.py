from inputfunctions import inputCheck, TYPES
from decorators import taskName

string = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and "\
         "stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking "\
         "the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

def calculateWordsDelimitedBySpaces():
    """function for calculating words, delimited by spaces"""
    return string.count(' ') - string.count(',') - 1

def calculateEveryLetterAmount(string_):
    """function for calculating every letter amount in string"""
    string_ = string_.lower()
    letters = {}
    for i in string_:
        if i.isalpha():
            if letters.__contains__(i):
                letters[i] += 1
            else:
                letters[i] = 1
    return letters

def findAllPhrasesSeparatedByCommas():
    """function for finding all phrases, separated by commas"""
    lst = []
    for i in string.split(','):
        lst.append(i)
    return sorted(lst)

@taskName
def task4():
    """function for performing forth task"""
    while True:
        choice = inputCheck("please, enter option from 1 to 3 or '0' to exit: ", TYPES.INT)
        match choice:
            case 1:
                print(f"count of words delimited by spaces: {calculateWordsDelimitedBySpaces()}")
            case 2:
                print(f"Every letter amount: {calculateEveryLetterAmount(string)}")
            case 3:
                print(f"All phrases separated with commas: {findAllPhrasesSeparatedByCommas()}")
            case 0:
                return
            case _:
                print("incorrect input.")
                continue

