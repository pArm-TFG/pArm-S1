from serial import SerialException
from ..gcode import interpreter
from logging import getLogger
from ..gcode import generator

log = getLogger()


def verify_movement_completed(self):
    try:
        gcode = ["J{}".format(x) for x in range(2, 21)]
        found, missed_instructions, line = interpreter.wait_for(self, gcode)
        line_meaning = interpreter.parse_line(line)

        if found and line_meaning == 'Ack':
            found, missed_instructions, line = interpreter.wait_for(self, 'I21')
            if found and line == 'Arrived to position':
                log.info(line)

    except SerialException:
        log.warning("There is no suitable connection with the device")


def request_cartesian_position(self):

    byte_stream = generator.generate_request_cartesian_position()

    try:
        with self.connection as conn:
            conn.write(byte_stream)
    except SerialException:
        log.warning("There is no suitable connection with the device")
    else:
        log.debug(f"Cartesian position requested")


def request_angular_position(self):

    byte_stream = generator.generate_request_angular_position()

    try:
        with self.connection as conn:
            conn.write(byte_stream)
    except SerialException:
        log.warning("There is no suitable connection with the device")
    else:
        log.debug(f"Angular position requested")


def request_recalculate_keys(self):

    byte_stream = generator.generate_recaculate_keys()

    try:
        with self.connection as conn:
            conn.write(byte_stream)
    except SerialException:
        log.warning("There is no suitable connection with the device")
    else:
        log.debug(f"Key recalculation requested")