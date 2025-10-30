#! /usr/bin/env python3
# encoding: UTF-8

# This file is part of Plotlines.

# Plotlines is free software: You can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# Plotlines is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the
# GNU General Public License along with Plotlines.
# If not, see <https://www.gnu.org/licenses/>.


from collections.abc import Generator
import enum
import random

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.coordinates import Coordinates


class Motif:
    """
    https://heterogenoustasks.wordpress.com/2015/01/26/standard-patterns-in-choice-based-games/

    """

    class Edit(enum.Flag):
        FILL = enum.auto()
        FORK = enum.auto()
        JOIN = enum.auto()
        LINK = enum.auto()
        STEM = enum.auto()
        STEP = enum.auto()

    @staticmethod
    def diamond(zone: int = 0):
        # TODO: Allocate label to each node and edge
        nodes = [Node(zone=0), Node(zone=1), Node(zone=2), Node(zone=3), Node(zone=4)]
        edges = [
            nodes[0].connect(nodes[1]),
            nodes[1].connect(nodes[2]),
            nodes[1].connect(nodes[3]),
            nodes[2].connect(nodes[4]),
            nodes[3].connect(nodes[4]),
        ]
        yield from nodes + edges

    @staticmethod
    def join(items: list[Node | Edge], limit: int = None, fwd=True) -> Generator[Node | Edge]:
        nodes = [i for i in items if len(i.connections[0]) == 0]
        limit = len(nodes) if limit is None else min(limit, len(nodes))
        for node in random.sample(nodes, limit):
            lhs = [Node(zone=node.zone), Node(zone=node.zone)]
            yield from lhs
            if fwd:
                yield node.connect(lhs[0])
                yield node.connect(lhs[1])
            else:
                yield lhs[0].connect(node)
                yield lhs[1].connect(node)
