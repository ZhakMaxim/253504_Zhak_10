import statistics
from math import fabs, sqrt
from inputfunctions import inputCheck, TYPES
import matplotlib.pyplot as plt
import numpy as np
from statistics import median, mode
from task import Task

class SeriesPlotBuilder:
    def __init__(self, series, iterations):
        self._series = series
        self._iterations = iterations

    def showPlot(self):
        x = np.linspace(-0.99, 0.99, 200)
        y1 = 1/(1-x)
        y2 = sum(x**i for i in range(self._iterations))
        plt.style.use('_mpl-gallery')
        plt.plot(x, y1, label='1/(1-x)', color='r')
        plt.plot(x, y2, label='Series', color='g')
        plt.subplots_adjust(bottom=0.05, left=0.05)

        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Series Convergence')
        plt.text(-1.05, 85, 'There are two plots:\nred is our math function\ngreen is our series ')
        plt.annotate('Annotation :)', (-1.05, 80))

        plt.grid(True)
        figure = plt.gcf()
        figure.set_size_inches(16, 9)
        plt.savefig(r'D:\PyCharm\PycharmProjects\IGILab4\task3\plots.png', dpi=300)
        plt.show()


class Series:
    def __init__(self, x, eps):
        self._x = x
        self._eps = eps

    def calculateSeries(self):
        """function for calculating sum of series with given accuracy"""
        series = []
        seriesResult = 0.0
        for i in range(500):
            series.append(self._x**i)
            seriesResult += self._x**i
            if fabs(seriesResult - 1/(1-self._x)) <= self._eps:
                print(f"x = {self._x}, n = {i}, F(x) = {round(seriesResult, 10)}, Math F(x) = {round(1/(1-self._x), 10)}"
                      f", eps = {self._eps}")
                print(f"average of series elements: {round(seriesResult/(i + 1), 10)}")
                print(f"median : {median(series)}")
                print(f"mode: {mode(series)}")
                print(f"dispersion: {statistics.variance(series)}")
                print(f"mean deviation: {statistics.stdev(series)}")
                return series, i

        print("max count of iterations")
        return


class Task3(Task):
    @staticmethod
    def perform():
        """function for performing third task"""
        while True:
            x = inputCheck('please, input x: ', TYPES.FLOAT)
            if fabs(x) >= 1:
                print("incorrect input.")
                continue
            eps = inputCheck('please, input eps: ', TYPES.FLOAT)
            series = Series(x, eps)
            series_lst, n = series.calculateSeries()

            seriesPlotBuilder = SeriesPlotBuilder(series_lst, n)
            seriesPlotBuilder.showPlot()
            return