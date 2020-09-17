
def generate_xyz_movement(x,y,z):
    byte_stream = bytes(f"G0 X{x} Y{y} Z{z}", encoding="utf-8")
    return byte_stream


def generate_theta_movement(theta1, theta2, theta3):
    byte_stream = bytes(f"G1 X{theta1} Y{theta2} Z{theta3}", encoding="utf-8")
    return byte_stream


def generate_send_to_origin():
    byte_stream = bytes("G28", encoding="utf-8")
    return byte_stream
