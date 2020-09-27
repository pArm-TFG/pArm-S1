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
    2: ErrorData(logging.ERROR, 'Javier esta xd')
}


def read_buffer_line():
    try:
        with connection as conn:
            line = conn.readline()
    except SerialException:
        log.warning("There is no suitable connection with the device")
    else:
        log.debug("Line read successfully")

    return line


def parse_line(line: Optional[Union[str, bytes]] = None) -> Union[bool, XYZ, Theta, str]:
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
    split_order = m_order.split(' ')
    order_number = int(split_order[0][1:])

    if order_number == 1:
        return True


def parse_j_order(j_order):
    order_number = int(j_order[1:])

    if order_number == 1:
        return 'Ack'
    if 2 <= order_number <= 20:
        return errors[order_number]
    if order_number == 21:
        return 'Arrived to position'


def wait_for(gcode: Union[str, Iterable[str]], timer: int = 5) -> Tuple[bool,
                                                                        List[str],
                                                                        str]:
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
