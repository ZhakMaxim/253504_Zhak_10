from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from inputfunctions import *

class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass

class ShapeColor:
    def __init__(self, color):
        self._color = color

    def getColor(self):
        return self._color

    color = property(getColor)

class Triangle(Shape):
    def __init__(self, a, h, x, color, figure_name):
        self._a = a
        self._h = h
        self._x = x
        self._color = ShapeColor(color)
        self._figure_name = figure_name

    def getX(self):
        return self._x

    x = property(getX)

    def getA(self):
        return self._a

    a = property(getA)

    def getH(self):
        return self._h

    h = property(getH)

    def getColor(self):
        return self._color

    color = property(getColor)

    def getName(self):
        return self._figure_name

    name = property(getName)

    def calculate_area(self):
        return 0.5 * self._a * self._h


    def print_attributes(self):
        print('rectangle base: {}, height: {}, color: {}, area: {}'.format(self._a, self._h, self._color.color,
                                                                           self.calculate_area()))
class TriangleDrawer:
    def __init__(self, triangle: Triangle):
        self._triangle = triangle

    def plot_triangle(self):
        x_rad = np.deg2rad(self._triangle.x)

        A = np.array([0, 0])
        C = np.array([self._triangle.a, 0])
        B = np.array([1/np.tan(x_rad) * self._triangle.h, self._triangle.h])


        plt.plot([A[0], C[0]], [A[1], C[1]], color='black')
        plt.plot([A[0], B[0]], [A[1], B[1]], color='black')
        plt.plot([B[0], C[0]], [B[1], C[1]], color='black')

        dots = np.array([A, B, C])

        hull = ConvexHull(dots)

        plt.fill(dots[hull.vertices, 0], dots[hull.vertices, 1], self._triangle.color.color)

        plt.axis('equal')
        plt.xlabel('x')
        plt.ylabel('y')

        plt.title(self._triangle.name)
        figure = plt.gcf()
        figure.set_size_inches(16, 9)
        plt.savefig(r'D:\PyCharm\PycharmProjects\IGILab4\task4\plots.png', dpi=300)
        plt.show()

class Task4:
    @staticmethod
    def perform():
        a = inputCheck('please, enter the base of triangle: ', TYPES.FLOAT)
        h = inputCheck('please, enter the height of triangle: ', TYPES.FLOAT)
        x = inputCheck('please, enter the angle: ', TYPES.INT)
        color = input('please, enter the color of triangle: ')
        name = input('please, enter the name of triangle: ')

        triangle = Triangle(a, h, x, color, name)
        triangle.print_attributes()
        triangleDrawer = TriangleDrawer(triangle)
        triangleDrawer.plot_triangle()
