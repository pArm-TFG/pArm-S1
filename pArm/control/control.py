from .. import generate_xyz_movement, generate_theta_movement


class Control:

    def __init__(self,x = 0,y = 0,z = 0,theta1 = 0,theta2 = 0,theta3 = 0):
        self.x = x
        self.y = y
        self.z = z

        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3

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
        # TODO - check constraints
        self._x = x

    @y.setter
    def y(self, y):
        # TODO - check constraints
        self._y = y

    @z.setter
    def z(self, z):
        self._z = z



    def move_to_xyz(self, x, y, z):





