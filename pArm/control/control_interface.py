from abc import ABC, abstractmethod
from typing import Callable, Optional
from concurrent.futures import ThreadPoolExecutor
from ..utils import AtomicFloat


class ControlInterface(ABC):

    @abstractmethod
    def __init__(self, executor: ThreadPoolExecutor, x=0, y=0, z=0, theta1=0, theta2=0, theta3=0, port=''):
        self.executor = executor
        self.x = x
        self.y = y
        self.z = z

        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3

    @abstractmethod
    def move_to_xyz(self, x, y, z, time_object: Optional[AtomicFloat] = None):
        """
        Triggers the needed procedures to move the arm to the cartesian position
        that is indicated in its parameters.
        :param x: x position to which the end effector shall move
        :param y: y position to which the end effector shall move
        :param z: z position to which the end effector shall move
        :param time_object: the atomic float holder value.
        :return: the future object.
        """
        pass

    @abstractmethod
    def move_to_thetas(self, theta1, theta2, theta3, time_object: Optional[AtomicFloat] = None):
        """
        Triggers the needed procedures to move the arm to the angular position
        that is indicated in its parameters.
        :param theta1: theta1 angle to which the base motor shall move
        :param theta2: theta2 angle to witch the shoulder motor shall move
        :param theta3: theta3 angle to which the elbow motor shall move
        :param time_object: the atomic float holder value.
        :return: the future object.
        """
        pass

    @abstractmethod
    def cancel_movement(self):
        """
        This function sends a request to the arm controller telling it to stop
        the movement that is currently being made. If the controller confirms
        that the movement has been canceled, this function also updates the
        class position variables with the real physical ones.
        :return: no return.
        """
        pass

    @abstractmethod
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
        pass

    @property
    @abstractmethod
    def err_fn(self) -> Callable[[int, str], None]:
        pass

    @property
    @abstractmethod
    def x(self):
        pass

    @property
    @abstractmethod
    def y(self):
        pass

    @property
    @abstractmethod
    def z(self):
        pass

    @property
    @abstractmethod
    def port(self):
        pass

    @x.setter
    @abstractmethod
    def x(self, value):
        pass

    @y.setter
    @abstractmethod
    def y(self, value):
        pass

    @z.setter
    @abstractmethod
    def z(self, value):
        pass

    @port.setter
    @abstractmethod
    def port(self, value):
        pass

    @err_fn.setter
    @abstractmethod
    def err_fn(self, fn: Callable[[int, str], None]):
        pass
