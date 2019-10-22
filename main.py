from sys import exit

from application import app, mywindow

application = mywindow()
application.showMinimized()

exit(app.exec())
