from ..communications import Connection
from serial import SerialException
from logging import getLogger

log = getLogger("Roger")

connection = Connection()
key = ""

def read_public_key():
    try:
        with connection as conn:
            msg_in_bytes = conn.readline()
    except SerialException:
        log.warning("There is no suitable connection with the device")
    else:
        log.debug("Public key received")

    readable_msg = msg_in_bytes.decode("utf-8")
    if readable_msg[0] == "I":
        if