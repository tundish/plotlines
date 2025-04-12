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


Mark = namedtuple("Mark", ["sector", "region"])


def pairs(degree=2):
    return itertools.product(range(10), repeat=degree)


def rationalize(seq):
    for pair in seq:
        try:
            yield Fraction(*pair)
        except ZeroDivisionError:
            yield Decimal("inf")


witness = Counter(rationalize(pairs()))
print(*witness.items(), sep="\n")

n_sectors = 4
n_regions = 4

grid = [Mark(*values) for values in itertools.product(range(n_sectors), range(n_regions))]
print(*grid, sep="\n")
