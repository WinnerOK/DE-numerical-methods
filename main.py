from sys import exit

from application import app, mywindow
from plotter import PlotCanvas
import calculators

plot_canvas = PlotCanvas(dpi=75)
plot_canvas.add_exact_solution(calculators.Exact)
plot_canvas.add_solution(calculators.Euler)

application = mywindow(plotter=plot_canvas)
application.showMinimized()


exit(app.exec())
