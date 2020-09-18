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
from . import init_logging
from PyQt5 import QtWidgets
from .GUI import GUI
from .control import control
import sys

if __name__ == '__main__':
    init_logging("Roger", log_file="p-Arm.log")
    app = QtWidgets.QApplication(sys.argv)

    ui = GUI.Ui()
    ui.setupGUI()
    ui.show()
    sys_control = control.Control()

    sys.exit(app.exec_())
    pass  # TODO
