from ..gcode import generator
from ..gcode import interpreter
from ..security import RSA
from .. import Connection
from serial import SerialException
from logging import getLogger
from .control_interface import ControlInterface
from typing import Callable, Optional, Union
from pArm.control import control_management
from concurrent.futures import ThreadPoolExecutor, Future
from ..utils import AtomicFloat, ErrorData
from .heart_beat import Heart

LOWEST_X_VALUE = 0
HIGHEST_X_VALUE = 300
LOWEST_Y_VALUE = 0
HIGHEST_Y_VALUE = 300
LOWEST_Z_VALUE = 0
HIGHEST_Z_VALUE = 300

log = getLogger("Roger")


class Control(ControlInterface):

    def __init__(self, executor: ThreadPoolExecutor, x=0, y=0, z=0, theta1=0,
                 theta2=0, theta3=0, port=''):
        super(Control, self).__init__(executor, x, y, z, theta1, theta2, theta3,
                                      port)

        self._err_fn = None

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

    @property
    def err_fn(self) -> Callable[[int, str], None]:
        return self._err_fn

    @err_fn.setter
    def err_fn(self, fn: Callable[[int, str], None]):
        self._err_fn = fn

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

    def move_to_xyz(self, x, y, z,
                    time_object: Optional[AtomicFloat] = None) -> \
            Future:
        """
        Triggers the needed procedures to move the arm to the cartesian position
        that is indicated in its parameters.
        :param x: x position to which the end effector shall move
        :param y: y position to which the end effector shall move
        :param z: z position to which the end effector shall move
        :param time_object: the atomic float holder value.
        :return: the future object.
        """

        def fn():
            byte_stream = generator.generate_xyz_movement(x, y, z)
            try:
                with self.connection as conn:
                    conn.write(byte_stream)
            except SerialException:
                log.warning("There is no suitable connection with the device")
            err = control_management.verify_movement_completed(time_object)
            if err:
                return err
            self.read_cartesian_positions()
            self.read_angular_positions()

            return self

        return self.executor.submit(fn)

    def move_to_thetas(self,
                       theta1,
                       theta2,
                       theta3,
                       time_object: Optional[AtomicFloat] = None) -> \
            Future:
        """
        Triggers the needed procedures to move the arm to the angular position
        that is indicated in its parameters.
        :param theta1: theta1 angle to which the base motor shall move
        :param theta2: theta2 angle to witch the shoulder motor shall move
        :param theta3: theta3 angle to which the elbow motor shall move
        :param time_object: the atomic float holder value.
        :return: the future object.
        """

        byte_stream = generator.generate_theta_movement(theta1, theta2, theta3)

        def fn():
            try:
                with self.connection as conn:
                    conn.write(byte_stream)
            except SerialException:
                log.warning("There is no suitable connection with the device")
            else:
                log.debug(
                    "theta1, theta2, theta3 values successfully sent to device")
            err = control_management.verify_movement_completed(time_object)
            if err:
                return err
            self.read_cartesian_positions()
            self.read_angular_positions()
            return self

        return self.executor.submit(fn)

    def send_to_origin(self, time_object: Optional[AtomicFloat] = None) -> \
            Future:
        """
        This function send the arm to its initial position.
        :param time_object: the atomic float holder value.
        :return: the future object.
        """

        byte_stream = generator.generate_send_to_origin()

        def fn():
            try:
                with self.connection as conn:
                    conn.write(byte_stream)
            except SerialException:
                log.warning("There is no suitable connection with the device")
            else:
                log.debug(f"Device sent to origin")
            err = control_management.verify_movement_completed(time_object)
            if err:
                return err
            self.read_cartesian_positions()
            self.read_angular_positions()

            return self

        return self.executor.submit(fn)

    def read_cartesian_positions(self):
        """
        This function request the real physical cartesian position from the arm
        controller and then save them in the class variables
        :return: no return.
        """
        control_management.request_cartesian_position()

        try:
            found, missed_instructions, line = interpreter.wait_for('G0')
            if found:
                cartesian_positions = interpreter.parse_line(line)
                self.x = cartesian_positions.x
                self.y = cartesian_positions.y
                self.z = cartesian_positions.z
        except SerialException:
            log.warning("There is no suitable connection with the device")

    def read_angular_positions(self):
        """
        This function request the real physical angular values from the arm
        controller and then save them in the class variables
        :return: no return.
        """
        control_management.request_angular_position()

        try:
            found, missed_instructions, line = interpreter.wait_for('G1')
            if found:
                angular_positions = interpreter.parse_line(line)
                self.theta1 = angular_positions.t1
                self.theta2 = angular_positions.t2
                self.theta3 = angular_positions.t3
        except SerialException:
            log.warning("There is no suitable connection with the device")

    def cancel_movement(self) -> Future:
        """
        This function cancels the current movement. If the controller confirms
        that the movement has been canceled, this function also updates the
        class position variables with the real physical ones.
        :return: ErrorData if the cancellation could not complete successfully.
        """
        control_management.request_cancel_movement()

        def fn():
            gcode = ["J{}".format(x) for x in range(2, 21)]
            gcode.append('M1')

            try:
                found, missed_instructions, line = interpreter.wait_for(gcode)
                if found and line is True:
                    self.read_angular_positions()
                    self.read_cartesian_positions()
                    return self
                else:
                    err_code = int(line[1:])
                    return interpreter.errors[err_code]
            except SerialException:
                log.warning("There is no suitable connection with the device")

        return self.executor.submit(fn)

    def read_handshake_values(self, order: str):
        """
        This function reads through the buffer searching for a line that contains
        the order specified in it parameter. If found it return the whole line.
        :param order: the order that tha function shall look for
        :return: the complete line where that instruction has been found.
        """
        try:
            found, missed_instructions, line = interpreter.wait_for(order)
            if found:
                return interpreter.parse_line(line)
        except SerialException as e:
            log.warning(str(e), exc_info=True)

    def do_handshake(self):
        """
        Starts the handshake procedure.
        The procedure is as follows:
        1. The control application (this software) requests the procedure to start

        2. The arm controller sends I2 {n} where n is the module needed to "un-sign"
        a string that will follow.

        3. The arm controller sends I3 {e} where e is the exponent needed to "un-sign"
        a string that will follow.

        4. The control application (this software) will proceed to create an instance
        of the RSA class with n and e.

        5. The arm controller sends I4 {signed integer} where the signed integer
        its a random integer that the arm controller has signed.

        6. Using the RSA object the control application (this software) first
        "un-sign" the integer. Then, using the same n and e we encrypt it.

        7. Then we use this new encrypted integer to generate the heartbeat
        and  send it back to the arm controller.

        8. The arm controller verifies the integer, and if it succeeds,
        it send an I5 to confirm the handshake has been done correctly.

        The control application (this software) can also receive an error code
        with the format Jx, where x its an integer between 2 and 21. This can happen
        if at any step, the arm controller receives an unexpected value. This event
        would finish the handshaking procedure and the pairing would fail.
        :return: The returns from the else statements are possible error codes
        that the arm controller could return.
        """
        gcode = {"J{}".format(x) for x in range(2, 21)}
        control_management.request_handshake()
        try:
            gcode.add('I2')
            found, missed_instructions, n = interpreter.wait_for(gcode)
            if found and isinstance(n, str):
                gcode.add('I3')
                found, missed_instructions, e = interpreter.wait_for(gcode)
                if found and isinstance(e, str):
                    rsa = RSA(int(n), int(e))
                    gcode.add('I4')
                    found, missed_instructions, signed_value = \
                        interpreter.wait_for(gcode)
                    if found and isinstance(signed_value, str):
                        verified_value = rsa.verify(int(signed_value))
                        encrypted_value = rsa.encrypt(verified_value)
                        heart = Heart(int(encrypted_value))
                        with self.connection as conn:
                            conn.write(generator
                                       .generate_unsigned_string(encrypted_value))
                            found, missed_instructions, line = \
                                interpreter.wait_for('I5')
                            if found:
                                log.info("Handshake done.")
                                heart.start_beating = True
                    else:
                        return signed_value
                else:
                    return e
            else:
                return n

        except SerialException:
            log.warning("There is no suitable connection with the device")
