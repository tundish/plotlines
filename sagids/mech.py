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

from collections import Counter
from collections import namedtuple
from decimal import Decimal
from fractions import Fraction
import itertools
import turtle

# Game of three-sixteenths
# + Number the board cyclically 1,3,5,7
# + Initially register set of unique ninths.
# + Initial position on centre points.
# + Reset and replay after target met.

Mark = namedtuple("Mark", ["sector", "region", "spot"])


def pairs(degree=2):
    return itertools.product(range(10), repeat=degree)


def rationalize(seq):
    for pair in seq:
        try:
            yield Fraction(*pair)
        except ZeroDivisionError:
            yield Decimal("inf")


def marks(n_sectors=4, regions=[1, 3, 5, 7]):
    return [
        Mark(*values, spot=n)
        for n, values in enumerate(
            itertools.product(range(n_sectors), regions)
        )
    ]


witness = Counter(rationalize(pairs()))
print(*witness.items(), sep="\n")

grid = marks()
print(*grid, sep="\n")
