from typing import Type, List, Tuple
from abc import ABCMeta, abstractmethod

from PyQt5.QtWidgets import QWidget
from calculators.solution import Solution


class PlotterMeta(type(QWidget), ABCMeta):
    pass


class Plotter(QWidget, metaclass=PlotterMeta):
    @abstractmethod
    def add_exact_solution(self, exact_solution: Type[Solution]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_solution(self, solution: Type[Solution]) -> None:
        raise NotImplementedError

    @abstractmethod
    def plot(self, data: dict) -> List[Tuple[str, Tuple[str, bool]]]:
        # Input format must be specified by a subclass
        raise NotImplementedError

    @abstractmethod
    def change_visibility(self, graph_name: str, is_visible: bool) -> None:
        # Change visibility of a graph by name
        raise NotImplementedError
