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
import itertools
from abc import ABC, abstractmethod
from threading import Lock
from typing import Optional, Generic, TypeVar

T = TypeVar('T')


class Atomic(ABC, Generic[T]):
    """
    Base class for an Atomic container. It can be initialized with any type
    ``T``, but then that type must be respected and cannot be changed.
    """
    def __init__(self,
                 initial_value: Optional[T] = None,
                 step: Optional[T] = None):
        self.rlock = Lock()

    @property
    @abstractmethod
    def value(self) -> T:
        """
        Atomically obtains the stored value.
        :return: the stored value.
        """
        pass

    @value.setter
    @abstractmethod
    def value(self, val: T):
        """
        Atomically sets the stored value.
        :param val: the new value to store.
        :type val: T
        """
        pass


class AtomicFloat(Atomic[float]):
    """
    Atomically stores a floating number.
    """
    def __init__(self, initial_value=.0):
        super().__init__(initial_value)
        self._val = initial_value

    @property
    def value(self) -> float:
        """
        Atomically obtains the stored value.
        :return: the stored value as float.
        """
        with self.rlock:
            return self._val

    @value.setter
    def value(self, val: float):
        """
        Atomically sets the stored value.
        :param val: the new value to store.
        :type val: float
        """
        with self.rlock:
            self._val = val


class AtomicInteger(Atomic[int]):
    """
    Atomically stores an integer.
    """
    def __init__(self, initial_value=0, step=1):
        super().__init__(initial_value, step)
        self._step = step
        self._number_of_read = 0
        self._counter = itertools.count(initial_value, step)
        self._read_lock = Lock()

    @property
    def value(self) -> int:
        """
        Atomically obtains the stored value.
        :return: the stored value as int.
        """
        with self._read_lock:
            value = next(self._counter) - self._number_of_read
            self._number_of_read += 1
        return value

    @value.setter
    def value(self, val: int):
        """
        Atomically sets the stored value.
        :param val: the new value to store.
        :type val: int
        """
        with self.rlock:
            self._counter = itertools.count(val, self._step)
            self._number_of_read = 0

    def increment(self):
        """
        Increments the stored value with the given step.
        """
        next(self._counter)
