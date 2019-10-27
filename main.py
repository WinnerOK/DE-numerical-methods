from sys import exit

from application import app, MainWindow
from plotter import PlotCanvas
import calculators

plot_canvas = PlotCanvas(dpi=75)
plot_canvas.add_exact_solution(calculators.Exact)
plot_canvas.add_solution(calculators.Euler)
plot_canvas.add_solution(calculators.ImprovedEuler)
plot_canvas.add_solution(calculators.RungeKutta)

application = MainWindow(plotter=plot_canvas)
application.showMaximized()


exit(app.exec())
