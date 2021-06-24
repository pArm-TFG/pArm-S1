#                             pArm - S1
#                  Copyright (C) 2021 - Javinator9889
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
"""
Log file containing the :func:`init_logging` method which initializes and creates the logger
"""
import gzip
import logging
import os
import shutil
from logging.handlers import RotatingFileHandler
from typing import Optional

LOG_DEFAULT_FORMAT = "%(asctime)s | [%(levelname)s]:\t%(message)s"
"""
Default logging format used when outputting messages. It has the form:
    > HH:MM:SS:ssss | [message level]:  message
"""
logging.basicConfig(level=logging.DEBUG, format=LOG_DEFAULT_FORMAT)


def file_rotator(src: str, dest: str):
    """
    Custom file rotator that creates a compressed GZIP object from the given log file.

    :param src: the source log file.
    :param dest: the destination compressed GZIP file.
    """
    with open(src, "rb") as sf, gzip.open(dest, "wb") as gzfile:
        shutil.copyfileobj(sf, gzfile)
    os.remove(src)


def namer(name: str) -> str:
    """
    Custom "namer" that appends ``.gz`` to the provided filename.

    :param name: the log filename.
    :return: the filename with ``.gz`` extension.
    :rtype: :obj:`str`
    """
    return f"{name}.gz"


def init_logging(
    logger_name: Optional[str] = None,
    log_file: Optional[str] = None,
    console_level: int = logging.DEBUG,
    file_level: int = logging.DEBUG,
    log_format: str = LOG_DEFAULT_FORMAT,
    enable_console_logging: bool = False,
) -> logging.Logger:
    """
    Creates a custom logger (or uses the :class:`logging.RootLogger`) that is able to output to
    both console and file, which is useful in development environments and production ones.

    By default, it rotates the log files when they are about 2MB size and compress them for
    later visualization and usage.

    :param logger_name: the name of the logger, or ``None`` to use :class:`logging.RootLogger`.
    :param log_file: the filename in which logs will be stored. If ``None``, no file will be used.
    :param console_level: the logging level of the console, by default :attr:`logging.DEBUG`.
    :param file_level: the logging level of the file, by default :attr:`logging.DEBUG`.
    :param log_format: the logging format to use. By default, uses the one defined at
           :attr:`LOG_DEFAULT_FORMAT`.
    :param enable_console_logging: whether to log to the console or not. Defaults to ``False``.
    :return: an instance of the created :class:`logging.Logger`.
    """
    fmt = logging.Formatter(log_format)
    log = logging.getLogger(logger_name)

    for handler in log.handlers:
        if isinstance(handler, logging.StreamHandler):
            if enable_console_logging:
                handler.setLevel(console_level)
                handler.setFormatter(fmt)
            else:
                log.handlers.remove(handler)

    if log_file is not None:
        file_handler = RotatingFileHandler(log_file, maxBytes=1 << 20, backupCount=5, delay=True)
        file_handler.rotator = file_rotator
        file_handler.namer = namer
        file_handler.setLevel(file_level)
        file_handler.setFormatter(fmt)
        log.addHandler(file_handler)

    return log


def add_handler(handler: logging.Handler,
                logger_name: Optional[str] = None,
                level: int = logging.DEBUG,
                log_format: Optional[str] = None):
    """
    Adds a new handler to an existing logger, with the specified formatter
    in ```init_logging```. If a new format is specified (is not None) then
    it will be used for this handler.

    :param handler: the new handler to be added.
    :param logger_name: the logger name to which add the handler.
    :param level: the logging level for that formatter.
    :param log_format: the log format used if not formatter was created.
    """
    logger = logging.getLogger(logger_name)
    fmt = logging.Formatter(log_format) if log_format else logging.Formatter(LOG_DEFAULT_FORMAT)
    handler.setFormatter(fmt)
    handler.setLevel(level)

    logger.addHandler(handler)
