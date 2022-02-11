from abc import ABC, abstractmethod

# Framework Structuring
class Matrix(ABC):

    @abstractmethod
    def actions(s):
        pass

    @abstractmethod
    def results(S,a):
        pass

    @abstractmethod
    def goalTest(S):
        pass

    @abstractmethod
    def stepCost(S,a,s):
        pass

    @abstractmethod
    def pathCost(sArray):
        pass