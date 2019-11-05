from collections import OrderedDict
from typing import Type, Callable, Optional, Tuple, List, Iterable

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from calculators.solution import Solution
from plotter import Plotter


class PlotCanvas(FigureCanvas, Plotter):  # Can't combine Plotter and Figure Canvas, class layout problem

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width // dpi, height // dpi), dpi=dpi, tight_layout=True)
        self.__graph_plot = fig.add_subplot(3, 1, 1)
        self.__error_plot = fig.add_subplot(3, 1, 2)
        self.__max_error_plot = fig.add_subplot(3, 1, 3)

        self.__numerical_solutions = []  # type: List[Type[Solution]]
        self.__numerical_function = None

        self.__exact_solution = None  # type: Optional[Type[Solution]]
        self.__exact_function = None  # type:Optional[Callable[[float, Optional[float]], float]]

        self.__calculation_data = []  # type: List[Tuple[str, Iterable[Optional[float]]]]
        self.__error_data = []  # type: List[Tuple[str, Iterable[Optional[float]]]]
        self.__max_error_data = []  # type: List[Tuple[str, Iterable[Optional[float]]]]

        self.__x_0 = None  # type: Optional[float]
        self.__y_0 = None  # type: Optional[float]
        self.__x = None  # type: Optional[float]
        self.__n_0_error = None  # type: Optional[int]
        self.__n_error = None  # type: Optional[int]
        self.__n = None  # type: Optional[int]

        self.__is_visible = {}  # type:Dict[str,bool]
        self.__colors = {}  # type: Dict[str, str]

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

    def add_solution(self, solution: Type[Solution]) -> None:
        self.__numerical_solutions.append(solution)
        self.__is_visible[solution.name] = True

    def add_exact_solution(self, exact_solution: Type[Solution]) -> None:
        self.__exact_solution = exact_solution
        self.__is_visible[exact_solution.name] = True

    def set_functions(self, exact_function: Callable[[float], float], numerical: Callable[[float, float], float]):
        self.__exact_function = exact_function
        self.__numerical_function = numerical

    def __calculate_solution(self, solution: Type[Solution], function: Callable, n: Optional[int] = None) \
            -> Tuple[property, List[Optional[float]]]:
        if n is None:
            n = self.__n
        return solution.name, solution(self.__x_0, self.__y_0, self.__x, n, function).get_data()

    def __calculate_local_error(self, numerical_points: List[Optional[float]],
                                exact_points: List[Optional[float]], calculate_truncation=False) -> List[Optional[float]]:
        local_error_points = [0]
        for i, j in zip(exact_points[1:], numerical_points[1:]):
            if i is not None and j is not None:
                error = abs(i - j)
                if calculate_truncation:
                    error -= local_error_points[-1]
                local_error_points.append(error)
            else:
                local_error_points.append(None)
        return local_error_points

    def __calculate_maximum_local_error(self, numerical_points: List[Optional[float]],
                                        exact_points: List[Optional[float]], calculate_local=True) -> Optional[float]:
        current_max = -1
        for i in self.__calculate_local_error(numerical_points, exact_points, calculate_local):
            if i is not None:
                current_max = max(current_max, i)
        return None if current_max == -1 else current_max

    def __calculate(self):
        exact_solution_calculation = self.__calculate_solution(self.__exact_solution, self.__exact_function)
        self.__calculation_data = [
            self.__calculate_solution(solution, self.__numerical_function)
            for solution in self.__numerical_solutions
        ]

        self.__error_data = [
            (
                solution[0],
                self.__calculate_local_error(
                    solution[1],
                    exact_solution_calculation[1]
                )
            )
            for solution in self.__calculation_data
        ]
        # noinspection PyTypeChecker
        self.__calculation_data.append(exact_solution_calculation)

        d = OrderedDict()

        for n in range(self.__n_0_error, self.__n_error + 1):
            exact_solution_points = self.__calculate_solution(self.__exact_solution, self.__exact_function, n)[1]
            for numerical_solution in self.__numerical_solutions:
                # noinspection PyTypeChecker
                d.setdefault(numerical_solution.name, []).append(
                    self.__calculate_maximum_local_error(
                        self.__calculate_solution(numerical_solution, self.__numerical_function, n)[1],
                        exact_solution_points
                    )
                )
        self.__max_error_data = list(d.items())

    def __parse_input(self, data: dict):
        self.set_functions(data['graph']["y"], data['graph']["f"])
        self.__x_0 = data['graph']["x_0"]
        self.__y_0 = data['graph']["y_0"]
        self.__x = data['graph']["x"]
        self.__n = data['graph']['n']
        self.__n_0_error = data['error']["n_0"]
        self.__n_error = data['error']["n"]

    def plot(self, data: dict) -> List[Tuple[str, Tuple[str, bool]]]:
        # returning correspondence: (solution.name, ['color in hex', <is_visible boolean>]
        self.__parse_input(data)

        self.__calculate()

        return self.__plot_update()

    def __plot_update(self):
        self.__graph_plot.cla()
        self.__error_plot.cla()
        self.__max_error_plot.cla()

        x_solution_plot = np.linspace(self.__x_0, self.__x, self.__n + 1)
        x_error_plot = np.linspace(self.__n_0_error, self.__n_error, self.__n_error - self.__n_0_error + 1)

        for solution in self.__max_error_data:
            if self.__is_visible[solution[0]]:
                self.__max_error_plot.plot(x_error_plot, solution[1], label=solution[0],
                                           color=self.__colors.get(solution[0], None))

        for solution in self.__error_data:
            if self.__is_visible[solution[0]]:
                self.__error_plot.plot(x_solution_plot, solution[1], label=solution[0],
                                       color=self.__colors.get(solution[0], None))

        for solution in self.__calculation_data:
            if self.__is_visible[solution[0]]:
                self.__colors.update({
                    solution[0]:
                        self.__graph_plot.plot(x_solution_plot, solution[1],
                                               label=solution[0],
                                               color=self.__colors.get(solution[0], None))[0].get_color()
                })

        self.__graph_plot.set_title("Solution comparison")
        self.__graph_plot.set_xlabel("x")
        self.__graph_plot.set_ylabel("y")
        self.__graph_plot.legend(loc="upper left")

        self.__error_plot.set_title("Local error comparison")
        self.__error_plot.set_xlabel("x")
        self.__error_plot.set_ylabel("Local error")

        self.__max_error_plot.set_title("Max local error comparison")
        self.__max_error_plot.set_xlabel("#intervals")
        self.__max_error_plot.set_ylabel("Max local error")
        self.draw()

        metadata = OrderedDict()

        for k, v in self.__colors.items():
            metadata.setdefault(k, []).append(v)

        for k, v in self.__is_visible.items():
            metadata.setdefault(k, []).append(v)

        return list(metadata.items())

    def change_visibility(self, graph_name: str, is_visible: bool) -> None:
        self.__is_visible[graph_name] = is_visible
        self.__plot_update()
