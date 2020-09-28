
def generate_xyz_movement(x, y, z):
    """
    Generate a Gcode such that the arm controller moves to the cartesian position
    that are passed as parameters

    :param x: x position to there the arm end effector should move
    :param y: y position to there the arm end effector should move
    :param z: z position to there the arm end effector should move
    :return: the actual Gcode, ready to be sent.
    """
    return f"G0 X{x} Y{y} Z{z}".encode('utf-8')


def generate_theta_movement(theta1, theta2, theta3):
    """
    Generate a Gcode such that the arm controller moves the motors to the angles
    specified as parameters

    :param theta1: angle to which the base motor shall move.
    :param theta2: angle to which the shoulder motor shall move.
    :param theta3: angle to which the elbow motor shall move.
    :return: the actual Gcode, ready to be sent.
    """
    return f"G1 X{theta1} Y{theta2} Z{theta3}".encode('utf-8')


def generate_send_to_origin():
    """
    Generates a Gcode such that the arm moves to the original positions.
    This process is called zeroing
    :return: the actual Gcode, ready to be sent.
    """
    return 'G28'.encode('utf-8')


def generate_cancel_movement():
    """
    Generates a Gcode such that the arm controller shall stop the movement that
    the arm is actually doing.
    :return: the actual Gcode, ready to be sent.
    """
    return 'M1'.encode('utf-8')


def generate_request_cartesian_position():
    """
    Generates a Gcode to request the physical cartesian positions at which the
    arm currently is.
    :return: the actual Gcode, ready to be sent.
    """
    return 'M114'.encode('utf-8')


def generate_request_angular_position():
    """
    Generates a Gcode to request the physical angular positions at which the
    arm currently is.
    :return: the actual Gcode, ready to be sent.
    """
    return 'M280'.encode('utf-8')


def generate_request_n_e():
    """
    Generates a Gcode to request the arm controller to send "n" and "e"
    :return: the actual Gcode, ready to be sent.
    """
    return 'I1'.encode('utf-8')


def generate_unsigned_string(unsigned_string):
    return f'I5 {unsigned_string}'.encode('utf-8')


def generate_recalculate_keys():
    return 'I6'.encode('utf-8')


