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
from typing import Union


class RSA:
    def __init__(self, e: int, n: int):
        self.e = e
        self.n = n

    def verify(self, message: Union[int, str]) -> Union[int, str]:
        """
        This function is used to "un-sign" the control string received from the
        arm controller.
        :param message: the string to be "un-signed"
        :return: the unsigned string
        """
        if self.n == 1:
            return ''

        if type(message) == int:
            return right_to_left(message, self.e, self.n)
        elif type(message) == str:
            verified_message = list()
            for msg_val in message.split():
                try:
                    val = int(msg_val)
                    verified_message.append(
                        chr(right_to_left(val, self.e, self.n))
                    )
                except ValueError:
                    del verified_message
                    raise AttributeError(
                        f'message contents must be an integer - {msg_val} is '
                        f'invalid')
            return ''.join(verified_message)
        else:
            raise AttributeError(
                f'message must be int or str, not {type(message)}')

    def encrypt(self, message: Union[int, str]) -> Union[int, str]:
        """
        This function is used to encrypt either an integer or str. This is
        used mainly for encrypting the signed message sent by S2.

        :param message: a string or int to be encrypted.
        :return: the encrypted message.
        """
        if self.n == 1:
            return ''

        if type(message) == int:
            return right_to_left(message, self.e, self.n)
        elif type(message) == str:
            encrypted_message = list()
            for char in message:
                encrypted_message.append(
                    str(right_to_left(ord(char), self.e, self.n))
                )
            return ' '.join(encrypted_message)
        else:
            raise AttributeError(
                f'message must be int or str, not {type(message)}')


def right_to_left(number: int, exp: int, mod: int) -> int:
    """
    This function does the math of the encryption process.
    :param number: A number to be encripted
    :param exp: The exponent of the mathematical operation used to do the
    actual encryption
    :param mod: The module of the mathematical operation used to do the
    actual encryption
    :return: the encrypted number.
    """
    ret: int = 1
    while exp > 0:
        if exp % 2 == 1:
            ret = (ret * number) % mod
        exp >>= 1
        number = (number * number) % mod

    return ret
