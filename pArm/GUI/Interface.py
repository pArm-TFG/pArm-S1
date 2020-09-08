from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

def adjustWidgetValue(type, slider: QtWidgets.QSlider, spinBox: QtWidgets.QSpinBox):
    if type == "slider":
         spinBox.setValue(slider.value())
    elif type == "spinBox":
        slider.setSliderPosition(spinBox.value())

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

def setAngularLayout(slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QSpinBox):
    slidersLabels[0].setText("Base Servo Angle")
    slidersLabels[1].setText("Shoulder Servo Angle")
    slidersLabels[2].setText("Elbow Servo Angle")   
    labelColorChange(slidersLabels[0],0,180,0)
    labelColorChange(slidersLabels[1],0,180,0)
    labelColorChange(slidersLabels[2],0,180,0)

def setCartesianLayout(slidersLabels: QtWidgets.QLabel, sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QSpinBox):   
    slidersLabels[0].setText("X Coordinate")
    slidersLabels[1].setText("Y Coordinate")
    slidersLabels[2].setText("Z Coordinate")
    labelColorChange(slidersLabels[0],230,50,255)
    labelColorChange(slidersLabels[1],230,50,255)
    labelColorChange(slidersLabels[2],230,50,255)

def swapCoordinatesHighlight(comboBox: QtWidgets.QComboBox, slidersLabels: QtWidgets.QLabel,sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QSpinBox, index):
    if index == 1 :
        setCartesianLayout(slidersLabels,sliders,spinBoxes) 
    elif index == 0 :
        setAngularLayout(slidersLabels,sliders,spinBoxes)
        
def swapCoordinatesConfirm(comboBox: QtWidgets.QComboBox, slidersLabels: QtWidgets.QLabel,sliders: QtWidgets.QSlider, spinBoxes: QtWidgets.QSpinBox, index):
    if index == 1 :
        setCartesianLayout(slidersLabels,sliders,spinBoxes) 
        labelColorChange(slidersLabels[0],255,0,0)
        labelColorChange(slidersLabels[1],255,0,0)
        labelColorChange(slidersLabels[2],255,0,0)
    elif index == 0 :
        setAngularLayout(slidersLabels,sliders,spinBoxes)    
        labelColorChange(slidersLabels[0],255,0,0)
        labelColorChange(slidersLabels[1],255,0,0)
        labelColorChange(slidersLabels[2],255,0,0)   
        
    