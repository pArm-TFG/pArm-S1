from ..gcode import generator
from ..gcode import interpreter
from ..security import RSA
from .. import Connection
from serial import SerialException
from logging import getLogger
from .control_interface import ControlInterface
import time

LOWEST_X_VALUE = 0
HIGHEST_X_VALUE = 300
LOWEST_Y_VALUE = 0
HIGHEST_Y_VALUE = 300
LOWEST_Z_VALUE = 0
HIGHEST_Z_VALUE = 300

log = getLogger("Roger")


class Control(ControlInterface):

    def __init__(self, x=0, y=0, z=0, theta1=0, theta2=0, theta3=0, port=''):
        super(Control, self).__init__()
        self.x = x
        self.y = y
        self.z = z

        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3

        self.port = port

        self.connection = Connection()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def port(self):
        return self._port

    @x.setter
    def x(self, x):
        if LOWEST_X_VALUE <= x <= HIGHEST_X_VALUE:
            self._x = x
        else:
            print("X value out of bounds")

    @y.setter
    def y(self, y):
        if LOWEST_Y_VALUE <= y <= HIGHEST_Y_VALUE:
            self._y = y
        else:
            print("Y value out of bounds")

    @z.setter
    def z(self, z):
        if LOWEST_Z_VALUE <= z <= HIGHEST_Z_VALUE:
            self._z = z
        else:
            print("Z value out of bounds")

    @port.setter
    def port(self, port):
        self._port = port
        #self.connection.port = self._port

    def move_to_xyz(self, x, y, z):

        byte_stream = generator.generate_xyz_movement(x, y, z)
        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug("X, Y, Z values successfully sent to device")

    def move_to_thetas(self, theta1, theta2, theta3):

        byte_stream = generator.generate_theta_movement(theta1, theta2, theta3)

        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug("theta1, theta2, theta3 values successfully sent to device")

    def send_to_origin(self):

        byte_stream = generator.generate_send_to_origin()

        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug(f"Device sent to origin")

    def request_cartesian_position(self):

        byte_stream = generator.generate_request_cartesian_position()

        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug(f"Cartesian position requested")

    def request_angular_position(self):

        byte_stream = generator.generate_request_angular_position()

        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug(f"Angular position requested")

    def request_recalculate_keys(self):

        byte_stream = generator.generate_recaculate_keys()

        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug(f"Key recalculation requested")


    def read_cartesian_positions(self):
        self.request_cartesian_position()
        cartesian_positions = interpreter.parse_line()
        self.x = cartesian_positions.x
        self.y = cartesian_positions.y
        self.z = cartesian_positions.z

    def read_angular_positions(self):
        self.request_angular_position()
        angular_positions = interpreter.parse_line()
        self.theta1 = angular_positions.t1
        self.theta2 = angular_positions.t2
        self.theta3 = angular_positions.t3

    def cancel_movement(self):
        byte_stream = generator.generate_cancel_movement()

        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug(f"Device sent to origin")

        cancel_confirm = interpreter.parse_line()
        timeout = time.time() + 5

        while not cancel_confirm and time.time() > timeout:
            cancel_confirm = interpreter.parse_line()

        if cancel_confirm is True:
            self.read_cartesian_positions()
            self.read_angular_positions()

    #def read_n(self):

    #def read_e(self):

    #def read_signed_value(self):

    #def


    def do_handshake(self):

        byte_stream = generator.generate_request_n_e()

        try:
            with self.connection as conn:
                conn.write(byte_stream)

            found, missed_instructions, line = interpreter.wait_for(self, 'I2')
            if found:
                n = interpreter.parse_line(line)

            found, missed_instructions, line = interpreter.wait_for(self, 'I3')
            if found:
                e = interpreter.parse_line(line)

            rsa = RSA(n,e)

            found, missed_instructions, line = interpreter.wait_for(self, 'I4')
            if found:
                signed_value = interpreter.parse_line(line)

            unsigned_value = rsa.verify(signed_value)

            bunsigned_value = generator.generate_unsigned_string(unsigned_value)

            conn.write(bunsigned_value)

            found, missed_instructions, line = interpreter.wait_for(self, 'I5')



        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug("Handshake started. Request sent")


