from typing import Type, Callable, List, Tuple, Optional, Iterable, Dict

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from calculators.solution import Solution


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width // dpi, height // dpi), dpi=dpi)
        self.graph_plot = fig.add_subplot(2, 1, 1)
        self.error_plot = fig.add_subplot(2, 1, 2)

        self.numerical_solutions = []  # type: List[Type[Solution]]
        self.numerical_function = None

        self.exact_solution = None  # type: Optional[Type[Solution]]
        self.exact_function = None  # type:Optional[Callable[[float, Optional[float]], float]]

        self.calculation_data = []  # type: List[Tuple[str, Iterable[Optional[float]]]]
        self.error_data = []  # type: List[Tuple[str, Iterable[Optional[float]]]]

        self.x_0 = None  # type: Optional[float]
        self.y_0 = None  # type: Optional[float]
        self.x = None  # type: Optional[float]
        self.n_0_error = None  # type: Optional[int]
        self.n_error = None  # type: Optional[int]
        self.n = None  # type: Optional[int]

        self.is_visible = {}  # type:Dict[str,bool]
        self.colors = {}  # type: Dict[str, str]

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

    def add_solution(self, solution: Type[Solution]) -> None:
        self.numerical_solutions.append(solution)
        self.is_visible[solution.name] = True

    def add_exact_solution(self, reference_solution: Type[Solution]) -> None:
        self.exact_solution = reference_solution
        self.is_visible[reference_solution.name] = True

    def set_functions(self, exact: Callable[[float], float], numerical: Callable[[float, float], float]):
        self.exact_function = exact
        self.numerical_function = numerical

    def calculate_solution(self, solution: Type[Solution], function: Callable, n: Optional[int] = None) \
            -> Tuple[property, List[Optional[float]]]:
        if n is None:
            n = self.n
        return solution.name, solution(self.x_0, self.y_0, self.x, n, function).get_data()

    def calculate_maximum_local_error(self, numerical_points: List[Optional[float]],
                                      exact_points: List[Optional[float]]) -> Optional[float]:
        current_max = -1
        for i, j in zip(exact_points, numerical_points):
            if i is not None and j is not None:
                current_max = max(current_max, abs(i - j))
        return None if current_max == -1 else current_max

    def calculate(self):
        exact_solution_calculation = self.calculate_solution(self.exact_solution, self.exact_function)
        self.calculation_data = [
            self.calculate_solution(solution, self.numerical_function)
            for solution in self.numerical_solutions
        ]
        # noinspection PyTypeChecker
        self.calculation_data.append(exact_solution_calculation)

        self.error_data.clear()

        for numerical_solution in self.numerical_solutions:
            # noinspection PyTypeChecker
            self.error_data.append(
                (
                    numerical_solution.name,
                    [
                        self.calculate_maximum_local_error(
                            self.calculate_solution(numerical_solution, self.numerical_function, n)[1],
                            self.calculate_solution(self.exact_solution, self.exact_function, n)[1]
                        ) for n in range(self.n_0_error, self.n_error + 1)
                    ],
                    True
                )
            )

    def parse_input(self, data: dict):
        self.set_functions(data['graph']["y"], data['graph']["f"])
        self.x_0 = data['graph']["x_0"]
        self.y_0 = data['graph']["y_0"]
        self.x = data['graph']["x"]
        self.n = data['graph']['n']
        self.n_0_error = data['error']["n_0"]
        self.n_error = data['error']["n"]

    def plot(self, data: dict):
        self.parse_input(data)

        self.calculate()

        return self.plot_update()

    def plot_update(self):
        self.graph_plot.cla()
        self.error_plot.cla()

        x_solution_plot = np.linspace(self.x_0, self.x, self.n + 1)
        x_error_plot = np.linspace(self.n_0_error, self.n_error, self.n_error - self.n_0_error + 1)

        colors = []

        for solution in self.error_data:
            if self.is_visible[solution[0]]:
                self.error_plot.plot(x_error_plot, solution[1], label=solution[0])

        for solution in self.calculation_data:
            if self.is_visible[solution[0]]:
                self.colors.update({
                    solution[0]:
                        self.graph_plot.plot(x_solution_plot, solution[1],
                                             "o-", label=solution[0],
                                             color=self.colors.get(solution[0], None))[0].get_color()
                })
                # yield (
                #     solution[0],
                #     self.graph_plot.plot(x_solution_plot, solution[1], "o-", label=solution[0])[0].get_color()
                # )

        self.graph_plot.set_title("Solution comparison")
        self.graph_plot.set_xlabel("x")
        self.graph_plot.set_ylabel("y")
        self.graph_plot.legend()

        self.error_plot.set_title("Max local error comparison")
        self.error_plot.set_xlabel("#intervals")
        self.error_plot.set_ylabel("Max local error")
        self.draw()

        return self.colors.items()

    def change_visibility(self, graph_name: str, is_visible: bool):
        self.is_visible[graph_name] = is_visible
        self.plot_update()
