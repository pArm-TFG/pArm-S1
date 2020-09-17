# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InProgressGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from .Interface import *
from pyqtgraph import PlotWidget
import pyqtgraph


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 600))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(212, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        MainWindow.setPalette(palette)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Slider1 = QtWidgets.QSlider(self.centralwidget)
        self.Slider1.setGeometry(QtCore.QRect(30, 110, 371, 22))
        self.Slider1.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.Slider1.setOrientation(QtCore.Qt.Horizontal)
        self.Slider1.setObjectName("Slider1")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(520, 10, 20, 541))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.SubtitleLeftLabel = QtWidgets.QLabel(self.centralwidget)
        self.SubtitleLeftLabel.setGeometry(QtCore.QRect(160, 20, 231, 31))
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
        self.SubtitleRightLabel.setGeometry(QtCore.QRect(650, 20, 231, 31))
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
        self.Slider2.setGeometry(QtCore.QRect(30, 240, 371, 22))
        self.Slider2.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.Slider2.setOrientation(QtCore.Qt.Horizontal)
        self.Slider2.setObjectName("Slider2")
        self.Slider3 = QtWidgets.QSlider(self.centralwidget)
        self.Slider3.setGeometry(QtCore.QRect(30, 370, 371, 22))
        self.Slider3.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.Slider3.setOrientation(QtCore.Qt.Horizontal)
        self.Slider3.setObjectName("Slider3")
        self.comboBoxCoordinates = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxCoordinates.setGeometry(QtCore.QRect(30, 450, 221, 41))
        self.comboBoxCoordinates.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.comboBoxCoordinates.setObjectName("comboBoxCoordinates")
        self.comboBoxCoordinates.addItem("")
        self.comboBoxCoordinates.addItem("")
        self.ExecuteButton = QtWidgets.QPushButton(self.centralwidget)
        self.ExecuteButton.setGeometry(QtCore.QRect(280, 450, 221, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ExecuteButton.setFont(font)
        self.ExecuteButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ExecuteButton.setObjectName("ExecuteButton")
        self.SliderLabel1 = QtWidgets.QLabel(self.centralwidget)
        self.SliderLabel1.setGeometry(QtCore.QRect(30, 70, 291, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SliderLabel1.setFont(font)
        self.SliderLabel1.setObjectName("SliderLabel1")
        self.SliderLabel2 = QtWidgets.QLabel(self.centralwidget)
        self.SliderLabel2.setGeometry(QtCore.QRect(30, 200, 291, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SliderLabel2.setFont(font)
        self.SliderLabel2.setObjectName("SliderLabel2")
        self.SliderLabel3 = QtWidgets.QLabel(self.centralwidget)
        self.SliderLabel3.setGeometry(QtCore.QRect(30, 330, 301, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SliderLabel3.setFont(font)
        self.SliderLabel3.setObjectName("SliderLabel3")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 530, 471, 21))
        self.progressBar.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.doubleSpinBox1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox1.setGeometry(QtCore.QRect(420, 100, 81, 31))
        self.doubleSpinBox1.setObjectName("doubleSpinBox1")
        self.doubleSpinBox2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox2.setGeometry(QtCore.QRect(420, 230, 81, 31))
        self.doubleSpinBox2.setObjectName("doubleSpinBox2")
        self.doubleSpinBox3 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox3.setGeometry(QtCore.QRect(420, 360, 81, 31))
        self.doubleSpinBox3.setObjectName("doubleSpinBox3")
        self.subLabel1 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel1.setGeometry(QtCore.QRect(30, 150, 91, 16))
        self.subLabel1.setObjectName("subLabel1")
        self.subLabel2 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel2.setGeometry(QtCore.QRect(380, 150, 71, 16))
        self.subLabel2.setObjectName("subLabel2")
        self.subLabel3 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel3.setGeometry(QtCore.QRect(30, 280, 81, 16))
        self.subLabel3.setObjectName("subLabel3")
        self.subLabel4 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel4.setGeometry(QtCore.QRect(380, 280, 71, 16))
        self.subLabel4.setObjectName("subLabel4")
        self.subLabel5 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel5.setGeometry(QtCore.QRect(30, 410, 81, 16))
        self.subLabel5.setObjectName("subLabel5")
        self.subLabel6 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel6.setGeometry(QtCore.QRect(380, 410, 81, 16))
        self.subLabel6.setObjectName("subLabel6")
        self.subLabel7 = QtWidgets.QLabel(self.centralwidget)
        self.subLabel7.setGeometry(QtCore.QRect(210, 280, 81, 16))
        self.subLabel7.setObjectName("subLabel7")
        self.topView = PlotWidget(self.centralwidget)
        self.topView.setGeometry(QtCore.QRect(580, 80, 351, 171))
        self.topView.setObjectName("topView")
        self.sideView = PlotWidget(self.centralwidget)
        self.sideView.setGeometry(QtCore.QRect(580, 280, 351, 171))
        self.sideView.setObjectName("sideView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(580, 60, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(580, 260, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.loggerBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.loggerBox.setGeometry(QtCore.QRect(580, 480, 351, 71))
        self.loggerBox.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.loggerBox.setObjectName("loggerBox")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 460, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
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

        # Grouped widgets in order to ease parameter passing

        sliders = [self.Slider1,self.Slider2, self.Slider3]
        spinBoxes = [self.doubleSpinBox1, self.doubleSpinBox2, self.doubleSpinBox3]
        slidersLabels = [self.SliderLabel1, self.SliderLabel2, self.SliderLabel3, self.subLabel1, self.subLabel2, self.subLabel3, self.subLabel4, self.subLabel5, self.subLabel6, self.subLabel7]

        # Extra setting initialization
        
        self.Slider1.setMaximum(1510)
        self.Slider1.setMinimum(0)
        self.Slider1.setTickInterval(377)
        self.Slider1.setTickPosition(3)

        self.Slider2.setMaximum(1350)
        self.Slider2.setMinimum(0)
        self.Slider2.setTickInterval(337)
        self.Slider2.setTickPosition(3)

        self.Slider3.setMaximum(1200)
        self.Slider3.setMinimum(0)
        self.Slider3.setTickInterval(300)
        self.Slider3.setTickPosition(3)

        # Extra setting initialization

        self.Slider1.valueChanged.connect(lambda: adjustWidgetValue("slider", self.Slider1, self.doubleSpinBox1))
        self.Slider2.valueChanged.connect(lambda: adjustWidgetValue("slider", self.Slider2, self.doubleSpinBox2))
        self.Slider3.valueChanged.connect(lambda: adjustWidgetValue("slider", self.Slider3, self.doubleSpinBox3))

        self.doubleSpinBox1.setRange(0,151.0)
        self.doubleSpinBox1.setSingleStep(0.1)
        self.doubleSpinBox2.setRange(0,135.0)
        self.doubleSpinBox2.setSingleStep(0.1)
        self.doubleSpinBox3.setRange(0,120.0)
        self.doubleSpinBox3.setSingleStep(0.1)

        self.doubleSpinBox1.valueChanged.connect(lambda: adjustWidgetValue("spinBox", self.Slider1, self.doubleSpinBox1))
        self.doubleSpinBox2.valueChanged.connect(lambda: adjustWidgetValue("spinBox", self.Slider2, self.doubleSpinBox2))
        self.doubleSpinBox3.valueChanged.connect(lambda: adjustWidgetValue("spinBox", self.Slider3, self.doubleSpinBox3))

        self.subLabel7.hide()

        #self.comboBoxCoordinates.highlighted.connect(lambda index: CoordinatesHighlight(self.comboBoxCoordinates, slidersLabels, sliders, spinBoxes, index))
        self.comboBoxCoordinates.activated.connect(lambda index: changeCoordinateMenu(self.comboBoxCoordinates, slidersLabels, sliders, spinBoxes, index))

        if getattr(self.ExecuteButton, "State", None) is None:
            setattr(self.ExecuteButton,"State", True)
        self.ExecuteButton.clicked.connect(lambda: executeMovement(self.ExecuteButton,self.loggerBox))

        self.loggerBox.setReadOnly(1)
        self.loggerBox.insertPlainText("Welcome to the p-Arm GUI!!\nThe arm is now being initialized...\n")
        self.loggerBox.ensureCursorVisible()

        self.topView.setBackground("w")
        self.sideView.setBackground("w")

        self.topView.setXRange(-400, 400, padding = 0)
        self.topView.setYRange(400,0, padding = 0)
        #self.topView.getPlotItem().hideAxis('bottom')
        #self.topView.getPlotItem().hideAxis('left')
        pen = pyqtgraph.mkPen(color=(255, 0, 0), width=10)
        self.topView.plot((-346,0), (0,0), pen = pen)
        self.topView.setTitle("Top View")
       

    

        #self.graphicsView.setBackground("w")
        #self.graphicsView_2.setBackground("w")
        #self.graphicsView.setXRange((-1,1))

        #self.graphicsView.getPlotItem().hideAxis('bottom')
        #self.graphicsView.getPlotItem().hideAxis('left')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "p-Arm Movement Control GUI"))
        self.SubtitleLeftLabel.setText(_translate("MainWindow", "Position Control Sliders"))
        self.SubtitleRightLabel.setText(_translate("MainWindow", "Arm Position Preview"))
        self.comboBoxCoordinates.setItemText(0, _translate("MainWindow", "Angular Position Control"))
        self.comboBoxCoordinates.setItemText(1, _translate("MainWindow", "Cartesian Position Control"))
        self.ExecuteButton.setText(_translate("MainWindow", "Execute Movement"))
        self.SliderLabel1.setText(_translate("MainWindow", "Base Servo"))
        self.SliderLabel2.setText(_translate("MainWindow", "Elbow Servo"))
        self.SliderLabel3.setText(_translate("MainWindow", "Shoulder Servo"))
        self.subLabel1.setText(_translate("MainWindow", "0º"))
        self.subLabel2.setText(_translate("MainWindow", "151º"))
        self.subLabel3.setText(_translate("MainWindow", "0º"))
        self.subLabel4.setText(_translate("MainWindow", "135º"))
        self.subLabel5.setText(_translate("MainWindow", "0º"))
        self.subLabel6.setText(_translate("MainWindow", "120º"))
        self.subLabel7.setText(_translate("MainWindow", "0.0mm"))
        self.label.setText(_translate("MainWindow", "Top View"))
        self.label_2.setText(_translate("MainWindow", "Side View"))
        self.label_3.setText(_translate("MainWindow", "Output Log"))
        self.menuPort_Selection.setTitle(_translate("MainWindow", "Port Selection"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
