from threading import Thread
from .. import Connection
from serial import SerialException
from logging import getLogger
from ..gcode import generator
import time

connection = Connection()
log = getLogger("Roger")


class Heart:

    def __init__(self, beat: int = 0, start_beating: bool = False):

        self.beat = beat
        self.is_beating = start_beating
        if start_beating:
            t = Thread(target=lambda: self.background_repeated_heartbeat())
            t.start()

    def heartbeat_tick(self):
        """
        This function generate a heartbeat. The heartbeat its an int passed as
        parameter to the class
        :return: no return.
        """

        byte_stream = generator.generate_heart_beat(self.beat)

        try:
            with connection as conn:
                conn.write(byte_stream)
        except SerialException:
            log.warning("There is no suitable connection with the device")

    def background_repeated_heartbeat(self):
        """
        If is_beating is true, this function repeats the beat at an interval of
        .2 seconds. If is_beating is false the heart does not beat.
        :return: no return.
        """
        while self.is_beating:
            self.heartbeat_tick()
            time.sleep(.2)

