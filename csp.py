from abc import abstractmethod, ABCMeta


class CSP(metaclass=ABCMeta):

    @abstractmethod
    def backtracking(self, x, y):
        pass

    @abstractmethod
    def is_save(self, x, y, val):
        pass