from math import fabs
from inputfunctions import inputCheck, TYPES
from decorators import taskName


def calculateSeries(x, eps):
    seriesResult = 0.0
    for i in range(500):
        seriesResult += x**i
        if fabs(seriesResult - 1/(1-x)) <= eps:
            print(f"x = {x}, n = {i}, F(x) = {seriesResult}, Math F(x) = {round(1/(1-x), 3)}, eps = {eps}")
            return i
    print("max count of iterations")
    return

@taskName
def task1():
    while True:
        x = inputCheck('please, input x: ', TYPES.FLOAT)
        if fabs(x) >= 1:
            print("incorrect input.")
            continue
        eps = inputCheck('please, input eps: ', TYPES.FLOAT)
        calculateSeries(x, eps)
        return