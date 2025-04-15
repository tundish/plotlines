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


from collections import defaultdict
import unittest


import dataclasses
from decimal import Decimal
from fractions import Fraction
import itertools
import random
import turtle


class Grid:

    @dataclasses.dataclass
    class Cell:
        spot: turtle.Vec2D
        parent: "Grid" = None

        @property
        def value(self) -> int:
            return {
                0: {0: 1, 1: 7},
                1: {0: 3, 1: 5},
            }[int(self.spot[0]) % 2][int(self.spot[1]) % 2]

    @dataclasses.dataclass
    class Marker:
        value: Fraction = None
        parent: "Grid" = None
        cell: "Cell" = None

    @classmethod
    def build_markers(cls, k=4):
        return [
            cls.Marker(value=v)
            for v in random.sample(
                [Fraction(n, 9) for n in [0, 1, 2, 4, 5, 7, 8]],
                k
            )
        ]

    @classmethod
    def build(cls, n_sectors=4, n_regions=4):
        markers = cls.build_markers(k=n_sectors)
        size = int(Decimal(n_sectors).sqrt() * Decimal(n_regions).sqrt())
        cells = [cls.Cell(turtle.Vec2D(*pos)) for pos in itertools.product(range(size), repeat=2)]
        print(f"{size=}")
        return cls(markers, cells=cells)

    def __init__(self, markers: list = None, cells: list = None):
        self.markers = markers or []
        for mark in self.markers:
            mark.parent = self

        self.cells = cells or []
        for cell in self.cells:
            cell.parent = self


class GridTests(unittest.TestCase):

    def test_markers(self):
        for n in range(8):
            with self.subTest(n=n):
                rv = Grid.build_markers(n)
                self.assertEqual(len(rv), n)
                self.assertEqual(len({i.value for i in rv}), n)

    def test_init(self):
        grid = Grid.build()
        self.assertEqual(len(grid.markers), 4)
        self.assertEqual(len(grid.cells), 16)

    def test_cell_values(self):
        grid = Grid.build()
        rows = defaultdict(list)
        for cell in grid.cells:
            rows[cell.spot[0]].append(cell)

        for row in rows:
            with self.subTest(row=row):
                cells = rows[row]
                if row in [0, 2]:
                    self.assertEqual([cell.value for cell in cells], [1, 7, 1, 7])
                elif row in [1, 3]:
                    self.assertEqual([cell.value for cell in cells], [3, 5, 3, 5])
                print(cells)
        print(f"{rows=}")
        print(f"{grid.cells=}")

