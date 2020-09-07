from PyQt5 import QtCore, QtGui, QtWidgets
from GUI import *

def adjustWidgetValue(type, slider: QtWidgets.QSlider, spinBox: QtWidgets.QSpinBox):
    if type == "slider":
         spinBox.setValue(slider.value())
    elif type == "spinBox":
        slider.setSliderPosition(spinBox.value())
        
def swapCoordinates(comboBox: QtWidgets.QComboBox):
    return
    