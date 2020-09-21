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
    def __init__(self,
                 port: str = "/dev/ttyUSB0",
                 baudrate: int = 9600,
                 should_open: bool = False):
        """
        Sets port and a baudrate for a serial connection. Also opens the port
        with the current configuration.

        :param port: the port used for serial communication
        :param baudrate: the baudrate of the serial connection
        :param should_open: if true, the port is opened
        """
        self.ser = serial.Serial(baudrate=baudrate)
        self.ser.port = port
        self._port = port
        if should_open:
            self.ser.open()

    def __enter__(self):
        """
        If not open, it opens the serial port.
        """
        if not self.ser.is_open:
            self.ser.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes current port
        """
        self.ser.close()

    def write(self, data: bytes):
        """
        Writes data of a specified size to serial port

        :param data: data to be writen to the port
        """
        self.ser.write(data)

    def read(self, size: int = 1) -> bytes:
        """
        Reads data from of a specified size to serial port

        :param size: the size to be read
        """
        return self.ser.read(size)

    def readline(self) -> bytes:
        """
        Reads a line from the serial buffer
        """
        return self.ser.readline()

    def readall(self) -> bytes:
        """
        Read all the serial buffer
        """
        return self.ser.readall()

    @property
    def is_closed(self) -> bool:
        return not self.ser.is_open

    @property
    def is_open(self) -> bool:
        return self.ser.is_open

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = f"/dev/{port}"
