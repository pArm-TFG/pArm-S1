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
from logging import Handler, LogRecord
from PyQt5 import QtWidgets
from typing import Optional


class QTextEditLogger(Handler):
    """
    Custom ``logging.Handler`` class which outputs the log
    to the in UI console. Receives the parent to which it is attached
    and defaults to read-only (can be changed accessing ``widget`` attr).

    :param edit_text: the source edit text to use if no parent specified.
    :param parent: the parent in which the new widget will be hosted.
    :raises AttributeError if both ``edit_text`` and ``parent`` are None.
    """
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

    def emit(self, record: LogRecord):
        """
        Formats the record and outputs it to the plain text edit widget.
        :param record: the record to be formatted.
        """
        msg = self.format(record)
        self.widget.appendPlainText(msg)
        self.widget.ensureCursorVisible()
