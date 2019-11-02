from math import *  # Need calculate any functions f'(x,y) and f(x)
from typing import Optional, Dict

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QCheckBox, QLineEdit
from PyQt5.QtCore import QRegularExpression, pyqtSlot
from PyQt5.QtGui import QRegularExpressionValidator

from designs.centralWidget import Ui_MainWindow
from plotter import PlotCanvas

EPS = 1e-5


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__ui = Ui_MainWindow()
        self.plotter = PlotCanvas()
        self.__setup_ui()
        self.__graph_checkboxes = {}  # checkboxes of plotted graphs

    def __setup_ui(self):
        self.__ui.setupUi(self)
        self.__setup_validators()
        self.__setup_buttons()
        self.__ui.gridLayout.addWidget(self.plotter, 0, 0, 1, 4)

    def __setup_validators(self):
        positive_integer = QRegularExpression(r"\d+")
        positive_integer_validator = QRegularExpressionValidator(positive_integer)

        rational = QRegularExpression(r"-?\d+\.\d+")
        rational_validator = QRegularExpressionValidator(rational)

        self.__ui.x0_Input.setValidator(rational_validator)
        self.__ui.y0_Input.setValidator(rational_validator)
        self.__ui.x_Input.setValidator(rational_validator)
        self.__ui.n_Input.setValidator(positive_integer_validator)
        self.__ui.n0_error_Input.setValidator(positive_integer_validator)
        self.__ui.n_error_Input.setValidator(positive_integer_validator)

    def __setup_buttons(self):
        self.__ui.reset_input_Button.clicked.connect(self.reset_input)
        self.__ui.solutions_Button.clicked.connect(self.draw)

    def reset_input(self):  # resetting input for a given IVP
        self.__ui.x0_Input.setText("1")
        self.__ui.y0_Input.setText("2")
        self.__ui.x_Input.setText("6")
        self.__ui.n_Input.setText("100")
        self.__ui.f_Input.setText("(1 + y / x) * log(1 + y / x) + y / x")
        self.__ui.y_exact_Input.setText("x * (exp(log(pow(y_0 / x_0 + 1, x / x_0))) - 1)")

    def __add_graph_checkbox(self, method_name: str, color: str, is_checked: bool):  # add a checkbox for a plotted graph
        tmp = QCheckBox(method_name)
        tmp.setStyleSheet("QCheckBox { color: " + color + "}")  # Setting a color to a checkbox label
        tmp.setChecked(is_checked)
        tmp.stateChanged.connect(self.update_plot)
        self.__ui.checkbox_Layout.addWidget(tmp)
        self.__graph_checkboxes[method_name] = tmp

    def clear_graph_checkbox(self):  # remove all checkboxes
        # This function doesn't do any helpful work in terms of this assignment, but in general in might be needed
        # if solutions are being added/removed during the runtime
        for i in reversed(range(1, self.__ui.checkbox_Layout.count())):
            # Remove in reverse order in order to preserve a layout for future checkboxes
            self.__ui.checkbox_Layout.itemAt(i).widget().setParent(None)  # Widgets without parent will be deleted by gc
        self.__graph_checkboxes.clear()

    def __notify_mistake(self, message: str, line_edit: Optional[QLineEdit]):  # Notify user about an input mistake
        QMessageBox.warning(self, 'Invalid input', message, QMessageBox.Ok,
                            QMessageBox.Ok)
        if line_edit is not None:
            line_edit.setFocus()
            line_edit.selectAll()

    def __validate_input(self, data: dict):
        if data['graph']['x_0'] > data['graph']['x']:
            self.__notify_mistake("X<sub>0</sub> is greater than X", self.__ui.x_Input)
            return False

        if data['error']['n_0'] > data['error']['n']:
            self.__notify_mistake("N<sub>0</sub> is greater than N", self.__ui.n_error_Input)
            return False

        if data['error']['n_0'] <= 0:
            self.__notify_mistake("N<sub>0</sub> must be greater than 0", self.__ui.n0_error_Input)
            return False

        if data['graph']['n'] <= 0:
            self.__notify_mistake("N must be greater than 0", self.__ui.n_Input)
            return False

        x_0 = data['graph']['x_0']
        y_0 = data['graph']['y_0']
        y = data['graph']['y']
        try:
            if abs(y_0 - y(x_0)) > EPS:
                print(y(x_0), y_0)
                self.__notify_mistake("Given exact solution does not correspond to the IVP", self.__ui.y_exact_Input)
                return False
        except Exception as e:
            self.__notify_mistake(f"An error occurred while parsing the exact solution:\n\"{e}\"",
                                  self.__ui.y_exact_Input)
            return False

        return True

    def get_input(self) -> Optional[Dict]:
        try:
            inp = {
                "graph": {
                    "x_0": float(self.__ui.x0_Input.text()),
                    "y_0": float(self.__ui.y0_Input.text()),
                    "x": float(self.__ui.x_Input.text()),
                    "n": int(self.__ui.n_Input.text())
                },

                "error": {
                    "n_0": int(self.__ui.n0_error_Input.text()),
                    "n": int(self.__ui.n_error_Input.text())
                }
            }
        except ValueError:
            self.__notify_mistake("Some of input fields are empty.", None)
            return
        ivp = {
            "x_0": inp['graph']['x_0'],
            "y_0": inp['graph']['y_0'],
        }
        inp["graph"]["y"] = lambda x: eval(self.__ui.y_exact_Input.text(),
                                           locals().update(ivp)
                                           )
        inp["graph"]["f"] = lambda x, y: eval(self.__ui.f_Input.text(),
                                              locals().update(ivp)
                                              )

        if self.__validate_input(inp):
            return inp

    @pyqtSlot()
    def draw(self):
        input_data = self.get_input()
        if input_data is None:
            return  # Input is invalid
        self.clear_graph_checkbox()
        for name, metadata in self.plotter.plot(input_data):
            self.__add_graph_checkbox(name, *metadata)

    @pyqtSlot()
    def update_plot(self):
        self.plotter.change_visibility(self.sender().text(), self.sender().isChecked())


app = QApplication([])
