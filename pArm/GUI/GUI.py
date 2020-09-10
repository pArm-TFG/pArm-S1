# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InProgressGUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Interface import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 600))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        MainWindow.setPalette(palette)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.TitleLabel.setGeometry(QtCore.QRect(310, -10, 401, 81))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.TitleLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.Slider1 = QtWidgets.QSlider(self.centralwidget)
        self.Slider1.setGeometry(QtCore.QRect(50, 170, 361, 22))
        self.Slider1.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.Slider1.setOrientation(QtCore.Qt.Horizontal)
        self.Slider1.setObjectName("Slider1")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(493, 80, 20, 481))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.SubtitleLeftLabel = QtWidgets.QLabel(self.centralwidget)
        self.SubtitleLeftLabel.setGeometry(QtCore.QRect(160, 70, 231, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.SubtitleLeftLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.SubtitleLeftLabel.setFont(font)
        self.SubtitleLeftLabel.setObjectName("SubtitleLeftLabel")
        self.SubtitleRightLabel = QtWidgets.QLabel(self.centralwidget)
        self.SubtitleRightLabel.setGeometry(QtCore.QRect(670, 70, 231, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.SubtitleRightLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.SubtitleRightLabel.setFont(font)
        self.SubtitleRightLabel.setObjectName("SubtitleRightLabel")
        self.Slider2 = QtWidgets.QSlider(self.centralwidget)
        self.Slider2.setGeometry(QtCore.QRect(50, 290, 361, 22))
        self.Slider2.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.Slider2.setOrientation(QtCore.Qt.Horizontal)
        self.Slider2.setObjectName("Slider2")
        self.Slider3 = QtWidgets.QSlider(self.centralwidget)
        self.Slider3.setGeometry(QtCore.QRect(50, 410, 361, 22))
        self.Slider3.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.Slider3.setOrientation(QtCore.Qt.Horizontal)
        self.Slider3.setObjectName("Slider3")
        self.comboBoxCoordinates = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxCoordinates.setGeometry(QtCore.QRect(20, 490, 151, 41))
        self.comboBoxCoordinates.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.comboBoxCoordinates.setObjectName("comboBoxCoordinates")
        self.comboBoxCoordinates.addItem("")
        self.comboBoxCoordinates.addItem("")
        self.executeButton = QtWidgets.QPushButton(self.centralwidget)
        self.executeButton.setGeometry(QtCore.QRect(210, 490, 121, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.executeButton.setFont(font)
        self.executeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.executeButton.setObjectName("executeButton")
        self.SliderLabel1 = QtWidgets.QLabel(self.centralwidget)
        self.SliderLabel1.setGeometry(QtCore.QRect(50, 130, 291, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SliderLabel1.setFont(font)
        self.SliderLabel1.setObjectName("SliderLabel1")
        self.SliderLabel2 = QtWidgets.QLabel(self.centralwidget)
        self.SliderLabel2.setGeometry(QtCore.QRect(50, 250, 291, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SliderLabel2.setFont(font)
        self.SliderLabel2.setObjectName("SliderLabel2")
        self.SliderLabel3 = QtWidgets.QLabel(self.centralwidget)
        self.SliderLabel3.setGeometry(QtCore.QRect(50, 370, 301, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SliderLabel3.setFont(font)
        self.SliderLabel3.setObjectName("SliderLabel3")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(20, 210, 471, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(20, 330, 471, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(20, 450, 471, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(380, 500, 118, 23))
        self.progressBar.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.progressBar.setProperty("value", 69)
        self.progressBar.setObjectName("progressBar")
        self.doubleSpinBox1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox1.setGeometry(QtCore.QRect(430, 161, 61, 31))
        self.doubleSpinBox1.setObjectName("doubleSpinBox1")
        self.doubleSpinBox2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox2.setGeometry(QtCore.QRect(430, 280, 61, 31))
        self.doubleSpinBox2.setObjectName("doubleSpinBox2")
        self.doubleSpinBox3 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox3.setGeometry(QtCore.QRect(430, 400, 61, 31))
        self.doubleSpinBox3.setObjectName("doubleSpinBox3")
        self.subLabel1 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel1.setGeometry(QtCore.QRect(50, 200, 47, 13))
        self.subLabel1.setObjectName("subLabel1")
        self.subLabel2 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel2.setGeometry(QtCore.QRect(390, 200, 47, 13))
        self.subLabel2.setObjectName("subLabel2")
        self.subLabel3 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel3.setGeometry(QtCore.QRect(50, 320, 47, 13))
        self.subLabel3.setObjectName("subLabel3")
        self.subLabel4 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel4.setGeometry(QtCore.QRect(390, 320, 47, 13))
        self.subLabel4.setObjectName("subLabel4")
        self.subLabel5 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel5.setGeometry(QtCore.QRect(50, 440, 47, 13))
        self.subLabel5.setObjectName("subLabel5")
        self.subLabel6 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel6.setGeometry(QtCore.QRect(390, 440, 47, 13))
        self.subLabel6.setObjectName("subLabel6")
        self.subLabel7 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel7.setGeometry(QtCore.QRect(223, 320, 47, 13))
        self.subLabel7.setObjectName("subLabel7")
        self.subLabel7.hide()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        self.menuPort_Selection = QtWidgets.QMenu(self.menubar)
        self.menuPort_Selection.setObjectName("menuPort_Selection")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuPort_Selection.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

         # Extra configs added by developer, this is not autogenerated code

        self.Slider1.setMaximum(1510)
        self.Slider1.setMinimum(0)
        self.Slider1.setTickInterval(377)
        self.Slider1.setTickPosition(3)
        self.Slider1.setSingleStep(10)
        self.doubleSpinBox1.setRange(0,151.0)
        self.doubleSpinBox1.setDecimals(1)
        self.doubleSpinBox1.setSingleStep(0.1)

        self.Slider2.setMaximum(1350)
        self.Slider2.setMinimum(0)
        self.Slider2.setTickInterval(337)
        self.Slider2.setTickPosition(3)
        self.Slider2.setSingleStep(10)
        self.doubleSpinBox2.setRange(0,135.0)
        self.doubleSpinBox2.setDecimals(1)
        self.doubleSpinBox2.setSingleStep(0.1)

        self.Slider3.setMaximum(1200)
        self.Slider3.setMinimum(0)
        self.Slider3.setTickInterval(300)
        self.Slider3.setTickPosition(3)
        self.Slider3.setSingleStep(10)
        self.doubleSpinBox3.setRange(0,120.0)
        self.doubleSpinBox3.setDecimals(1)
        self.doubleSpinBox3.setSingleStep(0.1)

        # Grouped widgets in order to ease parameter passing

        sliders = [self.Slider1,self.Slider2, self.Slider3]
        spinBoxes = [self.doubleSpinBox1, self.doubleSpinBox2, self.doubleSpinBox3]
        slidersLabels = [self.SliderLabel1, self.SliderLabel2, self.SliderLabel3, self.subLabel1, self.subLabel2, self.subLabel3, self.subLabel4, self.subLabel5, self.subLabel6, self.subLabel7]

        # Signal treatment for each widget

        self.Slider1.valueChanged.connect(lambda: adjustWidgetValue("slider", self.Slider1, self.doubleSpinBox1))
        self.Slider2.valueChanged.connect(lambda: adjustWidgetValue("slider", self.Slider2, self.doubleSpinBox2))
        self.Slider3.valueChanged.connect(lambda: adjustWidgetValue("slider", self.Slider3, self.doubleSpinBox3))

        self.doubleSpinBox1.valueChanged.connect(lambda: adjustWidgetValue("spinBox", self.Slider1, self.doubleSpinBox1))
        self.doubleSpinBox2.valueChanged.connect(lambda: adjustWidgetValue("spinBox", self.Slider2, self.doubleSpinBox2))
        self.doubleSpinBox3.valueChanged.connect(lambda: adjustWidgetValue("spinBox", self.Slider3, self.doubleSpinBox3))

        self.comboBoxCoordinates.highlighted.connect(lambda index: CoordinatesHighlight(self.comboBoxCoordinates, slidersLabels, sliders, spinBoxes, index))
        self.comboBoxCoordinates.activated.connect(lambda index: changeCoordinateMenu(self.comboBoxCoordinates, slidersLabels, sliders, spinBoxes, index))

        if getattr(self.executeButton, "State", None) is None:
            setattr(self.executeButton,"State", True)
        self.executeButton.clicked.connect(lambda: executeMovement(self.executeButton))

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "p-Arm GUI"))
        self.TitleLabel.setText(_translate("MainWindow", "p-Arm Movement Control GUI"))
        self.SubtitleLeftLabel.setText(_translate("MainWindow", "Position Control Sliders"))
        self.SubtitleRightLabel.setText(_translate("MainWindow", "Graphic Position Control"))
        self.comboBoxCoordinates.setItemText(0, _translate("MainWindow", "Angular Position Control"))
        self.comboBoxCoordinates.setItemText(1, _translate("MainWindow", "Cartesian Position Control"))
        self.executeButton.setText(_translate("MainWindow", "Execute Movement"))
        self.SliderLabel1.setText(_translate("MainWindow", "Base Servo Angle"))
        self.SliderLabel2.setText(_translate("MainWindow", "Elbow Servo Angle"))
        self.SliderLabel3.setText(_translate("MainWindow", "Shoulder Servo Angle"))
        self.subLabel1.setText(_translate("MainWindow", "0º"))
        self.subLabel2.setText(_translate("MainWindow", "151º"))
        self.subLabel3.setText(_translate("MainWindow", "0º"))
        self.subLabel4.setText(_translate("MainWindow", "135º"))
        self.subLabel5.setText(_translate("MainWindow", "0º"))
        self.subLabel6.setText(_translate("MainWindow", "120º"))
        self.subLabel7.setText(_translate("MainWindow", "0.0mm"))
        self.menuPort_Selection.setTitle(_translate("MainWindow", "Port Selection"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
