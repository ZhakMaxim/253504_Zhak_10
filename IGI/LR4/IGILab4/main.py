from task1.task1 import Task1
from task2.task2 import Task2
from task3.task3 import Task3
from task4.task4 import Task4
from task5.task5 import Task5
from task6.task6 import Task6
from inputfunctions import inputCheck, TYPES

class Program:
    @staticmethod
    def perform():
        """function for performing tasks"""
        while True:
            choice = inputCheck("please, enter the number of task or '0' for end: ", TYPES.INT)

            match choice:
                case 1:
                    Task1.perform()
                case 2:
                    Task2.perform()
                case 3:
                    Task3.perform()
                case 4:
                    Task4.perform()
                case 5:
                    Task5.perform()
                case 6:
                    Task6.perform()
                case 0:
                    break
                case _:
                    print("incorrect input.")

if __name__ == '__main__':
    program = Program()
    program.perform()



