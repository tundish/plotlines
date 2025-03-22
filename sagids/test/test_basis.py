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


from collections.abc import Callable
from collections import namedtuple
from fractions import Fraction
import functools
import math
import turtle

import unittest

Finite = namedtuple("Finite", ["min", "max", "modulus", "type"], defaults=[None, int])


class Bernstein:

    def __init__(self, *args):
        self.points = args
        self.coefficients = dict()

    @property
    def order(self) -> int:
        return len(self.points) - 1

    def blend(self, pos) -> list[Callable]:
        return [functools.partial(self.basis, pos=pos, index=n, order=self.order) for n, _ in enumerate(self.points)]

    def coefficient(self, index: int, order=None) -> int:
        f = math.factorial
        return self.coefficients.setdefault(
            (index, order),
            Fraction(f(order), f(index) * f(order - index))
        )

    def basis(self, point, *, pos: float | int, index: int, order: int, coerce: type = float):
        coeff = self.coefficient(index, order)
        k = coeff * pos ** index * (1 - pos) ** (order - index)
        rv = coerce(k) * point
        return rv

    def __call__(self,  pos: float | int):
        blend = self.blend(pos)
        vals = [fn(p) for fn, p in zip(blend, self.points)]
        try:
            return sum(vals[1:], start=vals[0])
        except IndexError:
            return (vals or None) and vals[0]


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

