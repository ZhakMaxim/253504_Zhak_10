from enum import Enum

class TYPES(Enum):
    INT = 1
    FLOAT = 2


def inputCheck(string, type_):
    """function for input check"""
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


