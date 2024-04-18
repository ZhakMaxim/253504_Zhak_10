import pandas as pd
from statistics import mean
from task import Task


class DataFrameHandler:
    def __init__(self, file_name):
        self._file_name = file_name
        self._data_frame = pd.read_csv(self._file_name)

    def print_data_frame_by_keys(self):
        data_frame_keys = list(self._data_frame)
        print(f'data frame keys: {data_frame_keys}')
        for key in data_frame_keys:
            print(f'{key}:')
            print(self._data_frame[key])

    def data_frame_calculation_number_1(self):
        n_cores_battery_power = self._data_frame.groupby('n_cores').mean()['battery_power']
        res = n_cores_battery_power[len(n_cores_battery_power)] / n_cores_battery_power[1]
        return res

    def data_frame_calculation_number_2(self):
        clock_speed_ram = self._data_frame.groupby('clock_speed').mean()['ram']
        ram_mean = mean(list(clock_speed_ram))
        buff = self._data_frame[self._data_frame['ram'] > ram_mean]
        res = buff['clock_speed'].mean()
        return res


class Task6(Task):
    @staticmethod
    def perform():
        """function for performing sixs task"""

        data_frame_handler = DataFrameHandler(r'D:\PyCharm\PycharmProjects\IGILab4\task6\test.csv')

        data_frame_handler.print_data_frame_by_keys()

        print(f'\nHow many times is the average battery power of phones with the maximum number of cores \ngreater than '
              f'the average battery power of phones with the minimum number of cores: '
              f'{round(data_frame_handler.data_frame_calculation_number_1(), 2)}\n')

        print(f'average clock speed of phone, which ram is more than average: '
              f'{round(data_frame_handler.data_frame_calculation_number_2(), 2)} GHz')