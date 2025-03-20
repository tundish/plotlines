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


from collections import namedtuple
import unittest

import turtle


Finite = namedtuple("Finite", ["min", "max", "modulus", "type"], defaults=[None, int])


class Bernstein:

    def __init__(self, *args):
        self.params = dict(u=Finite(0, 1, type=float))

    def __call__(self,  *args, vec_factory=turtle.Vec2D):
        return vec_factory(*args)


class BernsteinTests(unittest.TestCase):

    def test_n_1(self):
        poly = Bernstein(0, 1)
        rv = poly(3, 4)
        self.fail(rv)
