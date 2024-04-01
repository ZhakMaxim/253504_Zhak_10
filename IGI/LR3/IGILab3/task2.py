from inputfunctions import sequenceUserInput, sequenceRandomInput, inputCheck, TYPES
from decorators import taskName

def findMaxInList(lst):
    """function for finding max element in list"""
    return max(lst)

@taskName
def task2():
    """function for performing second task"""
    lst = []
    while True:
        choice = inputCheck("please, choose option: 1 - user input, 2 - random input: ", TYPES.INT)

        match choice:
            case 1:
                lst = sequenceUserInput()
                print(f"max number: {findMaxInList(lst)}")
                return
            case 2:
                lst = sequenceRandomInput()
                print(f"max number: {findMaxInList(lst)}")
                return
            case _:
                print("incorrect input, please enter one more time: ")

