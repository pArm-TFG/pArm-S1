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
    labelColorChange(slidersLabels[0],0,180,0)
    labelColorChange(slidersLabels[1],0,180,0)
    labelColorChange(slidersLabels[2],0,180,0)

def setCartesianHighLight(slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):   
    slidersLabels[0].setText("X Coordinate")
    slidersLabels[1].setText("Y Coordinate")
    slidersLabels[2].setText("Z Coordinate")
    labelColorChange(slidersLabels[0],230,50,255)
    labelColorChange(slidersLabels[1],230,50,255)
    labelColorChange(slidersLabels[2],230,50,255)

def setAngularMenu(slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):
    labelColorChange(slidersLabels[0],255,0,0)
    labelColorChange(slidersLabels[1],255,0,0)
    labelColorChange(slidersLabels[2],255,0,0)

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
    spinBoxes[0].setRange(0,120.0)
    spinBoxes[2].setValue(0.0)

    slidersLabels[3].setText("0º")
    slidersLabels[4].setText("151º")
    slidersLabels[5].setText("0º")
    slidersLabels[6].setText("135º")
    slidersLabels[7].setText("0º")
    slidersLabels[8].setText("120º")
    slidersLabels[9].hide()

def setCartesianMenu(slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QDoubleSpinBox):   
    labelColorChange(slidersLabels[0],255,0,0)
    labelColorChange(slidersLabels[1],255,0,0)
    labelColorChange(slidersLabels[2],255,0,0)

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

    slidersLabels[3].setText("0.0mm")
    slidersLabels[4].setText("346.0mm")
    slidersLabels[5].setText("-346.0mm")
    slidersLabels[6].setText("346.0mm")
    slidersLabels[7].setText("0.0mm")
    slidersLabels[8].setText("306.6mm")
    slidersLabels[9].show()

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
        
        
    