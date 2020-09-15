from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

def adjustWidgetValue(type, slider: QtWidgets.QSlider, spinBoxDouble: QtWidgets.QDoubleSpinBox):
    if type == "slider":
         spinBoxDouble.setValue(slider.value()/10)
    elif type == "spinBox":
        slider.setSliderPosition(spinBoxDouble.value()*10)

def labelColorChange(label: QtWidgets.QLabel,r, g, b):
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

def setAngularHighlight(slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):
    slidersLabels[0].setText("Base Servo Angle")
    slidersLabels[1].setText("Shoulder Servo Angle")
    slidersLabels[2].setText("Elbow Servo Angle")   
    labelColorChange(slidersLabels[0],245,110,110)
    labelColorChange(slidersLabels[1],245,110,110)
    labelColorChange(slidersLabels[2],245,110,110)

def setCartesianHighLight(slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):   
    slidersLabels[0].setText("X Coordinate")
    slidersLabels[1].setText("Y Coordinate")
    slidersLabels[2].setText("Z Coordinate")
    labelColorChange(slidersLabels[0],245,110,110)
    labelColorChange(slidersLabels[1],245,110,110)
    labelColorChange(slidersLabels[2],245,110,110)

def setAngularMenu(slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):
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

def setCartesianMenu(slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):   
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

    return "Cartesian"

def CoordinatesHighlight(comboBox: QtWidgets.QComboBox, slidersLabels: QtWidgets.QLabel,sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox, index):
    if index == 1 :
        setCartesianHighLight(slidersLabels,sliders,spinBoxes) 
    elif index == 0 :
        setAngularHighlight(slidersLabels,sliders,spinBoxes)
        
def changeCoordinateMenu(comboBox: QtWidgets.QComboBox, slidersLabels: QtWidgets.QLabel,sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox, index):
    if index == 1 : 
        setCartesianMenu(slidersLabels, sliders, spinBoxes)
    elif index == 0 : 
        setAngularMenu(slidersLabels, sliders, spinBoxes)
        
def show_popup(message: str):
    msg = QMessageBox()
    msg.setWindowTitle("Warning")
    msg.setText(message)
    msg.setIcon(2)
    x = msg.exec_()   
  
def executeMovement(button : QtWidgets.QPushButton, logger: QtWidgets.QPlainTextEdit):
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

   
   
      