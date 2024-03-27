from enum import Enum
import random

class TYPES(Enum):
    INT = 1
    FLOAT = 2


def inputCheck(string, type_):
    while True:
        match type_:
            case TYPES.INT:
                try:
                    input_ = int(input(f"{string}"))
                    return input_
                except ValueError as e:
                    print(str(e))
            case TYPES.FLOAT:
                try:
                    input_ = float(input(f"{string}"))
                    return input_
                except ValueError as e:
                    print(str(e))


def sequenceUserInput():
    lst = []
    print("please, enter sequence. Enter '0' for stop input")
    while True:
        el = inputCheck("", TYPES.FLOAT)
        if el:
            lst.append(el)
        else:
            return lst


def sequenceRandomInput():
    lst = []
    size = random.randint(5, 101)
    for i in range(size):
        lst.append(random.randint(1, 1000))
    print("random generated list:\n", lst)
    return lst

def listInput():
    size = inputCheck("please, input list size: ", TYPES.INT)
    lst = []
    print("please, enter list elements")
    for i in range(size):
        lst.append(inputCheck("", TYPES.FLOAT))
    return lst


