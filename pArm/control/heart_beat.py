import time
from typing import Optional
from threading import Thread
from logging import getLogger
from serial import SerialException
from .. import Connection

log = getLogger("Roger")


class Heart:
    def __init__(self,
                 beat: int = 0,
                 start_beating: bool = False,
                 conn: Optional[Connection] = None):
        self.beat = f"I7 {beat}".encode('utf-8')
        self._is_beating = start_beating
        self.connection = conn if conn else Connection()
        self._t = Thread(target=lambda: self.background_repeated_heartbeat())
        if start_beating:
            self._t.start()

    @property
    def is_beating(self):
        return self._is_beating

    @is_beating.setter
    def is_beating(self, val: bool):
        self._is_beating = val
        if val and not self._t.is_alive():
            self._t.start()
        elif not val and self._t.is_alive():
            self._t.join()

    def heartbeat_tick(self):
        """
        This function generate a heartbeat. The heartbeat its an int passed as
        parameter to the class
        :return: no return.
        """

        try:
            log.debug('Ticking')
            self.connection.write(self.beat)
        except SerialException:
            log.warning("There is no suitable connection with the device",
                        exc_info=True)

    def background_repeated_heartbeat(self):
        """
        If is_beating is true, this function repeats the beat at an interval of
        .2 seconds. If is_beating is false the heart does not beat.
        :return: no return.
        """
        while self.is_beating:
            self.heartbeat_tick()
            time.sleep(.195)

