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
from typing import Optional
from PyQt5 import QtCore, QtWidgets
from logging import Handler, LogRecord


class QTextEditLogger(QtCore.QObject, Handler):
    """
    Custom ``logging.Handler`` class which outputs the log
    to the in UI console. Receives the parent to which it is attached
    and defaults to read-only (can be changed accessing ``widget`` attr).

    :param edit_text: the source edit text to use if no parent specified.
    :param parent: the parent in which the new widget will be hosted.
    :raises AttributeError if both ``edit_text`` and ``parent`` are None.
    """
    _log_signal = QtCore.pyqtSignal(str)

    def __init__(self,
                 edit_text: Optional[QtWidgets.QPlainTextEdit] = None,
                 parent: Optional[QtWidgets.QWidget] = None):
        super(QTextEditLogger, self).__init__()
        if edit_text:
            self.widget = edit_text
        elif parent:
            self.widget = QtWidgets.QPlainTextEdit(parent)
        else:
            raise AttributeError("Either edit_text or parent must not be None")
        self.widget.setReadOnly(True)

        def msg_handler(msg):
            """
            Simple message handler that must be connected to the signal so
            the edit text can be updated.

            :param msg: the message to display
            """
            self.widget.appendPlainText(msg)
            self.widget.ensureCursorVisible()

        self._log_signal.connect(msg_handler)

    def emit(self, record: LogRecord):
        """
        Formats the record and outputs it to the plain text edit widget.
        :param record: the record to be formatted.
        """
        msg = self.format(record)
        self._log_signal.emit(msg)
