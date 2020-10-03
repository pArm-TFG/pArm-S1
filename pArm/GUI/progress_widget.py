#                             pArm-S1
#                  Copyright (C) 2020 - Javinator9889
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#                   (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#               GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
from __future__ import annotations
from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QProgressBar
from time import time, sleep
from typing import Tuple, Optional, Union
from ..utils import AtomicFloat


class Worker(QObject):
    """
    Worker class for counting the remaining time until a given value. Provides
    three signals for handling when a new value is set, the lower and upper
    limits and when it has finished.

    Those signals are:
     - ``update_progress [float]``
     - ``limit_values [tuple of floats]``
     - ``finished [bool]``
    """
    update_progress = QtCore.pyqtSignal(float)
    """ Signal called when a new value is available """

    limit_values = QtCore.pyqtSignal(tuple)
    """ Signal called when the limits are known """

    finished = QtCore.pyqtSignal(bool)
    """ Signal called when the processing has finished """

    def __init__(self, time_object: AtomicFloat):
        super().__init__()
        self.time = time_object

    def work(self):
        """
        Notifies the worker to start. Waits until a value is available
        in the ``AtomicFloat`` object (defaults to -1.0) and then emits the
        lower and upper limit. Finally, starts counting the elapsed time and
        notifies through ``update_progress`` the new value that must be
        displayed. At the end, notifies that it has finished processing
        and quits.
        """
        while not self.time.value != -1.0:
            sleep(.01)

        self.limit_values.emit((0, self.time.value))
        start_time = time()
        finish_time = start_time + self.time.value
        while time() < finish_time:
            self.update_progress.emit(time() - start_time)

        self.finished.emit(True)


class ProgressWidget(QProgressBar):
    """
    ProgressBar class that inherits from QProgressBar implementing an
    anonymous worker for updating the UI with a given value.

    This class basically works the same as QProgressBar but with the addition
    of the two following methods:
     - ``create_worker(time_object: AtomicFloat)``
     - ``run_worker(time_object: Optional[AtomicFloat])``

    Those methods must be called in order to update the progress bar by the
    value stored in ``time_object``.
    """

    @classmethod
    def from_bar(cls,
                 progress_bar: Union[QObject, QProgressBar]) -> ProgressWidget:
        return cls(base=progress_bar)

    def __init__(self, base: Optional[QProgressBar] = None):
        super().__init__()
        self.__base = base
        self._worker: Optional[Worker] = None
        self._thread: Optional[QtCore.QThread] = None

    def __getattr__(self, attr):
        if self.__base:
            return getattr(self.__base, attr)
        return getattr(self, attr)

    def __setattr__(self, attr, value):
        if attr == '_ProgressWidget__base':
            return object.__setattr__(self, attr, value)

        if self.__base:
            return setattr(self.__base, attr, value)
        return setattr(self, attr, value)

    def __getattribute__(self, item):
        if item == '_ProgressWidget__base':
            return super(ProgressWidget, self).__getattribute__(item)
        if hasattr(self.__base, item):
            return object.__getattribute__(self.__base, item)
        return super(ProgressWidget, self).__getattribute__(item)

    def create_worker(self, time_object: AtomicFloat):
        """
        Creates a new worker overwriting any existing one. A reference to an
        existing ``time_object`` must be given every time the worker is created.

        This function attaches signals for knowing which are the limits for the
        progress bar, the new value that must be shown and whether it reaches
        100%.

        :param time_object: the atomic float holder value.
        :type time_object: AtomicFloat
        """
        thread = QtCore.QThread()
        worker = Worker(time_object)
        worker.update_progress.connect(
            lambda progress: self.handle_progress(progress)
        )
        worker.moveToThread(thread)
        thread.started.connect(worker.work)
        worker.limit_values.connect(
            lambda limits: self.handle_limits(limits)
        )
        worker.finished.connect(thread.quit)
        QtCore.QMetaObject.connectSlotsByName(self)

        self._worker = worker
        self._thread = thread

    def run_worker(self, time_object: Optional[AtomicFloat] = None) -> Worker:
        """
        Starts an existing worker (if any) or creates a new one. In that case,
        this function checks if ``time_object`` is not ``None`` and then calls
        ``create_worker`` function.

        :param time_object: the atomic float holder value. Can be ``None`` if
        ``create_worker`` was called before.
        :return: the created Worker.
        :raises ValueError: if ``time_object`` is None and no worker is
        available.
        """
        if not self._worker:
            if not time_object:
                raise ValueError('When creating a worker, time_object cannot '
                                 'be None')
            self.create_worker(time_object)
        self._thread.start()
        return self._worker

    def handle_limits(self, limits: Tuple[float, float]):
        """
        Function that is called whether the running worker has received the
        value from the ``time_object``.

        As the worker works with ``float``, a conversion to ``int`` must be
        done. In this case, the progress bar works with 4 decimals.

        :param limits: a tuple containing both the lower limit and upper limit.
        """
        self.setMinimum(int(round(limits[0], 4) * 10000))
        self.setMaximum(int(round(limits[1], 4) * 10000))
        self.show()

    def handle_progress(self, value: float):
        """
        Function that is called when a new value must be displayed in the
        progress bar. When the progress bar reaches the top, it is hidden.

        As the worker works with ``float``, a conversion to ``int`` must be
        done. In this case, the progress bar works with 4 decimals.

        :param value: the new value that must be displayed.
        """
        if value >= self.maximum():
            self.hide()
        else:
            self.setValue(int(round(value, 4) * 10000))
