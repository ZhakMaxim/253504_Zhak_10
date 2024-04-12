"""Program for Lab4 - Default data types, collections, functions, modules. Version 1.0. Zhak M.V., date - 09.04.2024"""
from task1.task1 import Task1
from task2.task2 import Task2
from task3.task3 import Task3
from task4.task4 import Task4
from task5.task5 import Task5
from inputfunctions import inputCheck, TYPES

class Program:
    @staticmethod
    def perform():
        while True:
            choice = inputCheck("please, enter the number of task or '0' for end: ", TYPES.INT)

            match choice:
                case 1:
                    task1 = Task1()
                    task1.perform()
                case 2:
                    task2 = Task2()
                    task2.perform()
                case 3:
                    task3 = Task3()
                    task3.perform()
                case 4:
                    task4 = Task4()
                    task4.perform()
                case 5:
                    task5 = Task5()
                    task5.perform()
                case 0:
                    break
                case _:
                    print("incorrect input.")

program = Program()
program.perform()



