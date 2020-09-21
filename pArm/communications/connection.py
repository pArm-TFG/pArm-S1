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
from typing import Optional


class Connection:
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a singleton instance that handles all the connections
        with the UART device.
        :param args: arbitrary arguments used while creating the class.
        :param kwargs: arbitrary keyword arguments used while creating the
        class.
        """
        if not Connection.__instance:
            Connection.__instance = object.__new__(cls)
            Connection.__instance.__must_init = True
        else:
            Connection.__instance.__must_init = False

        return Connection.__instance

    def __init__(self,
                 port: str = "/dev/ttyUSB0",
                 baudrate: int = 9600,
                 should_open: bool = False):
        """
        Sets port and a baudrate for a serial connection. Also opens the port
        with the current configuration.

        :param port: the port used for serial comunication
        :param baudrate: the baudrate of the serial connection
        :param should_open: if true, the port is opened
        """
        if self.__must_init:
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

    def write(self, data: bytes) -> Optional[int]:
        """
        Writes data of a specified size to serial port.

        :param data: data to be writen to the port.
        :return: the length of the written data.
        """
        return self.ser.write(data)

    def swrite(self, data: str, encoding: str = 'utf-8') -> Optional[int]:
        """
        Writes specified data string to serial port.
        :param data: the data to write to serial port, as string.
        :param encoding: in which encoding the string is written.
        :return: the length of the written data.
        """
        return self.write(data.encode(encoding))

    def read(self, size: int = 1) -> bytes:
        """
        Reads data from of a specified size to serial port.

        :param size: the size to be read.
        :return: the read value in bytes.
        """
        return self.ser.read(size)

    def sread(self, size: int = 1, encoding: str = 'utf-8') -> str:
        """
        Reads from serial port the specified size.
        :param size: the size to be read.
        :param encoding: the encoding in which the bytes is expected to be.
        :return: the read value as string.
        """
        return self.read(size).decode(encoding)

    def readline(self) -> bytes:
        """
        Reads a line from the serial buffer
        :return: the read line in bytes.
        """
        return self.ser.readline()

    def sreadline(self, encoding: str = 'utf-8') -> str:
        """
        Reads a line from the serial buffer.
        :param encoding: the encoding in which the bytes is expected to be.
        :return: the read line as string.
        """
        return self.readline().decode(encoding)

    def readall(self) -> bytes:
        """
        Reads all the serial buffer.

        :return: the entire buffer in bytes.
        """
        return self.ser.readall()

    def sreadall(self, encoding: str = 'utf-8') -> str:
        """
        Reads all the serial buffer.

        :param encoding: the encoding in which the bytes is expected to be.
        :return: the entire buffer as string.
        """
        return self.readall().decode(encoding)

    @property
    def is_closed(self) -> bool:
        return not self.ser.is_open

    @property
    def is_open(self) -> bool:
        return self.ser.is_open

    @property
    def port(self):
        ser_port = self.ser.port
        if ser_port != self._port:
            self._port = ser_port
        return ser_port

    @port.setter
    def port(self, port: str):
        self._port = port
        self.ser.port = self._port
