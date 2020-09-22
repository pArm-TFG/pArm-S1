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
        return self.connection.port

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
        self.connection.port = port
        
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

    def read_handshake_values(self, order: str):
        try:
            found, missed_instructions, line = interpreter.wait_for(self, order)
            if found:
                return interpreter.parse_line(line)
        except SerialException as e:
            log.warning(str(e), exc_info=True)

    def do_handshake(self):

        byte_stream = generator.generate_request_n_e()

        try:
            with self.connection as conn:
                conn.write(byte_stream)

            n = self.read_handshake_values('I2')
            e = self.read_handshake_values('I3')

            rsa = RSA(n, e)

            signed_value = self.read_handshake_values('I4')
            verified_value = rsa.verify(signed_value)

            verified_value_bytes = generator.generate_unsigned_string(verified_value)
            conn.write(verified_value_bytes)
            found, missed_instructions, line = interpreter.wait_for(self, 'I5')
            if found:
                log.info("Handshake done.")

        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug("Handshake started. Request sent")


