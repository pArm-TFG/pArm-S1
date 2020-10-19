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
import logging
from . import init_logging
from PyQt5 import QtWidgets, QtGui
from .GUI import GUI
from .control.control import Control
import sys
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.NOTSET)


def main():
    try:
        init_logging("Roger", log_file="p-Arm.log")
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon("yo.jpg"))

        executor = ThreadPoolExecutor()

        sys_control = Control(executor)

        ui = GUI.Ui(sys_control)
        ui.setupGUI()
        ui.show()

        sys.exit(app.exec_())
    except Exception as e:
        log = logging.getLogger("Roger")
        log.critical(f"Unexpected error '{e}' while executing application!",
                     exc_info=True)


if __name__ == '__main__':
    main()
