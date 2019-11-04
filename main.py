from sys import exit

from application import app, MainWindow
from PlotCanvas import PlotCanvas
import calculators

application = MainWindow(PlotCanvas())
application.plotter.add_exact_solution(calculators.Exact)
application.plotter.add_solution(calculators.Euler)
application.plotter.add_solution(calculators.ImprovedEuler)
application.plotter.add_solution(calculators.RungeKutta)

application.showMaximized()

exit(app.exec())
