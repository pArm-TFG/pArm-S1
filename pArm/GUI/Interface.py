
from PyQt5 import QtCore, QtGui, QtWidgets

def adjustWidgetValue(type, slider: QtWidgets.QSlider, spinBox: QtWidgets.QSpinBox):
    if (type == "slider"):
         spinBox.setValue(slider.value())
    elif (type == "spinBox"):
        slider.setSliderPosition(spinBox.value())
        
    