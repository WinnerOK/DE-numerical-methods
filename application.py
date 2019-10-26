from math import *
from typing import Optional

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QCheckBox, QLineEdit
from PyQt5.QtCore import QRegularExpression, pyqtSlot
from PyQt5.QtGui import QRegularExpressionValidator

from designs.centralWidget import Ui_MainWindow
from plotter import PlotCanvas

EPS = 1e-5


class mywindow(QMainWindow):
    def __init__(self, plotter: PlotCanvas):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.plotter = plotter
        self.setup_ui()
        self.graph_checkboxes = {}

    def setup_ui(self):
        self.ui.setupUi(self)
        self.setup_validators()
        self.setup_buttons()
        self.ui.gridLayout.addWidget(self.plotter, 0, 0, 1, 4)

    def setup_validators(self):
        positive_integer = QRegularExpression(r"\d+")
        positive_integer_validator = QRegularExpressionValidator(positive_integer)

        rational = QRegularExpression(r"-?\d+\.\d+")
        rational_validator = QRegularExpressionValidator(rational)

        self.ui.x0_Input.setValidator(rational_validator)
        self.ui.y0_Input.setValidator(rational_validator)
        self.ui.x_Input.setValidator(rational_validator)
        self.ui.n_Input.setValidator(positive_integer_validator)
        self.ui.n0_error_Input.setValidator(positive_integer_validator)
        self.ui.n_error_Input.setValidator(positive_integer_validator)

    def setup_buttons(self):
        self.ui.reset_input_Button.clicked.connect(self.reset_input)
        self.ui.solutions_Button.clicked.connect(self.draw)
        # self.ui.error_Button.clicked.connect.(drawing function)

    def reset_input(self):
        self.ui.x0_Input.setText("1")
        self.ui.y0_Input.setText("2")
        self.ui.x_Input.setText("6")
        self.ui.n_Input.setText("100")
        self.ui.f_Input.setText("(1+y/x)*log(1+y/x) + y/x")
        self.ui.y_exact_Input.setText("x * (pow (y_0/x_0 + 1, x/x_0) - 1 )")

    def add_graph_checkbox(self, method_name: str, color: str):
        tmp = QCheckBox(method_name)
        tmp.setStyleSheet("QCheckBox { color: " + color + "}")
        tmp.setChecked(True)
        tmp.stateChanged.connect(self.update_plot)
        self.ui.checkbox_Layout.addWidget(tmp)
        self.graph_checkboxes[method_name] = tmp

    def clear_graph_checkbox(self):
        for i in reversed(range(1, self.ui.checkbox_Layout.count())):
            self.ui.checkbox_Layout.itemAt(i).widget().setParent(None)
        self.graph_checkboxes.clear()

    def notify_mistake(self, message: str, line_edit: Optional[QLineEdit]):
        QMessageBox.warning(self, 'Invalid input', message, QMessageBox.Ok,
                            QMessageBox.Ok)
        if line_edit is not None:
            line_edit.setFocus()
            line_edit.selectAll()

    def validate_input(self, data: dict):
        # data = self.get_input()
        if data['graph']['x_0'] > data['graph']['x']:
            self.notify_mistake("X<sub>0</sub> is greater than X", self.ui.x_Input)
            return False

        if data['error']['n_0'] > data['error']['n']:
            self.notify_mistake("N<sub>0</sub> is greater than N", self.ui.n_error_Input)
            return False

        x_0 = data['graph']['x_0']
        y_0 = data['graph']['y_0']
        y = data['graph']['y']
        try:
            if abs(y_0 - y(x_0)) > EPS:
                print(y(x_0), y_0)
                self.notify_mistake("Given exact solution does not correspond to the IVP", self.ui.y_exact_Input)
                return False
        except Exception as e:
            self.notify_mistake(f"An error occured while parsing the exact solution:\n\"{e}\"", self.ui.y_exact_Input)
            return False

        return True

    def get_input(self):
        try:
            inp = {
                "graph": {
                    "x_0": float(self.ui.x0_Input.text()),
                    "y_0": float(self.ui.y0_Input.text()),
                    "x": float(self.ui.x_Input.text()),
                    "n": int(self.ui.n_Input.text())
                },

                "error": {
                    "n_0": int(self.ui.n0_error_Input.text()),
                    "n": int(self.ui.n_error_Input.text())
                }
            }
        except ValueError:
            self.notify_mistake("Some of input fields are empty.", None)
        ivp = {
            "x_0": inp['graph']['x_0'],
            "y_0": inp['graph']['y_0'],
        }
        inp["graph"]["y"] = lambda x: eval(self.ui.y_exact_Input.text(),
                                           locals().update(ivp)
                                           )
        inp["graph"]["f"] = lambda x, y: eval(self.ui.f_Input.text(),
                                              locals().update(ivp)
                                              )

        self.validate_input(inp)
        return inp

    @pyqtSlot()
    def draw(self):
        input_data = self.get_input()
        self.clear_graph_checkbox()
        for name, color in self.plotter.plot(input_data):
            self.add_graph_checkbox(name, color)

    @pyqtSlot()
    def update_plot(self):
        self.plotter.change_visibility(self.sender().text(), self.sender().isChecked())


app = QApplication([])
