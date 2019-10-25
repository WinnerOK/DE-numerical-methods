from typing import Type, Callable, List, Tuple, Optional, Iterable

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

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

    def add_solution(self, solution: Type[Solution]) -> None:
        self.numerical_solutions.append(solution)

    def add_exact_solution(self, reference_solution: Type[Solution]) -> None:
        self.exact_solution = reference_solution

    def set_functions(self, exact: Callable[[float], float], numerical: Callable[[float, float], float]):
        self.exact_function = exact
        self.numerical_function = numerical

    def calculate(self):
        exact_solution_points = self.exact_solution(self.x_0, self.y_0, self.x, self.n, self.exact_function).get_data()
        self.calculation_data = [
            (solution.name, solution(self.x_0, self.y_0, self.x, self.n, self.numerical_function).get_data())
            for solution in self.numerical_solutions
        ]

        self.error_data.clear()
        for numerical_solution in self.calculation_data:
            # noinspection PyTypeChecker
            self.error_data.append(
                (numerical_solution[0],
                 list(map(lambda i: abs(i[0] - i[1]), zip(exact_solution_points, numerical_solution[1]))))
            )

        # noinspection PyTypeChecker
        self.calculation_data.append(('exact', exact_solution_points))

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

        self.graph_plot.cla()
        self.error_plot.cla()

        x_solution_plot = np.linspace(self.x_0, self.x, self.n)
        x_error_plot = np.linspace(self.x_0, self.x)

        for solution in self.calculation_data:
            yield (solution[0], self.graph_plot.plot(x_solution_plot, solution[1], label=solution[0])[0].get_color())

        self.graph_plot.legend()
        self.draw()