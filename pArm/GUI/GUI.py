import math
import os

import pyqtgraph
import serial.tools.list_ports
import webbrowser
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QMessageBox, QMenu, QAction
from pyqtgraph import PlotWidget
from concurrent.futures import Future
from ..utils import AtomicFloat
from ..utils.error_data import ErrorData
from ..control.control_interface import ControlInterface
from .progress_widget import ProgressWidget
from .rect_item import RectItem


def inverse_kinematics(x_coord, y_coord, z_coord):
    try:
        from math import acos, atan, atan2, pi, sqrt, sin, cos
        
        x_coord = 11.5 if x_coord < 11.5 else x_coord

        al = 142.07
        au = 158.08

        theta_0 = pi - atan2(x_coord, y_coord)
        xz = (x_coord ** 2) + (y_coord**2) + (z_coord ** 2)
        lxz = sqrt(xz)
        theta_1 = acos((-1*(al ** 2) - xz + au ** 2) / (-2 * al * lxz))
        theta_2 = acos((-1*(al ** 2) - au ** 2 + xz) / (-2 * al * au))
        theta_1 += atan(z_coord/(sqrt(x_coord**2 + y_coord**2)))

        theta_0 *= (180/pi)
        theta_1 *= (180/pi)
        theta_2 *= (180/pi)
        theta_1 = 135 - theta_1
        return theta_0, theta_1, theta_2
    except ValueError:
        return None

def check_list(theta_0, theta_1, theta_2, x_coord, y_coord, z_coord):
    result = True

    if theta_0 < (180-151):
        result = False
    
    if theta_1 > 135 or theta_1 < 0:
        result = False

    if theta_2 > 120:
        result = False

    if math.sqrt(x_coord**2 + y_coord**2 + z_coord**2) > 261:    
        result = False

    if theta_2 >(theta_1 + 55):
        result = False
  
    return result


