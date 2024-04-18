from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from inputfunctions import *
from task import Task

class ResizableMixin:
    _a: float
    _h: float

    def resize(self, a, h):
        self._a = a
        self._h = h

class Shape(ABC):
    def __init__(self, color, shape_name):
        self._color = ShapeColor(color)
        self._shape_name = shape_name

    def getColor(self):
        return self._color

    color = property(getColor)

    def getShapeName(self):
        return self._shape_name

    name = property(getShapeName)

    @abstractmethod
    def calculate_area(self):
        pass

class ShapeColor:
    def __init__(self, color):
        self._color = color

    def getColor(self):
        return self._color

    color = property(getColor)

class Triangle(Shape, ResizableMixin):
    def __init__(self, a, h, x, color, figure_name):
        super().__init__(color, figure_name)
        self._a = a
        self._h = h
        self._x = x

    def getX(self):
        return self._x

    x = property(getX)

    def getA(self):
        return self._a

    a = property(getA)

    def getH(self):
        return self._h

    h = property(getH)

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


        plt.xlabel('x')
        plt.ylabel('y')

        plt.title(self._triangle.name)
        figure = plt.gcf()
        figure.set_size_inches(16, 9)
        plt.savefig(r'D:\PyCharm\PycharmProjects\IGILab4\task4\plots.png', dpi=300)
        plt.show()

class Task4(Task):
    @staticmethod
    def perform():
        """function for performing fourth task"""
        a = inputCheck('please, enter the base of triangle: ', TYPES.FLOAT)
        h = inputCheck('please, enter the height of triangle: ', TYPES.FLOAT)
        x = inputCheck('please, enter the angle: ', TYPES.INT)
        color = input('please, enter the color of triangle: ')
        name = input('please, enter the name of triangle: ')

        triangle = Triangle(a, h, x, color, name)
        triangle.print_attributes()
        triangleDrawer = TriangleDrawer(triangle)
        triangleDrawer.plot_triangle()

        while True:
            choice = input('please, enter 1 if you want to change base and height of triangle or '
                           'something else if you want to quit: ')
            if choice == '1':
                a = inputCheck('please, enter the base of triangle: ', TYPES.FLOAT)
                h = inputCheck('please, enter the height of triangle: ', TYPES.FLOAT)
                triangle.resize(a, h)
                triangleDrawer.plot_triangle()
            else:
                break

