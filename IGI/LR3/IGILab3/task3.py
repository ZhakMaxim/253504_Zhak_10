from decorators import taskName


def calculateCountOfSymbolsBetweenGanO(string):
    """function for calculating count of symbols between G and O"""
    counter = 0
    for i in range(len(string)):
        if string[i] == 'g':
            for j in range(i + 1, len(string)):
                if string[j] == 'o':
                    return counter
                counter += 1

@taskName
def task3():
    """function for performing third task"""
    string = input("please, enter string: ")
    print(f"count of symbols between 'g' and 'o': {calculateCountOfSymbolsBetweenGanO(string)}")