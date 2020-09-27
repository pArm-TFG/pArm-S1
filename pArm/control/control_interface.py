from abc import ABC, abstractmethod
from typing import Callable
from concurrent.futures import ThreadPoolExecutor


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
    def move_to_xyz(self, x, y, z):
        pass

    @abstractmethod
    def move_to_thetas(self, theta1, theta2, theta3):
        pass

    @abstractmethod
    def cancel_movement(self):
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
