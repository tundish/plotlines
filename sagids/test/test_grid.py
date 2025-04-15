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

from sagids.grid import Grid


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
        self.assertEqual(set(grid.markers), {1, 2, 3, 4})
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
        print(f"{grid.cells=}")

    def test_cell_sight(self):
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
        print(f"{grid.cells=}")

