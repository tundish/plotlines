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


import pickle
import unittest

from sagids.coordinates import Coordinates


class CoordinatesTests(unittest.TestCase):

    def test_cardinality(self):
        for n in range(5):
            args = list(range(n))
            with self.subTest(n=n, args=args):
                rv = Coordinates(*args)
                self.assertEqual(len(rv), n)
                self.assertTrue(all(isinstance(i, int) for i in rv))

    def test_coerce(self):
        for n in range(5):
            args = list(range(n))
            with self.subTest(n=n, args=args):
                rv = Coordinates(*args, coerce=complex)
                self.assertEqual(len(rv), n)
                self.assertTrue(all(isinstance(i, complex) for i in rv))

    def test_abs(self):
        c = Coordinates(3, 4)
        rv = abs(c)
        self.assertEqual(rv, 5)

    def test_pickle(self):
        c = Coordinates(3, 4)
        b = pickle.dumps(c)
        d = pickle.loads(b)
        self.assertIsInstance(d, Coordinates)
        self.assertEqual(d, c)

    def test_subtract(self):
        x = Coordinates(1.1, 2.2, 3.3)
        y = Coordinates(0.5, 0.6, 0.7)
        z = x - y
        self.assertIsInstance(z, Coordinates)
        for a, b in zip(z, (0.6, 1.6, 2.6)):
            self.assertAlmostEqual(a, b)

    def test_addition(self):
        x = Coordinates(1.1, 2.2, 3.3)
        y = Coordinates(0.5, 0.6, 0.7)
        z = x + y
        self.assertIsInstance(z, Coordinates)
        for a, b in zip(z, (1.6, 2.8, 4.0, 0.0)):
            self.assertAlmostEqual(a, b)

