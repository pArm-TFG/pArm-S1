# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(971, 549)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Slider1 = QtWidgets.QSlider(self.centralwidget)
        self.Slider1.setGeometry(QtCore.QRect(280, 150, 341, 81))
        self.Slider1.setOrientation(QtCore.Qt.Horizontal)
        self.Slider1.setObjectName("Slider1")
        self.Slider1.setMaximum(180)
        self.Slider1.setMinimum(0)
        self.Slider1.sliderMoved.connect(lambda: self.sliderEvent("Moving"))
        self.Slider1.sliderPressed.connect(lambda: self.sliderEvent("Now Pressed"))
        self.Slider1.sliderReleased.connect(lambda: self.sliderEvent("Now Released"))
        self.Slider1.valueChanged.connect(lambda: self.sliderEvent("Position change"))
        self.Slider1.setTickInterval(45)
        self.Slider1.setTickPosition(1)
     
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 300, 151, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_popup)

        self.SpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.SpinBox.setGeometry(QtCore.QRect(660, 170, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.SpinBox.setFont(font)
        self.SpinBox.setObjectName("SpinBox")
        self.SpinBox.setRange(0,180)
        self.SpinBox.valueChanged.connect(self.spinBoxEvent)


        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(520, 320, 118, 23))
        self.progressBar.setProperty("value",0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 971, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Javi se las come dobladas"))

    def sliderEvent(self, text):
        self.pushButton.setText(text)
        self.SpinBox.setValue(self.Slider1.value())
        self.progressBar.setProperty("value",(self.Slider1.value() / 180)*100)

    def spinBoxEvent(self):
        self.Slider1.setSliderPosition(self.SpinBox.value())
        self.progressBar.setProperty("value",(self.Slider1.value() / 180)*100)

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText("Something happened")
        x = msg.exec_()    

     


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
