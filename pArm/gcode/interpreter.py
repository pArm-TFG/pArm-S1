from ..communications import Connection
from serial import SerialException
from logging import getLogger
from typing import Tuple, Union
from collections import namedtuple

log = getLogger("Roger")

connection = Connection()


def read_buffer_line():
    try:
        with connection as conn:
            line = conn.readline()
    except SerialException:
        log.warning("There is no suitable connection with the device")
    else:
        log.debug("Line read successfully")

    return line


def parse_line():
    line = read_buffer_line()
    readable_line = line.decode("utf-8")

    if readable_line[0] == "I":
        parse_i_order(readable_line)
    elif readable_line[0] == "G":
        parse_g_order(readable_line)
    elif readable_line[0] == "M":
        parse_m_order(readable_line)


def parse_i_order(i_order):
    order_number = int(i_order[0][1:])

    if order_number == 1:
        pass
        # TODO


def parse_g_order(g_order) -> Union[float, str, Tuple[float, float, float]]:
    split_order = g_order.split(' ')
    order_number = int(split_order[0][1:])

    XYZ = namedtuple('XYZ', 'x y z')
    Theta = namedtuple('Theta', 't1 t2 t3')

    if order_number == 0:
        return XYZ(x=float(split_order[1][1:]),
                   y=float(split_order[2][1:]),
                   z=float(split_order[3][1:]))

    elif order_number == 1:
        return Theta(t1=float(split_order[1][1:]),
                     t2=float(split_order[2][1:]),
                     t3=float(split_order[3][1:]))


def parse_m_order(m_order):
    split_order = m_order.split(' ')
    order_number = int(split_order[0][1:])

    if order_number == 1:
        return True