class Ui(QtGui.QMainWindow):

    def __init__(self, control: ControlInterface):
        super(Ui, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'InProgressGUI.ui'), self)

        #Logic interface
        self.handler = control

        #Serial Port used to send data to PCB
        self.port = None

        #Auxiliar Dirty Counter
        self.counter = 500

        #Left Window Section
        self.menu_port = self.findChild(QtWidgets.QMenu, 'menuPort_Selection')

        self.menu_info = self.findChild(QtWidgets.QMenu, 'menu_info')

        self.slider_1 = self.findChild(QtWidgets.QSlider, 'Slider1')
        self.slider_2 = self.findChild(QtWidgets.QSlider, 'Slider2')
        self.slider_3 = self.findChild(QtWidgets.QSlider, 'Slider3')

        self.spin_box_1 = self.findChild(QtWidgets.QDoubleSpinBox, 'SpinBox1')
        self.spin_box_2 = self.findChild(QtWidgets.QDoubleSpinBox, 'SpinBox2')
        self.spin_box_3 = self.findChild(QtWidgets.QDoubleSpinBox, 'SpinBox3')

        self.execute_button = self.findChild(QtWidgets.QPushButton, 'ExecuteButton')
        self.origin_button = self.findChild(QtWidgets.QPushButton, 'origin_button')

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

        self.progress_bar = ProgressWidget.from_bar(self.findChild(QtWidgets.QProgressBar, 'ProgressBar'))
        self.progress_bar.hide()
        
        #Right Window Section
        self.logger_box =  self.findChild(QtWidgets.QPlainTextEdit, 'LoggerBox')

        self.top_view = self.findChild(PlotWidget, 'TopView')
        self.side_view = self.findChild(PlotWidget, 'SideView')

    def setupGUI(self):
        # Grouped widgets in order to ease parameter passing
        sliders = [self.slider_1,self.slider_2, self.slider_3]
        spin_boxes = [self.spin_box_1, self.spin_box_2, self.spin_box_3]
        sliders_labels = [self.slider_1_label, self.slider_2_label, self.slider_3_label, self.slider_1_left_label, self.slider_1_right_label, self.slider_2_left_label, self.slider_2_right_label, self.slider_3_left_label, self.slider_3_right_label, self.slider_2_mid_label]
        graphics = [self.top_view, self.side_view]

        # Extra setting initialization

        if getattr(self.slider_1, "id", None) is None:
            setattr(self.slider_1,"id", 1)

        if getattr(self.slider_2, "id", None) is None:
            setattr(self.slider_2,"id", 2)

        if getattr(self.slider_3, "id", None) is None:
            setattr(self.slider_3,"id", 3)

        self.slider_1.setMaximum(1510)
        self.slider_1.setMinimum(0)
        self.slider_1.setTickInterval(377)
        self.slider_1.setTickPosition(3)
        self.slider_1.setSliderPosition(900)

        self.slider_2.setMaximum(1350)
        self.slider_2.setMinimum(0)
        self.slider_2.setTickInterval(337)
        self.slider_2.setTickPosition(3)

        self.slider_3.setMaximum(1200)
        self.slider_3.setMinimum(100)
        self.slider_3.setTickInterval(275)
        self.slider_3.setTickPosition(3)

        self.slider_1.valueChanged.connect(lambda: self.adjustWidgetValue("slider", sliders, spin_boxes, graphics, self.combo_box_coordinates.currentIndex(), 1))
        self.slider_2.valueChanged.connect(lambda: self.adjustWidgetValue("slider", sliders, spin_boxes, graphics,self.combo_box_coordinates.currentIndex(), 2))
        self.slider_3.valueChanged.connect(lambda: self.adjustWidgetValue("slider",  sliders, spin_boxes, graphics,self.combo_box_coordinates.currentIndex(), 3))

        if getattr(self.spin_box_1, "id", None) is None:
            setattr(self.spin_box_1,"id", 1)

        if getattr(self.spin_box_2, "id", None) is None:
            setattr(self.spin_box_2,"id", 2)

        if getattr(self.spin_box_3, "id", None) is None:
            setattr(self.spin_box_3,"id", 3)

        self.spin_box_1.setRange(0,151.0)
        self.spin_box_1.setSingleStep(0.1)
        self.spin_box_1.setValue(90.0)
        self.spin_box_2.setRange(0,135.0)
        self.spin_box_2.setSingleStep(0.1)
        self.spin_box_3.setRange(10.0, 120.0)
        self.spin_box_3.setSingleStep(0.1)

        self.spin_box_1.valueChanged.connect(lambda: self.adjustWidgetValue("spinBox",  sliders, spin_boxes, graphics,self.combo_box_coordinates.currentIndex(),1 ))
        self.spin_box_2.valueChanged.connect(lambda: self.adjustWidgetValue("spinBox",  sliders, spin_boxes, graphics,self.combo_box_coordinates.currentIndex(), 2))
        self.spin_box_3.valueChanged.connect(lambda: self.adjustWidgetValue("spinBox",  sliders, spin_boxes, graphics,self.combo_box_coordinates.currentIndex(), 3))

        self.slider_2_mid_label.hide()

        #self.comboBoxCoordinates.highlighted.connect(lambda index: CoordinatesHighlight(self.comboBoxCoordinates, sliders_labels, sliders, spin_boxes, index))
        self.combo_box_coordinates.activated.connect(lambda index: self.changeCoordinateMenu(self.combo_box_coordinates, sliders_labels, sliders, spin_boxes, index))

        self.menu_port.triggered.connect(lambda portID: self.setSerialPort(portID))

        self.menu_info.triggered.connect(lambda action: self.open_browser_info(action))

        if getattr(self.execute_button, "State", None) is None:
            setattr(self.execute_button,"State", True)
        self.execute_button.clicked.connect(lambda: self.executeMovement(self.execute_button,self.logger_box, spin_boxes,self.combo_box_coordinates.currentIndex()))
        self.origin_button.clicked.connect(lambda: self.move_to_origin(self.origin_button, sliders, spin_boxes, self.combo_box_coordinates.currentIndex()))

        self.logger_box.setReadOnly(1)
        self.logger_box.insertPlainText("Welcome to the p-Arm GUI!!\nThe arm is now being initialized...\n")
        self.logger_box.ensureCursorVisible()

        self.top_view.setBackground("w")
        self.side_view.setBackground("w")

        self.top_view.setXRange(-400, 400, padding = 0)
        self.top_view.setYRange(280,-120, padding = 0)
        pen = pyqtgraph.mkPen(color=(0, 255, 0), width=8, style = QtCore.Qt.SolidLine)
        self.drawViewFromAngle(graphics, spin_boxes,1)
        self.side_view.setXRange(-420, 420, padding = 0)
        self.side_view.setYRange(294, -106, padding = 0)
        self.drawViewFromAngle(graphics, spin_boxes,3)

        self.scanSerialPorts(self.menu_port)

    def adjustWidgetValue(self,type, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox, graphics: QtWidgets.QGraphicsView, index: int, id):
        if type == "slider":
            if index == 0:
                    self.drawViewFromAngle(graphics, spinBoxes, id)
            elif index == 1:
                    self.drawViewFromCartesian(graphics, spinBoxes, id)
            spinBoxes[id-1].setValue(sliders[id-1].value()/10)
        elif type == "spinBox":
            sliders[id-1].setSliderPosition(spinBoxes[id-1].value()*10)

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

    def setAngularHighlight(self,sliders_labels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spin_boxes: QtWidgets.QDoubleSpinBox):
        sliders_labels[0].setText("Base Servo Angle")
        sliders_labels[1].setText("Shoulder Servo Angle")
        sliders_labels[2].setText("Elbow Servo Angle")
        self.labelColorChange(sliders_labels[0],245,110,110)
        self.labelColorChange(sliders_labels[1],245,110,110)
        self.labelColorChange(sliders_labels[2],245,110,110)

    def setCartesianHighLight(self,sliders_labels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spin_boxes: QtWidgets.QDoubleSpinBox):
        sliders_labels[0].setText("X Coordinate")
        sliders_labels[1].setText("Y Coordinate")
        sliders_labels[2].setText("Z Coordinate")
        self.labelColorChange(sliders_labels[0],245,110,110)
        self.labelColorChange(sliders_labels[1],245,110,110)
        self.labelColorChange(sliders_labels[2],245,110,110)

    def setAngularMenu(self,sliders_labels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spin_boxes: QtWidgets.QDoubleSpinBox):
        self.labelColorChange(sliders_labels[0],212,0,0)
        self.labelColorChange(sliders_labels[1],212,0,0)
        self.labelColorChange(sliders_labels[2],212,0,0)

        self.top_view.clear()
        self.side_view.clear()

        sliders_labels[0].setText("Base Servo Angle")
        sliders_labels[1].setText("Shoulder Servo Angle")
        sliders_labels[2].setText("Elbow Servo Angle")
        sliders_labels[3].setText("0º")
        sliders_labels[4].setText("151º")
        sliders_labels[5].setText("0º")
        sliders_labels[6].setText("135º")
        sliders_labels[7].setText("10º")
        sliders_labels[8].setText("120º")
        sliders_labels[9].hide()

        sliders[0].setMaximum(1510)
        sliders[0].setMinimum(0)
        sliders[0].setTickInterval(377)
        sliders[0].setSliderPosition(0)
        spin_boxes[0].setRange(0,151.0)
        spin_boxes[0].setValue(0.0)

        sliders[1].setMaximum(1350)
        sliders[1].setMinimum(0)
        sliders[1].setTickInterval(337)
        sliders[1].setSliderPosition(0)
        spin_boxes[1].setRange(0,135.0)
        spin_boxes[1].setValue(0.0)

        sliders[2].setMaximum(1200)
        sliders[2].setMinimum(100)
        sliders[2].setTickInterval(275)
        sliders[2].setSliderPosition(0)
        spin_boxes[2].setRange(10.,110.0)
        spin_boxes[2].setValue(0.0)

    def setCartesianMenu(self,sliders_labels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spin_boxes: QtWidgets.QDoubleSpinBox):
        self.labelColorChange(sliders_labels[0],212,0,0)
        self.labelColorChange(sliders_labels[1],212,0,0)
        self.labelColorChange(sliders_labels[2],212,0,0)

        self.top_view.clear()
        self.side_view.clear()

        sliders_labels[0].setText("X Coordinate")
        sliders_labels[1].setText("Y Coordinate")
        sliders_labels[2].setText("Z Coordinate")
        sliders_labels[3].setText("0.0mm")
        sliders_labels[4].setText("346.0mm")
        sliders_labels[5].setText("-346.0mm")
        sliders_labels[6].setText("346.0mm")
        sliders_labels[7].setText("-106.1mm")
        sliders_labels[8].setText("360.6mm")
        sliders_labels[9].show()

        sliders[0].setMaximum(3460)
        sliders[0].setMinimum(0)
        sliders[0].setTickInterval(865)
        sliders[0].setSliderPosition(0)
        spin_boxes[0].setRange(0,346.0)
        spin_boxes[0].setValue(0)

        sliders[1].setMaximum(3460)
        sliders[1].setMinimum(-3460)
        sliders[1].setTickInterval(1730)
        sliders[1].setSliderPosition(0)
        spin_boxes[1].setRange(-346.0,346.0)
        spin_boxes[1].setValue(0)

        sliders[2].setMaximum(3606)
        sliders[2].setMinimum(-1061)
        sliders[2].setTickInterval(901)
        sliders[2].setSliderPosition(0)
        spin_boxes[2].setRange(-106.1,360.6)
        spin_boxes[2].setValue(0)

    def CoordinatesHighlight(self,comboBox: QtWidgets.QComboBox, sliders_labels: QtWidgets.QLabel,sliders: QtWidgets.QSlider, spin_boxes: QtWidgets.QDoubleSpinBox, index):
        if index == 1 :
            self.setCartesianHighLight(sliders_labels,sliders,spin_boxes)
        elif index == 0 :
            self.setAngularHighlight(sliders_labels,sliders,spin_boxes)

    def changeCoordinateMenu(self,comboBox: QtWidgets.QComboBox, sliders_labels: QtWidgets.QLabel,sliders: QtWidgets.QSlider, spin_boxes: QtWidgets.QDoubleSpinBox, index):
        if index == 1 :
            self.setCartesianMenu(sliders_labels, sliders, spin_boxes)
        elif index == 0 :
            self.setAngularMenu(sliders_labels, sliders, spin_boxes)

    def show_popup(self,message: str):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText(message)
        msg.setIcon(2)
        x = msg.exec_()

    def executeMovement(self,button : QtWidgets.QPushButton, logger: QtWidgets.QPlainTextEdit, spin_boxes: QtWidgets.QDoubleSpinBox, index: int):
        if button.State:
            self.progress_bar.show()
            button.setText("Cancel movement")
            button.State = False
            time_holder_val = AtomicFloat(initial_value=-1)
            self.progress_bar.run_worker(time_holder_val)
            ft = None
            if index == 0:
                ft = self.handler.move_to_thetas(spin_boxes[0].value(),
                                            spin_boxes[1].value(),
                                            spin_boxes[2].value(),
                                            time_holder_val)
                self.logger_box.insertPlainText('Sending joints to PCB: ' + str((spin_boxes[0].value(),spin_boxes[1].value(),spin_boxes[2].value())) + '\n')
            elif index == 1:
                ft = self.handler.move_to_xyz(spin_boxes[0].value(),
                                         spin_boxes[1].value(),
                                         spin_boxes[2].value(),
                                         time_holder_val)
                self.logger_box.insertPlainText('Sending coordinates to PCB: ' + str((spin_boxes[0].value(),spin_boxes[1].value(),spin_boxes[2].value())) + '\n')
            if ft:
                ft.add_done_callback(lambda future: self.future_callback(future))     
        else:
            self.progress_bar.hide()
            #self.handler.cancel_movement()
            self.show_popup("Movement Cancelled")
            self.logger_box.insertPlainText("Movement Cancelled\n")
            self.logger_box.ensureCursorVisible()
            button.setText("Execute Movement")
            button.State = True

    def drawViewFromAngle(self,graphics: QtWidgets.QGraphicsView, spinBoxes: QtWidgets.QDoubleSpinBox, id):

        theta_0, theta_1, theta_2 = spinBoxes[0].value(), spinBoxes[1].value(), spinBoxes[2].value()
        x_coord1  = 142.07*math.cos((135 - spinBoxes[1].value())*(math.pi/180))
        x_coord2  = x_coord1 + 158.81*math.cos((180 - (135 - spinBoxes[1].value()) - (spinBoxes[2].value()))*(math.pi/180))
        z_coord1 = 142.07*math.sin((135 - spinBoxes[1].value())*(math.pi/180))
        z_coord2  = z_coord1 - 158.81*math.sin((180 - (135 - spinBoxes[1].value()) - (spinBoxes[2].value()))*(math.pi/180))

        x_coord = x_coord2*math.cos((spinBoxes[0].value())*(math.pi/180))
        y_coord = x_coord2*math.sin((spinBoxes[0].value())*(math.pi/180))
        x1_coord = x_coord1*math.cos((spinBoxes[0].value())*(math.pi/180))
        y1_coord = x_coord1*math.sin((spinBoxes[0].value())*(math.pi/180))

        graphics[0].clear()
        rect_item = RectItem(QtCore.QRectF(-53.05, -53.05, 106.1, 106.1))
        graphics[0].addItem(rect_item)

        if check_list(theta_0, theta_1, theta_2, x_coord, y_coord, z_coord2):
            pen1 = pyqtgraph.mkPen(color=(0, 240, 0), width=8, style = QtCore.Qt.SolidLine)
            pen2 = pyqtgraph.mkPen(color=(0, 220,215), width=8, style = QtCore.Qt.SolidLine)
        else:
            pen1 = pyqtgraph.mkPen(color=(255, 0, 0), width=8, style = QtCore.Qt.SolidLine)
            pen2 = pyqtgraph.mkPen(color=(255, 0, 0), width=8, style = QtCore.Qt.SolidLine)   

        if(z_coord2 > z_coord1 and x_coord2 > x_coord1): # Upper arm above Lower arm
            graphics[0].plot((0,x1_coord),(0,y1_coord), pen=pen1, symbol='o',symbolSize=15, symbolBrush=('b'))
            graphics[0].plot((x1_coord,x_coord),(y1_coord,y_coord), pen=pen2, symbol='o',symbolSize=15, symbolBrush=('b'))     
        elif(z_coord2 < z_coord1 and x_coord2 < x_coord1): # Lowe arm above Upper arm
            graphics[0].plot((x1_coord,x_coord),(y1_coord,y_coord), pen=pen2, symbol='o',symbolSize=15, symbolBrush=('b'))
            graphics[0].plot((0,x1_coord),(0,y1_coord), pen=pen1, symbol='o',symbolSize=15, symbolBrush=('b'))
        else: # neutral position
            graphics[0].plot((0,x1_coord),(0,y1_coord), pen=pen1, symbol='o',symbolSize=15, symbolBrush=('b'))
            graphics[0].plot((x1_coord,x_coord),(y1_coord,y_coord), pen=pen2, symbol='o',symbolSize=15, symbolBrush=('b'))

        x_coord1  = 142.07*math.cos((135 - spinBoxes[1].value())*(math.pi/180))
        x_coord2  = x_coord1 + 158.81*math.cos((180 - (135 - spinBoxes[1].value()) - (spinBoxes[2].value()))*(math.pi/180))
        z_coord1 = 142.07*math.sin((135 - spinBoxes[1].value())*(math.pi/180))
        z_coord2  = z_coord1 - 158.81*math.sin((180 - (135 - spinBoxes[1].value()) - (spinBoxes[2].value()))*(math.pi/180))
        rect_item2 = RectItem(QtCore.QRectF(-53.05, -106.1, 106.1, 106.1))
        graphics[1].clear()
        graphics[1].addItem(rect_item2)
        graphics[1].plot((0, x_coord1),
                    (0, z_coord1),
                    pen=pen1,
                    symbol='o',
                    symbolSize=15,
                    symbolBrush='b')
        graphics[1].plot((x_coord1, x_coord2),
                    (z_coord1, z_coord2),
                    pen=pen2,
                    symbol='o',
                    symbolSize=15,
                    symbolBrush='b')
        
    def drawViewFromCartesian(self,graphics: QtWidgets.QGraphicsView, spinBoxes: QtWidgets.QDoubleSpinBox, id):
        x_coord = spinBoxes[0].value()
        y_coord = spinBoxes[1].value()
        z_coord = spinBoxes[2].value()    


        angles = inverse_kinematics(x_coord, y_coord, z_coord)

        if angles:
            theta_0, theta_1, theta_2 = angles
            print(f'(θ⁰: {theta_0}, θ¹: {theta_1}, θ²: {theta_2})')

            if not check_list(theta_0, theta_1, theta_2, x_coord, y_coord, z_coord):
                pen1 = pyqtgraph.mkPen(color=(255, 0, 0), width=8, style = QtCore.Qt.SolidLine)
                pen2 = pyqtgraph.mkPen(color=(255, 0, 0), width=8, style = QtCore.Qt.SolidLine)
                self.disable_execute_button(False)
            else:
                pen1 = pyqtgraph.mkPen(color=(0, 240, 0), width=8, style = QtCore.Qt.SolidLine)
                pen2 = pyqtgraph.mkPen(color=(0, 220,215), width=8, style = QtCore.Qt.SolidLine)
                self.disable_execute_button(True)

            x_coord1  = 142.07*math.cos((135 - theta_1)*(math.pi/180))
            x_coord2  = x_coord1 + 158.08*math.cos((180 - (135 - theta_1) - (theta_2))*(math.pi/180))
            z_coord1 = 142.07*math.sin((135 - theta_1)*(math.pi/180))
            z_coord2  = z_coord1 - 158.08*math.sin((180 - (135 - theta_1) - (theta_2))*(math.pi/180))

            mid_x = x_coord1*math.sin(theta_0*(math.pi/180))
            mid_y = x_coord1*(-1*math.cos(theta_0*(math.pi/180)))

            graphics[0].clear()
            rect_item = RectItem(QtCore.QRectF(-53.05, -53.05, 106.1, 106.1))
            graphics[0].addItem(rect_item)

            if(z_coord2 > z_coord1 and x_coord2 > x_coord1): # Upper arm above Lower arm
                graphics[0].plot((0,mid_y),(0,mid_x), pen=pen1, symbol='o',symbolSize=15, symbolBrush=('b'))
                graphics[0].plot((mid_y,y_coord),(mid_x,x_coord), pen=pen2, symbol='o',symbolSize=15, symbolBrush=('b'))     
            elif(z_coord2 < z_coord1 and x_coord2 < x_coord1): # Lowe arm above Upper arm
                graphics[0].plot((mid_y,y_coord),(mid_x,x_coord), pen=pen1, symbol='o',symbolSize=15, symbolBrush=('b'))
                graphics[0].plot((0,mid_y),(0,mid_x), pen=pen1, symbol='o',symbolSize=15, symbolBrush=('b'))
            else: # neutral position
                graphics[0].plot((0,mid_y),(0,mid_x), pen=pen1, symbol='o',symbolSize=15, symbolBrush=('b'))
                graphics[0].plot((mid_y,y_coord),(mid_x,x_coord), pen=pen2, symbol='o',symbolSize=15, symbolBrush=('b'))

            graphics[1].clear()
            rect_item2 = RectItem(QtCore.QRectF(-53.05, -106.1, 106.1, 106.1))
            graphics[1].addItem(rect_item2)
            graphics[1].plot((0, x_coord1),
                             (0, z_coord1),
                             pen=pen1,
                             symbol='o',
                             symbolSize=15,
                             symbolBrush='b')
            graphics[1].plot((x_coord1, x_coord2),
                             (z_coord1, z_coord2),
                             pen=pen2,
                             symbol='o',
                             symbolSize=15,
                             symbolBrush='b')                 
        else:
            self.logger_box.insertPlainText('Unreachable position. \n')

    def scanSerialPorts(self, menu: QMenu):
        port_list = serial.tools.list_ports.comports()
        if len(port_list) == 0:
            menu.addAction('No ports available')
            self.logger_box.insertPlainText('No ports detected yet, please checkout devices connections \n')

        for port in port_list:
            menu.addAction(port.device)
            self.logger_box.insertPlainText('Port ' + port.device + ' detected & ready. \n')


    def setSerialPort(self, portID:QAction):
        self.port = portID.iconText()
        self.handler.port = self.port
        if  not (self.port == 'No ports available'):
            self.logger_box.insertPlainText('Port ' + self.port + ' selected as serial output')
        else:
            self.logger_box.insertPlainText('No serial ports available, please checkout your usb cable')

    def future_callback(self, ft: Future):
        res = ft.result()
        self.progress_bar.hide()
        if isinstance(res, ErrorData):
            self.show_popup(res.err_msg)
            self.execute_button.State = 0
            self.execute_button.setText("Execute Movement")
            self.logger_box.insertPlainText(f"Error happened: {res.err_msg}\n")
        elif isinstance(res, ControlInterface):
            self.logger_box.insertPlainText("The movement has been completed succesfully. \n")
            if self.combo_box_coordinates.currentIndex() == 0:
                self.spin_box_1.setValue(res.theta1)
                self.spin_box_2.setValue(res.theta2)
                self.spin_box_3.setValue(res.theta3)
            elif self.combo_box_coordinates.currentIndex() == 1:
                self.spin_box_1.setValue(res.x)
                self.spin_box_2.setValue(res.y)
                self.spin_box_3.setValue(res.z)

    def move_to_origin(self, button: QtWidgets.QPushButton, sliders: QtWidgets.QSlider, spin_boxes: QtWidgets.QDoubleSpinBox, index):
        if index == 0:
            spin_boxes[0].setValue(90)
            spin_boxes[1].setValue(0)
            spin_boxes[2].setValue(0)
        elif index == 1:
            spin_boxes[0].setValue(0)
            spin_boxes[1].setValue(0)
            spin_boxes[2].setValue(0)
        self.logger_box.insertPlainText("Arm has been moved back to its origin position \n")

    def disable_execute_button(self, enabler):
        if not enabler:
            self.execute_button.setText("Unreachable position")
            self.execute_button.setEnabled(False)
        else:
            self.execute_button.setText("Execute Movement")
            self.execute_button.setEnabled(True)

    def open_browser_info(self, action:QAction):
        if action.iconText() ==  'GitHub project':
            webbrowser.open("https://github.com/pArm-TFG")
        elif action.iconText() == 'Documentation':
            webbrowser.open('https://github.com/pArm-TFG/Memoria')
        elif action.iconText() == 'About us':
            webbrowser.open('https://www.linkedin.com/in/jose-alejandro-moya-blanco-78952a126/')  
            webbrowser.open('https://www.linkedin.com/in/javinator9889/')
            webbrowser.open('https://www.linkedin.com/in/mihai-octavian-34865419b/')



















            
            