from ..communications import Connection
from serial import SerialException
from logging import getLogger
from typing import Tuple, Union
from collections import namedtuple
from typing import Optional
from typing import List
from typing import Iterable
from ..utils.error_data import ErrorData
import logging
import time

log = getLogger("Roger")

connection = Connection()

XYZ = namedtuple('XYZ', 'x y z')
Theta = namedtuple('Theta', 't1 t2 t3')

errors = {
    2: ErrorData(logging.ERROR, 'Error en la calibración'),
    3: ErrorData(logging.ERROR, 'GCode desconocido'),
    4: ErrorData(logging.ERROR, 'Posición fuera del rango'),
    5: ErrorData(logging.ERROR, 'El brazo no puede cancelar un movimiento inexistente'),
    6: ErrorData(logging.ERROR, 'Error en el handshake'),
    7: ErrorData(logging.ERROR, 'El brazo ya se esta moviendo'),
    8: ErrorData(logging.ERROR, 'No se han especificado coordenadas para el movimiento cartesiano'),
    9: ErrorData(logging.ERROR, 'No se han especificado coordenadas para el movimiento angular.'),
    10:ErrorData(logging.ERROR, 'Dispositivo no identificado'),
    11:ErrorData(logging.ERROR, 'Desbordamiento del buffers')
}


def read_buffer_line():
    """
    Reads a line from the UART.
    :return: returns the first line read.
    """
    try:
        with connection as conn:
            line = conn.readline()
    except SerialException:
        log.warning("There is no suitable connection with the device")
    else:
        log.debug("Line read successfully")

    return line


def parse_line(line: Optional[Union[str, bytes]] = None) -> Union[bool, XYZ, Theta, str]:
    """
    Parses the line passed as parameter looking for the kind of order that it is
    If no line is passed as parameter, it reads the first line of the buffer.

    Parsing means that this function will decide what kind of order it is and
    will call the corresponding function to react accordingly.
    :param line: The line that needs to be parsed
    :return: calls the corresponding function.
    """
    if not line:
        line = read_buffer_line()

    if isinstance(line, bytes):
        line = line.decode("utf-8")

    if line[0] == "I":
        return parse_i_order(line)
    elif line[0] == "G":
        return parse_g_order(line)
    elif line[0] == "M":
        return parse_m_order(line)
    elif line[0] == "J":
        return parse_j_order(line)


def parse_i_order(i_order):
    """
    This function is called when the order is an I order. It continues to parse
    it to the number of the order and acts accordingly.
    :param i_order: the I order that has to be parsed.
    :return: returns the parameter of the order.
    """
    split_order = i_order.split(' ')
    order_number = int(i_order[0][1:])

    if order_number == 2:
        return split_order[1]
    elif order_number == 3:
        return split_order[1]
    elif order_number == 4:
        return split_order[1]
    elif order_number == 5:
        return True


def parse_g_order(g_order) -> Tuple[float, float, float]:
    """
    This function is called when the order is an G order. It continue to parse
    it to the number of the order and acts accordingly.
    :param g_order: the G order that has to be parsed.
    :return: a namedTuple that contains either the angular values or the
    cartesian ones
    """
    split_order = g_order.split(' ')
    order_number = int(split_order[0][1:])

    if order_number == 0:
        return XYZ(x=float(split_order[1][1:]),
                   y=float(split_order[2][1:]),
                   z=float(split_order[3][1:]))

    elif order_number == 1:
        return Theta(t1=float(split_order[1][1:]),
                     t2=float(split_order[2][1:]),
                     t3=float(split_order[3][1:]))


def parse_m_order(m_order):
    """
    This function is called when the order is an M order. It continue to parse
    it to the number of the order and acts accordingly.
    :param m_order: the M order that has to be parsed.
    :return: returns True if the order is type M1
    """
    split_order = m_order.split(' ')
    order_number = int(split_order[0][1:])

    if order_number == 1:
        return True


def parse_j_order(j_order):
    """
    This function is called when the order is an J order. It continue to parse
    it to the number of the order and acts accordingly.
    :param j_order: the J order that has to be parsed.
    :return: Either confirmation messages (For J1 and J21) or error codes
    (from J2 to J20)
    """
    order_number = int(j_order[1:])

    if order_number == 1:
        return float(j_order.split()[1])
    if 2 <= order_number <= 20:
        return errors[order_number]
    if order_number == 21:
        return 'Arrived to position'


def wait_for(gcode: Union[str, Iterable[str]], timer: int = 5) -> Tuple[bool,
                                                                        List[str],
                                                                        str]:
    """
    This function keeps reading the buffer until it finds the GCode that its
    passed as parameter. It is also capable to wait for an order from within an
    interval of order.

    :param gcode: The order or interval of orders that the function has to
    look for
    :param timer: The time that has to elapse until the function reaches timeout
    and stops looking for the specified order
    :return: Boolean, to know if the function finished because it found the
    order or because it reached timeout.
    List, containing other orders that have been read that were not the one that
    the function was specifically looking for.
    String, contains the whole line where the order has been found.
    """
    missed_inst = []
    timeout = time.time() + timer

    line = connection.sreadline()

    def check_valid(c_line, gcode) -> bool:
        return c_line in gcode if isinstance(gcode, Iterable) else c_line != gcode

    while not check_valid(line.split()[0], gcode) and time.time() <= timeout:
        if line != '':
            missed_inst.append(line)
        time.sleep(0.1)

    return timeout < time.time(), missed_inst, line
