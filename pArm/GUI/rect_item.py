#                             pArm-S1
#                  Copyright (C) 2020 - Javinator9889
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#                   (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#               GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
import pyqtgraph as qtg
from PyQt5 import QtCore, QtGui


class RectItem(qtg.GraphicsObject):
    def __init__(self, rect: QtCore.QRectF, parent=None):
        super(RectItem, self).__init__(parent)
        self.__rect = rect
        self.picture = QtGui.QPicture()
        self._gen_picture()

    @property
    def rect(self):
        # Read-only property
        return self.__rect

    def _gen_picture(self):
        painter = QtGui.QPainter(self.picture)
        painter.setPen(qtg.mkPen('w'))
        painter.setBrush(qtg.mkBrush((130,130,130)))
        painter.drawRect(self.rect)
        painter.end()

    def paint(self, painter: QtGui.QPainter, options, widget=None):
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())
