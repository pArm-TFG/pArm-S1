from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
from .Interface import *
import os
import pyqtgraph

class Ui(QtWidgets.QMainWindow):
    def __init__(self):

        super(Ui, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), "InProgressGUI.ui"), self)

        #Left Window Section
        self.slider_1 = self.findChild(QtWidgets.QSlider, 'Slider1')
        self.slider_2 = self.findChild(QtWidgets.QSlider, 'Slider2')
        self.slider_3 = self.findChild(QtWidgets.QSlider, 'Slider3')

        self.spin_box_1 = self.findChild(QtWidgets.QDoubleSpinBox, 'SpinBox1')
        self.spin_box_2 = self.findChild(QtWidgets.QDoubleSpinBox, 'SpinBox2')
        self.spin_box_3 = self.findChild(QtWidgets.QDoubleSpinBox, 'SpinBox3')

        self.execute_button = self.findChild(QtWidgets.QPushButton, 'ExecuteButton')
        
        self.combo_box_coordinates = self.findChild(QtWidgets.QComboBox, 'ComboBoxCoordinates')

        self.logger_box =  self.findChild(QtWidgets.QPlainTextEdit, 'LoggerBox')

        self.slider_1_label = self.findChild(QtWidgets.QLabel, 'SliderLabel1')
        self.slider_2_label = self.findChild(QtWidgets.QLabel, 'SliderLabel2')
        self.slider_3_label = self.findChild(QtWidgets.QLabel, 'SliderLabel3')
        self.slider_1_left_label = self.findChild(QtWidgets.QLabel, 'LeftLabelSlider1')
        self.slider_2_left_label = self.findChild(QtWidgets.QLabel, 'LeftLabelSlider2')
        self.slider_3_left_label = self.findChild(QtWidgets.QLabel, 'LeftLabelSlider3')
        self.slider_1_right_label = self.findChild(QtWidgets.QLabel, 'RightLabelSlider1')
        self.slider_2_right_label = self.findChild(QtWidgets.QLabel, 'RightLabelSlider2')
        self.slider_3_right_label = self.findChild(QtWidgets.QLabel, 'RightLabelSlider3')
        self.slider_2_mid_label = self.findChild(QtWidgets.QLabel, 'MidLabelSlider2')

        self.progress_bar = self.findChild(QtWidgets.QProgressBar, 'ProgressBar')

        #Right Window Section
        self.logger_box =  self.findChild(QtWidgets.QPlainTextEdit, 'LoggerBox')

        self.top_view = self.findChild(PlotWidget, 'TopView')
        self.side_view = self.findChild(PlotWidget, 'SideView')


        
    def setupGUI(self):
        # Grouped widgets in order to ease parameter passing
        sliders = [self.slider_1,self.slider_2, self.slider_3]
        spinBoxes = [self.spin_box_1, self.spin_box_2, self.spin_box_3]
        slidersLabels = [self.slider_1_label, self.slider_2_label, self.slider_3, self.slider_1_left_label, self.slider_1_right_label, self.slider_2_left_label, self.slider_2_right_label, self.slider_3_left_label, self.slider_3_right_label, self.slider_2_mid_label]

        # Extra setting initialization
        self.slider_1.setMaximum(1510)
        self.slider_1.setMinimum(0)
        self.slider_1.setTickInterval(377)
        self.slider_1.setTickPosition(3)

        self.slider_2.setMaximum(1350)
        self.slider_2.setMinimum(0)
        self.slider_2.setTickInterval(337)
        self.slider_2.setTickPosition(3)

        self.slider_3.setMaximum(1200)
        self.slider_3.setMinimum(0)
        self.slider_3.setTickInterval(300)
        self.slider_3.setTickPosition(3)

        # Extra setting initialization
        self.slider_1.valueChanged.connect(lambda: adjustWidgetValue("slider", self.slider_1, self.spin_box_1,self.top_view))
        self.slider_2.valueChanged.connect(lambda: adjustWidgetValue("slider", self.slider_2, self.spin_box_2,self.top_view))
        self.slider_3.valueChanged.connect(lambda: adjustWidgetValue("slider", self.slider_3, self.spin_box_3,self.top_view))

        self.spin_box_1.setRange(0,151.0)
        self.spin_box_1.setSingleStep(0.1)
        self.spin_box_2.setRange(0,135.0)
        self.spin_box_2.setSingleStep(0.1)
        self.spin_box_3.setRange(0,120.0)
        self.spin_box_3.setSingleStep(0.1)

        self.spin_box_1.valueChanged.connect(lambda: adjustWidgetValue("spinBox", self.slider_1, self.spin_box_1,self.top_view))
        self.spin_box_2.valueChanged.connect(lambda: adjustWidgetValue("spinBox", self.slider_2, self.spin_box_2,self.top_view))
        self.spin_box_3.valueChanged.connect(lambda: adjustWidgetValue("spinBox", self.slider_3, self.spin_box_3,self.top_view))

        self.slider_2_mid_label.hide()

        #self.comboBoxCoordinates.highlighted.connect(lambda index: CoordinatesHighlight(self.comboBoxCoordinates, slidersLabels, sliders, spinBoxes, index))
        self.combo_box_coordinates.activated.connect(lambda index: changeCoordinateMenu(self.combo_box_coordinates, slidersLabels, sliders, spinBoxes, index))

        if getattr(self.execute_button, "State", None) is None:
            setattr(self.execute_button,"State", True)
        self.execute_button.clicked.connect(lambda: executeMovement(self.execute_button,self.logger_box))

        self.logger_box.setReadOnly(1)
        self.logger_box.insertPlainText("Welcome to the p-Arm GUI!!\nThe arm is now being initialized...\n")
        self.logger_box.ensureCursorVisible()

        self.top_view.setBackground("w")
        self.side_view.setBackground("w")

        self.top_view.setXRange(-400, 400, padding = 0)
        self.top_view.setYRange(400,0, padding = 0)
        pen = pyqtgraph.mkPen(color=(255, 0, 0), width=10)
        self.top_view.plot((-346,0), (0,0), pen = pen)
        self.top_view.setTitle("Top View")
       


