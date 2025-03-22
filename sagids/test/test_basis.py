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

    def __init__(self, *args, point_factory=turtle.Vec2D):
        self.points = args
        self.point_factory = point_factory
        self.params = dict(u=Finite(0, 1, type=float))
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

    def basis(self, point, *, pos: float | int, index: int, order: int):
        coeff = self.coefficient(index, order)
        k = coeff * pos ** i * (1 - pos) ** (order - index)
        return k * point

    def __call__(self,  pos: float | int):
        blend = self.blend(pos)
        return [fn(p) for fn, p in zip(blend, self.points)]


class BernsteinTests(unittest.TestCase):

    def test_n_1(self):
        poly = Bernstein()
        for i in range(2):
            with self.subTest(i=i):
                self.assertEqual(poly.coefficient(i, order=1), 1)

        rv = poly.blend(0)
        self.fail(rv)
