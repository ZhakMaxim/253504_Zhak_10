from decorators import taskName

@taskName
def task3():
    string = input("please, enter string: ")
    print(f"count of symbols between 'g' and 'o': {calculateCountOfSymbolsBetweenGanO(string)}")

def calculateCountOfSymbolsBetweenGanO(string):
    counter = 0
    for i in range(len(string)):
        if string[i] == 'g':
            for j in range(i + 1, len(string)):
                if string[j] == 'o':
                    return counter
                counter += 1