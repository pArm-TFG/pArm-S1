from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
#from .Interface import *
from PyQt5.QtWidgets import QMessageBox
import os
import math
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
        self.slider_1.valueChanged.connect(lambda: self.adjustWidgetValue("slider", self.slider_1, self.spin_box_1,self.top_view))
        self.slider_2.valueChanged.connect(lambda: self.adjustWidgetValue("slider", self.slider_2, self.spin_box_2,self.top_view))
        self.slider_3.valueChanged.connect(lambda: self.adjustWidgetValue("slider", self.slider_3, self.spin_box_3,self.top_view))

        self.spin_box_1.setRange(0,151.0)
        self.spin_box_1.setSingleStep(0.1)
        self.spin_box_2.setRange(0,135.0)
        self.spin_box_2.setSingleStep(0.1)
        self.spin_box_3.setRange(0,120.0)
        self.spin_box_3.setSingleStep(0.1)

        self.spin_box_1.valueChanged.connect(lambda: self.adjustWidgetValue("spinBox", self.slider_1, self.spin_box_1,self.top_view))
        self.spin_box_2.valueChanged.connect(lambda: self.adjustWidgetValue("spinBox", self.slider_2, self.spin_box_2,self.top_view))
        self.spin_box_3.valueChanged.connect(lambda: self.adjustWidgetValue("spinBox", self.slider_3, self.spin_box_3,self.top_view))

        self.slider_2_mid_label.hide()

        #self.comboBoxCoordinates.highlighted.connect(lambda index: CoordinatesHighlight(self.comboBoxCoordinates, slidersLabels, sliders, spinBoxes, index))
        self.combo_box_coordinates.activated.connect(lambda index: self.changeCoordinateMenu(self.combo_box_coordinates, slidersLabels, sliders, spinBoxes, index))

        if getattr(self.execute_button, "State", None) is None:
            setattr(self.execute_button,"State", True)
        self.execute_button.clicked.connect(lambda: self.executeMovement(self.execute_button,self.logger_box))

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
       
    def adjustWidgetValue(self,type, slider: QtWidgets.QSlider, spinBoxDouble: QtWidgets.QDoubleSpinBox, screen: QtWidgets.QGraphicsView):
        if type == "slider":
            spinBoxDouble.setValue(slider.value()/10)
            self.drawTopViewFromAngle(screen,spinBoxDouble)
        elif type == "spinBox":
            slider.setSliderPosition(spinBoxDouble.value()*10)
            self.drawTopViewFromAngle(screen,spinBoxDouble)

    def labelColorChange(self,label: QtWidgets.QLabel,r, g, b):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(r, g, b))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        label.setPalette(palette)

    def setAngularHighlight(self,slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):
        slidersLabels[0].setText("Base Servo Angle")
        slidersLabels[1].setText("Shoulder Servo Angle")
        slidersLabels[2].setText("Elbow Servo Angle")   
        labelColorChange(slidersLabels[0],245,110,110)
        labelColorChange(slidersLabels[1],245,110,110)
        labelColorChange(slidersLabels[2],245,110,110)

    def setCartesianHighLight(self,slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):
        slidersLabels[0].setText("X Coordinate")
        slidersLabels[1].setText("Y Coordinate")
        slidersLabels[2].setText("Z Coordinate")
        labelColorChange(slidersLabels[0],245,110,110)
        labelColorChange(slidersLabels[1],245,110,110)
        labelColorChange(slidersLabels[2],245,110,110)

    def setAngularMenu(self,slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):
        labelColorChange(slidersLabels[0],212,0,0)
        labelColorChange(slidersLabels[1],212,0,0)
        labelColorChange(slidersLabels[2],212,0,0)

        slidersLabels[0].setText("Base Servo Angle")
        slidersLabels[1].setText("Shoulder Servo Angle")
        slidersLabels[2].setText("Elbow Servo Angle")
        slidersLabels[3].setText("0º")
        slidersLabels[4].setText("151º")
        slidersLabels[5].setText("0º")
        slidersLabels[6].setText("135º")
        slidersLabels[7].setText("0º")
        slidersLabels[8].setText("120º")
        slidersLabels[9].hide()

        sliders[0].setMaximum(1510)
        sliders[0].setMinimum(0)
        sliders[0].setTickInterval(377)
        sliders[0].setSliderPosition(0)
        spinBoxes[0].setRange(0,151.0)
        spinBoxes[0].setValue(0.0)

        sliders[1].setMaximum(1350)
        sliders[1].setMinimum(0)
        sliders[1].setTickInterval(337)
        sliders[1].setSliderPosition(0)
        spinBoxes[1].setRange(0,135.0)
        spinBoxes[1].setValue(0.0)

        sliders[2].setMaximum(1200)
        sliders[2].setMinimum(0)
        sliders[2].setTickInterval(300)
        sliders[2].setSliderPosition(0)
        spinBoxes[2].setRange(0,120.0)
        spinBoxes[2].setValue(0.0)    

    def setCartesianMenu(self,slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):   
        labelColorChange(slidersLabels[0],212,0,0)
        labelColorChange(slidersLabels[1],212,0,0)
        labelColorChange(slidersLabels[2],212,0,0)

        slidersLabels[0].setText("X Coordinate")
        slidersLabels[1].setText("Y Coordinate")
        slidersLabels[2].setText("Z Coordinate")
        slidersLabels[3].setText("0.0mm")
        slidersLabels[4].setText("346.0mm")
        slidersLabels[5].setText("-346.0mm")
        slidersLabels[6].setText("346.0mm")
        slidersLabels[7].setText("0.0mm")
        slidersLabels[8].setText("360.6mm")
        slidersLabels[9].show()

        sliders[0].setMaximum(3460)
        sliders[0].setMinimum(0)
        sliders[0].setTickInterval(865)
        sliders[0].setSliderPosition(0)
        spinBoxes[0].setRange(0,346.0)
        spinBoxes[0].setValue(0.0)

        sliders[1].setMaximum(3460)
        sliders[1].setMinimum(-3460)
        sliders[1].setTickInterval(1730)
        sliders[1].setSliderPosition(0)
        spinBoxes[1].setRange(-346.0,346.0)
        spinBoxes[1].setValue(0.0)

        sliders[2].setMaximum(3606)
        sliders[2].setMinimum(0)
        sliders[2].setTickInterval(901) 
        sliders[2].setSliderPosition(0)
        spinBoxes[2].setRange(0,360.6)
        spinBoxes[2].setValue(0.0)    

    def CoordinatesHighlight(self,comboBox: QtWidgets.QComboBox, slidersLabels: QtWidgets.QLabel,sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox, index):
        if index == 1 :
            setCartesianHighLight(slidersLabels,sliders,spinBoxes) 
        elif index == 0 :
            setAngularHighlight(slidersLabels,sliders,spinBoxes)
        
    def changeCoordinateMenu(self,comboBox: QtWidgets.QComboBox, slidersLabels: QtWidgets.QLabel,sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox, index):
        if index == 1 : 
            setCartesianMenu(slidersLabels, sliders, spinBoxes)
        elif index == 0 : 
            setAngularMenu(slidersLabels, sliders, spinBoxes)
        
    def show_popup(self,message: str):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText(message)
        msg.setIcon(2)
        x = msg.exec_()   
  
    def executeMovement(self,button : QtWidgets.QPushButton, logger: QtWidgets.QPlainTextEdit):
        if button.State is True :
            button.setText("Cancel movement")
            button.State = False
            #Execute movement Logic code here
        else:
            show_popup("Movement Cancelled")
            logger.insertPlainText("Movement Cancelled\n")
            logger.ensureCursorVisible()
            button.setText("Execute Movement")
            button.State = True  
            #Cancel movement Logic code here

    def drawTopViewFromAngle(self,screen: QtWidgets.QGraphicsView, spinBox: QtWidgets.QDoubleSpinBox):
        pen = pyqtgraph.mkPen(color=(255, 0, 0), width=10)
        x_f = 346*math.cos((180 - spinBox.value())*(math.pi/180))
        y_f = 346*math.sin((180 - spinBox.value())*(math.pi/180))
        screen.clear()
        screen.plot((0, x_f),(0,y_f), pen=pen)    

   