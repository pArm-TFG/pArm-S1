
def generate_xyz_movement(x,y,z):
    return f"G0 X{x} Y{y} Z{z}".encode('utf-8')


def generate_theta_movement(theta1, theta2, theta3):
    return f"G1 X{theta1} Y{theta2} Z{theta3}".encode('utf-8')


def generate_send_to_origin():
    return 'G28'.encode('utf-8')


def generate_cancel_movement():
    return 'M1'.encode('utf-8')


def generate_request_cartesian_position():
    return 'M114'.encode('utf-8')


def generate_request_angular_position():
    return 'M280'.encode('utf-8')


def generate_request_n_e():
    return 'I1'.encode('utf-8')


def generate_unsigned_string(unsigned_string):
    return f"I5 {unsigned_string}".encode('utf-8')


