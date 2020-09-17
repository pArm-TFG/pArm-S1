from .. import generate_xyz_movement, generate_theta_movement, generate_send_to_origin
from .. import Connection
from serial import SerialException
from logging import getLogger


LOWEST_X_VALUE = 0
HIGHEST_X_VALUE = 300
LOWEST_Y_VALUE = 0
HIGHEST_Y_VALUE = 300
LOWEST_Z_VALUE = 0
HIGHEST_Z_VALUE = 300

log = getLogger("Roger")


class Control:

    def __init__(self, x=0, y=0, z=0, theta1=0, theta2=0, theta3=0):
        self.x = x
        self.y = y
        self.z = z

        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3

        self.current_index = 0

        self.connection = Connection()

    @property
    def current_index(self):
        return self.current_index

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

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

    @current_index.setter
    def current_index(self, current_index):
        self._current_index = current_index

    def move_to_xyz(self, x, y, z):

        byte_stream = generate_xyz_movement(x, y, z)

        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug("X, Y, Z values successfully sent to device")

    def move_to_thetas(self, theta1, theta2, theta3):

        byte_stream = generate_theta_movement(theta1, theta2, theta3)

        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug("theta1, theta2, theta3 values successfully sent to device")

    def send_to_origin(self):

        byte_stream = generate_send_to_origin()

        try:
            with self.connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")
        else:
            log.debug(f"Device sent to origin")

    def execute_movement(self, x_theta1, y_theta2, z_theta3, xyz_theta, is_execute):
        if not is_execute:
            if xyz_theta == 0:
                self.x = x_theta1
                self.y = y_theta2
                self.z = z_theta3
                self.move_to_xyz(x_theta1, y_theta2, z_theta3)
            elif xyz_theta == 1:
                self.theta1 = x_theta1
                self.theta1 = y_theta2
                self.theta3 = z_theta3
                self.move_to_thetas(x_theta1, y_theta2, z_theta3)
