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


import turtle
import unittest

from sagids.basis import Bernstein


class BernsteinTests(unittest.TestCase):

    def test_empty(self):
        poly = Bernstein()
        for i in range(2):
            with self.subTest(i=i):
                self.assertEqual(poly.coefficient(i, order=1), 1)

    def test_n_2(self):
        points = [
            turtle.Vec2D(0, 0),
            turtle.Vec2D(3, 4),
            turtle.Vec2D(5, 0),
        ]
        poly = Bernstein(*points)
        self.assertEqual(poly.order, 2)
        self.assertEqual(poly(0), points[0])
        self.assertEqual(poly(1), points[2])
        self.assertEqual(poly(0.5), (2.75, 2))

