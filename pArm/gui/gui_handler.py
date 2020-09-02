from PyQt5 import uic, QtWidgets
from .MainWindow import Ui_MainWindow

import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../MainWindow.ui', self)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    Ui_MainWindow.x_spin.setValue(100)
    sys.exit(app.exec_())





