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
        for n in range(7):
            with self.subTest(n=n):
                rv = Grid.build_markers(n)
                self.assertEqual(len(rv), n)
                self.assertEqual(len({i.value for i in rv}), n)

    def test_init(self):
        grid = Grid.build()
        self.assertEqual(len(grid.markers), 4)
        self.assertEqual(set(grid.markers), {1, 2, 3, 4})
        self.assertEqual(len(grid.cells), 16)
        self.assertIn((0, 0), grid.cells)

    def test_cell_values(self):
        grid = Grid.build()
        rows = defaultdict(list)
        for cell in grid.cells.values():
            rows[cell.spot[0]].append(cell)

        for row in rows:
            with self.subTest(row=row):
                cells = rows[row]
                if row in [0, 2]:
                    self.assertEqual([cell.value for cell in cells], [1, 7, 1, 7])
                elif row in [1, 3]:
                    self.assertEqual([cell.value for cell in cells], [3, 5, 3, 5])

    def test_makers_aligned(self):
        grid = Grid.build()
        rows = defaultdict(list)
        grid.mark((0, 1), (1, 0), (2, 1), (3, 2))
        self.assertTrue(grid.markers[1].is_aligned(grid.markers[2]))
        self.assertTrue(grid.markers[2].is_aligned(grid.markers[1]))
        self.assertTrue(grid.markers[2].is_aligned(grid.markers[3]))
        self.assertTrue(grid.markers[2].is_aligned(grid.markers[4]))
        self.assertTrue(grid.markers[3].is_aligned(grid.markers[2]))
        self.assertTrue(grid.markers[3].is_aligned(grid.markers[4]))
        self.assertTrue(grid.markers[4].is_aligned(grid.markers[3]))
        self.assertTrue(grid.markers[4].is_aligned(grid.markers[2]))
        self.assertFalse(grid.markers[4].is_aligned(grid.markers[1]))
        self.assertFalse(grid.markers[3].is_aligned(grid.markers[1]))
        self.assertFalse(grid.markers[1].is_aligned(grid.markers[3]))
        self.assertFalse(grid.markers[1].is_aligned(grid.markers[4]))

    def test_marker_zone(self):
        grid = Grid.build()
        grid.mark((1, 0), (0, 2), (2, 1), (3, 2))

        witness = set()
        for marker in grid.markers.values():
            with self.subTest(marker=marker):
                self.assertEqual(len(marker.zone), 4, marker.zone)
                self.assertFalse(witness.intersection(set(marker.zone)))
                witness = witness.union(set(marker.zone))
