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


import dataclasses
from decimal import Decimal
from fractions import Fraction
import itertools
import pprint
import random
import turtle


class Grid:

    @dataclasses.dataclass(frozen=True)
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
        id: int
        value: Fraction = None
        parent: "Grid" = None
        cell: "Cell" = None

        @property
        def zone(self):
            if not self.cell:
                return []
            quadrant = tuple(i // 2 for i in self.cell.spot)
            return [i for i in self.parent.cells if i[0] // 2 == quadrant[0] and i[1] // 2 == quadrant[1]]

        def visits(self, marker: "Marker"):
            vector = marker.cell.spot - self.cell.spot
            return abs(vector[0]) == abs(vector[1])

    @classmethod
    def build_markers(cls, k=4):
        return [
            cls.Marker(id=n+1, value=v)
            for n, v in enumerate(random.sample(
                [Fraction(n, 9) for n in [1, 2, 4, 5, 7, 8]],
                k
            ))
        ]

    @classmethod
    def build(cls, n_sectors=4, n_regions=4):
        rv = cls(markers=cls.build_markers(k=n_sectors))
        size = int(Decimal(n_sectors).sqrt() * Decimal(n_regions).sqrt())
        rv.cells = {
            pos: cls.Cell(turtle.Vec2D(*pos), parent=rv)
            for pos in itertools.product(range(size), repeat=2)
        }
        return rv

    def __init__(self, markers: list = None, cells: dict = None):
        self.markers = {i.id: i for i in markers}
        for mark in self.markers.values():
            mark.parent = self

        self.cells = cells or dict()

    def partition(self) -> list["Cell"]:
        markers = []
        pool = set(self.cells.values())
        while len(markers) < len(self.markers):
            cell = random.choice(list(pool))
            if not any(cell in m.zone for m in markers):
                m = self.Marker(len(markers), parent=self, cell=cell)
                if not any(m.visits(i) for i in markers):
                    markers.append(m)
                    zone = [self.Cell(spot=spot, parent=self) for spot in m.zone]
                    pool = pool - set(zone)
        return [m.cell for m in markers]

    def mark(self, *args: tuple["Cell"]):
        for cell, marker in zip(args, self.markers.values()):
            marker.cell = self.cells[cell.spot]
        return self


def run():
    grid = Grid.build()
    grid.mark(*grid.partition())
    pprint.pprint(vars(grid))


if __name__ == "__main__":
    run()
