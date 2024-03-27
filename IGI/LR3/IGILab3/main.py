from task1 import task1
from task2 import task2
from task3 import task3
from task4 import task4
from task5 import task5

from inputfunctions import inputCheck, TYPES


while True:
    choice = inputCheck("please, enter the number of task or '0' for end: ", TYPES.INT)

    match choice:
        case 1:
            task1()
        case 2:
            task2()
        case 3:
            task3()
        case 4:
            task4()
        case 5:
            task5()
        case 0:
            break
        case _:
            print("incorrect input.")
