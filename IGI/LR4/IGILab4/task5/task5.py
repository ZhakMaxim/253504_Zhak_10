import numpy as np
from task import Task

def calculate_mean_deviation(series):
    selective_average = sum(series) / len(series)
    all_elements_squares_sum = sum(i * i for i in series)
    return np.sqrt(all_elements_squares_sum / len(series) - selective_average ** 2)


class Task5(Task):
    @staticmethod
    def perform():
        """function for performing fifth task"""
        n = np.random.randint(2, 6)
        m = np.random.randint(2, 6)
        matrix = np.random.randint(1, 10, (n, m))
        print(f'random generated int matrix:\n{matrix}')

        min_element = np.min(matrix)
        print(f'min element: {min_element}')
        min_elements_result = np.nonzero(matrix == min_element)
        min_elements_indexes = list(zip(min_elements_result[0], min_elements_result[1]))
        print(f'min elements indexes: {min_elements_indexes}')

        print(f'standard deviation, calculated by numpy: {round(float(np.std(matrix)), 2)}')
        matrix_1d = matrix.reshape([1, n*m])
        matrix_list = [el for el in matrix_1d[0]]
        print(f'standard deviation, calculated by my function: {round(calculate_mean_deviation(matrix_list), 2)}')