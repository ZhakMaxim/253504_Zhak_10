import csv
import pickle
from inputfunctions import *
from task import Task
from abc import ABC, abstractmethod

notebook = {'John': '123-456-789',
            'Victor': '111-222-333',
            'Drew': '444-555-666',
            'Paul': '777-888-999',
            'Igor': '000-111-222'
            }

class DataHandler(ABC):
    def __init__(self, filename):
        self._filename = filename

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass


class PickleHandler(DataHandler):
    def __init__(self, filename):
        super().__init__(filename)

    def serialize(self):
        with open(self._filename, 'wb') as pd:
            pickle.dump(notebook, pd)

    def deserialize(self):
        with open(self._filename, 'rb') as pd:
            data = pickle.load(pd)
        return data


class CSVHandler(DataHandler):
    def __init__(self, filename):
        super().__init__(filename)

    def serialize(self):
        with open(self._filename, 'w', newline='') as cd:
            writer = csv.writer(cd)
            for name, phone_number in notebook.items():
                writer.writerow([name, phone_number])

    def deserialize(self):
        with open(self._filename, 'r', encoding='utf-8') as cd:
            reader = csv.reader(cd)
            data = dict(reader)
        return data


class NoteBookHandler:
    def __init__(self, note_book: dict):
        self._notebook = note_book

    def find_note_by_first_letter(self, letter):
        for k, v in self._notebook.items():
            if k[0].lower() == letter.lower():
                return k, v
        return 'nothing found :('

    def find_name_by_phone_number(self, phone_number):
        for k, v in self._notebook.items():
            if v == phone_number:
                return k
        return 'nothing found :('


class Task1(Task):
    @staticmethod
    def perform():
        """function for performing first task"""
        global notebook
        notebook = dict(sorted(notebook.items()))

        csvHandler = CSVHandler('task1/csv_data.csv')
        pickleHandler = PickleHandler('task1/pickle_data.txt')
        pickleHandler.serialize()
        csvHandler.serialize()

        print(f'pickle data:\n{pickleHandler.deserialize()}')
        print(f'csv data:\n{csvHandler.deserialize()}')

        noteBookHandler = NoteBookHandler(notebook)
        while True:
            choice = inputCheck('please, choose option:\n'
                                '1: finding note by first name letter\n'
                                '2: finding name by phone number\n'
                                '0: exit\n', TYPES.INT)
            match choice:
                case 1:
                    letter = input('please, enter letter: ')
                    print(noteBookHandler.find_note_by_first_letter(letter))
                case 2:
                    phone_number = input('please input phone number(f.e. 111-111-111): ')
                    print(noteBookHandler.find_name_by_phone_number(phone_number))
                case 0:
                    break
                case _:
                    print('please choose from 0 to 2!')
                    continue