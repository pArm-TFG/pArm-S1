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
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


__formatter = None


def init_logging(logger_name: Optional[str] = None,
                 log_file: Optional[str] = None,
                 console_level: int = logging.DEBUG,
                 file_level: int = logging.WARNING,
                 log_format: str = "%(process)d - %(asctime)s | [%("
                                   "levelname)s]: %(message)s") -> logging:
    """
    Creates a custom logging that outputs to both console and file, if
    filename provided. Automatically cleans-up old logs during runtime and
    allows customization of both console and file levels in addition to the
    formatter.

    :param logger_name: the logger name for later obtaining it.
    :param log_file: a filename for saving the logs during execution - can be
                    `None`
    :param console_level: the logging level for console.
    :param file_level: the logging level for the file.
    :param log_format: the logging format.

    :return: the created logging instance
    """
    global __formatter
    __formatter = logging.Formatter(log_format)
    logger = logging.getLogger(logger_name)
    if getattr(logger, 'created', False):
        return logger
    setattr(logger, 'created', True)
    for handler in logger.handlers:
        if type(handler) is logging.StreamHandler:
            handler.setLevel(console_level)
            handler.setFormatter(__formatter)

    def file_rotator(source: str, dest: str):
        """
        Custom file rotator for creating compressed logging files.

        :param source: source filename.
        :param dest: destination filename.
        """
        import gzip
        import shutil

        with open(source, "rb") as in_file:
            with gzip.open(dest, "wb") as out_file:
                shutil.copyfileobj(in_file, out_file)

    def namer(name: str) -> str:
        """
        Custom namer implementation as we are gzipping files.

        :param name: the name to append .gz
        :return: the name with .gz extension
        """
        return f"{name}.gz"

    if log_file:
        old_log = os.path.exists(log_file)
        file_handler = RotatingFileHandler(log_file,
                                           mode='a',
                                           maxBytes=2 << 20,
                                           backupCount=5)
        file_handler.rotator = file_rotator
        file_handler.namer = namer
        file_handler.setLevel(file_level)
        file_handler.formatter = __formatter
        if old_log:
            file_handler.doRollover()
        logger.addHandler(file_handler)

    return logger


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
    global __formatter
    fmt = logging.Formatter(log_format) if log_format else __formatter
    handler.setFormatter(fmt)
    handler.setLevel(level)

    logger.addHandler(handler)
