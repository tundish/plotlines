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
import random


class Grid:

    @dataclasses.dataclass
    class Register:
        value: Fraction = None

    @classmethod
    def build_registers(cls, k=4):
        return [
            cls.Register(value=v)
            for v in random.sample(
                [Fraction(n, 9) for n in [0, 1, 2, 4, 5, 7, 8]],
                k
            )
        ]

    @classmethod
    def build(cls, n_sectors=4, n_regions=4):
        marks = cls.build_registers(k=n_sectors)
        return cls(marks)

    def __init__(self, marks: list = None, slots: list = None):
        self.marks = marks or []
        self.slots = slots or []


class GridTests(unittest.TestCase):

    def test_registers(self):
        for n in range(8):
            with self.subTest(n=n):
                rv = Grid.build_registers(n)
                self.assertEqual(len(rv), n)
                self.assertEqual(len({i.value for i in rv}), n)

    def test_init(self):
        grid = Grid.build()
        self.assertEqual(len(grid.marks), 4)
        print(f"{grid=}")

