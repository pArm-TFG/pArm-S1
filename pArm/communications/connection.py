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
import serial


class Connection:
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 9600):
        self.ser = serial.Serial(port=port, baudrate=baudrate)

    def __enter__(self):
        if not self.ser.is_open:
            self.ser.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.close()

    def write(self, data: bytes):
        self.ser.write(data)

    def read(self, size: int = 1) -> bytes:
        return self.ser.read(size)

    def readline(self) -> bytes:
        return self.ser.readline()

    def readall(self) -> bytes:
        return self.ser.readall()

    @property
    def is_closed(self) -> bool:
        return not self.ser.is_open

    @property
    def is_open(self) -> bool:
        return self.ser.is_open
