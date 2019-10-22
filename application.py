from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QRegularExpression, pyqtSlot
from PyQt5.QtGui import QRegularExpressionValidator

from designs.centralWidget import Ui_MainWindow


class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.setup_ui()

    def setup_ui(self):
        self.ui.setupUi(self)
        self.setup_validators()
        self.setup_buttons()

    def setup_validators(self):
        positive_integer = QRegularExpression(r"\d+")
        positive_integer_validator = QRegularExpressionValidator(positive_integer, self.ui.input_Layout)

        rational = QRegularExpression(r"-?\d+.\d*")
        rational_validator = QRegularExpressionValidator(rational, self.ui.input_Layout)

        self.ui.x0_Input.setValidator(rational_validator)
        self.ui.y0_Input.setValidator(rational_validator)
        self.ui.x_Input.setValidator(rational_validator)
        self.ui.n_Input.setValidator(positive_integer_validator)

    def setup_buttons(self):
        self.ui.reset_Button.clicked.connect(self.reset_input)
        self.ui.solutions_Button.clicked.connect(self.draw)
        # self.ui.error_Button.clicked.connect.(drawing function)

    def reset_input(self):
        self.ui.x0_Input.setText("1")
        self.ui.y0_Input.setText("2")
        self.ui.x_Input.setText("6")
        self.ui.n_Input.setText("100")

    def validate_input(self):
        try:
            if int(self.ui.x0_Input.text()) > int(self.ui.x_Input.text()):
                QMessageBox.warning(self, 'Invalid input', "X<sub>0</sub> is greater than X", QMessageBox.Ok,
                                    QMessageBox.Ok)
                self.ui.x_Input.setFocus()
                self.ui.x_Input.selectAll()
                return False
        except ValueError:
            QMessageBox.warning(self, 'Invalid input', "Some field contain non integer literals", QMessageBox.Ok,
                                QMessageBox.Ok)
            return False
        return True

    @pyqtSlot()
    def draw(self):
        print(self.validate_input(), self.sender().objectName())


app = QApplication([])
