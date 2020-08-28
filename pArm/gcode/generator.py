
def generate_xyz_movement(x,y,z):
    byte_stream = bytes(f"G0 X{x} Y{y} Z{z}")
    return byte_stream


def generate_theta_movement(theta1, theta2, theta3):
    byte_stream = bytes(f"G1 X{theta1} Y{theta2} Z{theta3}")
    return byte_stream


def generate_send_to_origin(onX, onY, onZ):

    gcode = ['G28']

    if onX:
        gcode.append('X0')
    if onY:
        gcode.append('Y0')
    if onZ:
        gcode.append('Z0')

    axis = ' '.join(gcode[1:]).replace("0", "")
    gcode = ' '.join(gcode)

    return gcode, axis
