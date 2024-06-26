from inputfunctions import listInput
from decorators import taskName

def findMinPositiveElement(lst):
    """function for finding the minimum positive element from list"""
    minElement = None
    for i in lst:
        if i > 0:
            if not minElement:
                minElement = i
            else:
                minElement = min(minElement, i)
    return minElement

def calculateSumBetweenFirstAndLastPositiveElement(lst):
    """function for calculating sum between firs and last positive element from list"""
    sum_ = 0
    lastPositiveIndex = 0
    for i in range(len(lst)):
        if lst[i] > 0:
            for j in range(i + 1, len(lst) - 1):
                if lst[j] > 0:
                    lastPositiveIndex = j
            for j in range(i+1, lastPositiveIndex):
                sum_ += lst[j]

    return sum_

@taskName
def task5():
    """function for performing fifth task"""
    lst = listInput()
    print(f"min positive element: {findMinPositiveElement(lst)}")
    print(f"sum between first and last positive element: {calculateSumBetweenFirstAndLastPositiveElement(lst)}")
    print(f"list: {lst}")
