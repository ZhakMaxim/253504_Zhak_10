from abc import ABC, abstractmethod

class Task(ABC):
    @staticmethod
    @abstractmethod
    def perform():
        pass