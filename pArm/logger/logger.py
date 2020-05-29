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


def setup_logging(logger_name: str,
                  log_file: str,
                  level=logging.DEBUG,
                  logging_format: str = "%(process)d - %(asctime)s | [%("
                                        "levelname)s]: %(message)s",
                  log_to_stdout: bool = True) -> logging:
    """
    Creates a new logging which can log to both stdout and/or file

    :param logger_name: the logger identifying name.
    :param log_file: the logging file.
    :param level: logging level - defaults to DEBUG.
    :param logging_format: custom logging formatter.
    :param log_to_stdout: whether to log to console or not - defaults True.
    :return: the logger.
    """
    from os import path
    from os import makedirs

    log_dir = path.dirname(path.abspath(log_file))
    if not path.exists(log_dir):
        makedirs(log_dir)

    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(logging_format)
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)
    if log_to_stdout:
        logger.addHandler(logging.StreamHandler())

    return logger
