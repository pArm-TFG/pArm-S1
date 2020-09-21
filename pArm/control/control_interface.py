from abc import ABC, abstractmethod

class ControlInterface(ABC):

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
