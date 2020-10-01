import math
import os

import pyqtgraph
import serial.tools.list_ports
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QMessageBox, QMenu, QAction
from pyqtgraph import PlotWidget
from concurrent.futures import Future
from ..utils import AtomicFloat
from ..utils.error_data import ErrorData
from ..control.control_interface import ControlInterface
from .progress_widget import ProgressWidget


class Ui(QtWidgets.QMainWindow):

    def __init__(self, control: ControlInterface):
        super(Ui, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'InProgressGUI.ui'), self)

        #Logic interface
        self.handler = control

        #Serial Port used to send data to PCB
        self.port = 'null'

        #Left Window Section
        self.menu_port = self.findChild(QtWidgets.QMenu, 'menuPort_Selection')

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

        self.progress_bar = ProgressWidget.from_bar(
            self.findChild(QtWidgets.QProgressBar, 'ProgressBar')
        )
        # self.progress_bar = self.findChild(QtWidgets.QProgressBar, 'ProgressBar')
        # self.progress_bar.__class__ = ProgressWidget

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
        self.top_view.setYRange(400,0, padding = 0)
        pen = pyqtgraph.mkPen(color=(0, 255, 0), width=8, style = QtCore.Qt.SolidLine)
        #self.top_view.plot((0,0),(0,346), pen=pen)
        self.drawViewFromAngle(graphics, spin_boxes,1)
        self.side_view.setXRange(-300, 300, padding = 0)
        self.side_view.setYRange(300, 0, padding = 0)
        self.drawViewFromAngle(graphics, spin_boxes,3)
        #self.side_view.plotplot((0,x_coord1,x_coord2),(0,z_coord1,z_coord2), pen=pen, symbol='o', symbolSize=20, symbolBrush=('b'))

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

        sliders_labels[0].setText("X Coordinate")
        sliders_labels[1].setText("Y Coordinate")
        sliders_labels[2].setText("Z Coordinate")
        sliders_labels[3].setText("0.0mm")
        sliders_labels[4].setText("346.0mm")
        sliders_labels[5].setText("-346.0mm")
        sliders_labels[6].setText("346.0mm")
        sliders_labels[7].setText("0.0mm")
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
        sliders[2].setMinimum(0)
        sliders[2].setTickInterval(901)
        sliders[2].setSliderPosition(0)
        spin_boxes[2].setRange(0,360.6)
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
                ft.add_done_callback(lambda future: self.future.callback(future))     
        else:
            #self.handler.cancel_movement()
            self.show_popup("Movement Cancelled")
            self.logger_box.insertPlainText("Movement Cancelled\n")
            self.logger_box.ensureCursorVisible()
            button.setText("Execute Movement")
            button.State = True

    def drawViewFromAngle(self,graphics: QtWidgets.QGraphicsView, spinBoxes: QtWidgets.QDoubleSpinBox, id):
        if id == 1:
            pen = pyqtgraph.mkPen(color=(0, 255, 0), width=8, style = QtCore.Qt.SolidLine)
            x_coord = 346*math.cos((spinBoxes[0].value())*(math.pi/180))
            y_coord = 346*math.sin((spinBoxes[0].value())*(math.pi/180))
            graphics[0].clear()
            graphics[0].plot((0,x_coord),(0,y_coord), pen=pen, symbol='o', symbolSize=20, symbolBrush=('b'))
        elif id == 2 or  id == 3 :
            pen = pyqtgraph.mkPen(color=(0, 255, 0), width=8, style = QtCore.Qt.SolidLine)
            x_coord1  = 142*math.cos((135 - spinBoxes[1].value())*(math.pi/180))
            x_coord2  = x_coord1 + 158.8*math.cos((180 - (135 - spinBoxes[1].value()) - (spinBoxes[2].value()))*(math.pi/180))
            z_coord1 = 142*math.sin((135 - spinBoxes[1].value())*(math.pi/180))
            z_coord2  = z_coord1 - 158.8*math.sin((180 - (135 - spinBoxes[1].value()) - (spinBoxes[2].value()))*(math.pi/180))
            graphics[1].clear()
            graphics[1].plot((0,x_coord1,x_coord2),(0,z_coord1,z_coord2), pen=pen, symbol='o', symbolSize=20, symbolBrush=('b'))
            pass

    def drawViewFromCartesian(self,graphics: QtWidgets.QGraphicsView, spinBoxes: QtWidgets.QDoubleSpinBox, id):
        if id == 1 or id == 2:
            x_coord = spinBoxes[0].value()
            y_coord = spinBoxes[1].value()
            if not ((math.sqrt(x_coord**2 + y_coord**2)) > 346):
                pen = pyqtgraph.mkPen(color=(0, 255, 0), width=8, style = QtCore.Qt.SolidLine)
                graphics[0].clear()
                graphics[0].plot((0,y_coord),(0,x_coord), pen=pen, symbol='o', symbolSize=20, symbolBrush=('b'))
            else:
                pen = pyqtgraph.mkPen(color=(255, 0, 0), width=8, style = QtCore.Qt.SolidLine)
                graphics[0].clear()
                graphics[0].plot((0, y_coord),(0,x_coord), pen=pen, symbol='o', symbolSize=20, symbolBrush=('b'))
                self.logger_box.insertPlainText("Unreachable position, please move the arm back to its range\n")
        if id == 2 or id == 3 :
            pass

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
        if isinstance(res, ErrorData):
            pass
            #error logic
        elif isinstance(res, ControlInterface):
            pass
            #recieve data from pcb

    def move_to_origin(self, button: QtWidgets.QPushButton, sliders: QtWidgets.QSlider, spin_boxes: QtWidgets.QDoubleSpinBox, index):
        #this way it is ez to stablish an origin position
        if index == 0:
            spin_boxes[0].setValue(90)
            spin_boxes[1].setValue(0)
            spin_boxes[2].setValue(0)
        elif index == 1:
            spin_boxes[0].setValue(0)
            spin_boxes[1].setValue(0)
            spin_boxes[2].setValue(0)

        self.logger_box.insertPlainText("Arm has been moved back to its origin position \n")

