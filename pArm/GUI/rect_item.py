#                             pArm-S1
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
    """
    Custom graphics object for drawing a rectangle in Qt.
    Receives a QRectF containing the points in which the rectangle
    must start and must end.

    :param rect: the rectangle vertices.
    :param parent: optional parent at which is attached.
    """
    def __init__(self, rect: QtCore.QRectF, parent=None):
        super(RectItem, self).__init__(parent)
        self.__rect = rect
        self.picture = QtGui.QPicture()
        self._gen_picture()

    @property
    def rect(self):
        """
        Access the rectangular vertices item.
        :return: QtCore.QRectF object.
        """
        # Read-only property
        return self.__rect

    def _gen_picture(self):
        """
        Generates the rectangle and paints it in pyqtgraph.
        """
        painter = QtGui.QPainter(self.picture)
        painter.setPen(qtg.mkPen('w'))
        painter.setBrush(qtg.mkBrush((130,130,130)))
        painter.drawRect(self.rect)
        painter.end()

    def paint(self, painter: QtGui.QPainter, options, widget=None):
        """
        Starts painting the rectangle.
        :param painter: the QPainter object.
        :param options: options to pass to the painter (actually ignored).
        :param widget: widget to use with the painter (actually ignored)
        """
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        """
        Generates the bounding rectangle by using the generated picture.

        :return: QtCore.QRectF
        """
        return QtCore.QRectF(self.picture.boundingRect())
