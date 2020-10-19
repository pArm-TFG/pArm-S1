from serial import SerialException
from pArm.communications.connection import Connection
from pArm.gcode import interpreter
from logging import getLogger
from pArm.gcode import generator
from pArm.utils.error_data import ErrorData
import logging
from ..utils import AtomicFloat
from typing import Optional

log = getLogger("Roger")
connection = Connection()


def verify_movement_completed(time_object: Optional[AtomicFloat] = None):
    """
    Verifies that, after a movement order has been issued, it completes correctly.
    If not, this function takes care of the errors.
    :param time_object: the atomic float holder value.
    :return: An ErrorData named tuple, in case of an error.
    """
    try:
        gcode = ["J{}".format(x) for x in range(1, 21)]
        found, missed_instructions, line = interpreter.wait_for(gcode)
        line_meaning = interpreter.parse_line(line)

        if found and isinstance(line_meaning, float):
            if time_object:
                time_object.value = line_meaning
            found, missed_instructions, line = interpreter.wait_for('J21')
            if found:
                log.info(line)
            else:
                return ErrorData(logging.ERROR,
                                 'El brazo no ha podido llegar al destino')
        else:
            return line_meaning

    except SerialException:
        log.warning("There is no suitable connection with the device", exc_info=True)


def request_cartesian_position():
    """
    This function sends a Gcode requesting the cartesian positions of the
    arm
    :return: no return
    """
    byte_stream = generator.generate_request_cartesian_position()

    try:
        with connection as conn:
            conn.write(byte_stream)
    except SerialException:
        log.warning("There is no suitable connection with the device", exc_info=True)
    else:
        log.debug(f"Cartesian position requested")


def request_angular_position():
    """
    This function sends a Gcode requesting the angular positions of the
    arm
    :return: no return
    """
    byte_stream = generator.generate_request_angular_position()

    try:
        with connection as conn:
            conn.write(byte_stream)
    except SerialException:
        log.warning("There is no suitable connection with the device", exc_info=True)
    else:
        log.debug(f"Angular position requested")


def request_recalculate_keys():
    """
    This function sends a Gcode requesting the arm controller to re-calculate
    the keys used for the hand-shake. In the current state of the code and project
    this function is not being used.
    :return: no return
    """
    byte_stream = generator.generate_recalculate_keys()

    try:
        with connection as conn:
            conn.write(byte_stream)
    except SerialException:
        log.warning("There is no suitable connection with the device", exc_info=True)
    else:
        log.debug(f"Key recalculation requested")


def request_cancel_movement():
    """
    This function sends a Gcode requesting the arm controller to cancel the
    current movement being made.
    :return: no return
    """
    byte_stream = generator.generate_cancel_movement()
    try:
        with connection as conn:
            conn.write(byte_stream)
    except SerialException:
        log.warning("There is no suitable connection with the device", exc_info=True)
    else:
        log.debug(f"Requested cancel movement")


def request_handshake():
    """
    This function sends a Gcode requesting to begin the handshake procedure.
    If received correctly, the arm controller proceeds to also start the
    handshaking procedure on it end.
    :return: no return.
    """
    byte_stream = generator.generate_request_n_e()
    try:
        if not connection.is_open:
            connection.ser.open()
        connection.write(byte_stream)
    except SerialException:
        log.warning("There is no suitable connection with the device", exc_info=True)
    else:
        log.debug(f"Requested handshake start")
