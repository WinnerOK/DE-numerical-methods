from sys import exit

from application import app, MainWindow
import calculators

application = MainWindow()
application.plotter.add_exact_solution(calculators.Exact)
application.plotter.add_solution(calculators.Euler)
application.plotter.add_solution(calculators.ImprovedEuler)
application.plotter.add_solution(calculators.RungeKutta)

application.showMaximized()

exit(app.exec())
