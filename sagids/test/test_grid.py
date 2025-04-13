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


import unittest


import dataclasses
from fractions import Fraction


class Grid:

    @dataclasses.dataclass
    class Register:
        value: Fraction = None

    def __init__(self, slots=[]):
        self.slots = []


class GridTests(unittest.TestCase):

    def test_init(self):
        grid = Grid()

