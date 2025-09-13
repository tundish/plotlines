#! /usr/bin/env python3
# encoding: UTF-8

# This file is part of SaGiDS.

# SaGiDS is free software: You can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# SaGiDS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the
# GNU General Public License along with SaGiDS.
# If not, see <https://www.gnu.org/licenses/>.


import math


class Coordinates(tuple):

    def __new__(cls, *args, coerce=None):
        if coerce:
            args = [coerce(i) for i in args]
        return tuple.__new__(cls, args)

    def __abs__(self):
        return math.hypot(*self)

    def __getnewargs__(self):
        return self

    def __sub__(self, other):
        return self.__class__(*[a - b for a, b in zip(self, other)])

