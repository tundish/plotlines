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

    class Edit(enum.Enum):
        FORK = enum.auto()
        JOIN = enum.auto()
        LINK = enum.auto()
        LOOP = enum.auto()
        STEP = enum.auto()
        COPY = enum.auto()
        FILL = enum.auto()

    def __init__(self):
        pass

    def method(self):
        return self.join

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
    def fork(items: list[Node | Edge], limit: int = None, fwd=True, stems=2, **kwargs) -> Generator[Node | Edge]:
        if fwd:
            leaves = [i for i in items if isinstance(i, Node) and len(i.connections[1]) == 0]
        else:
            leaves = [i for i in items if isinstance(i, Node) and len(i.connections[0]) == 0]

        limit = len(leaves) if limit is None else min(limit, len(leaves))
        for node in random.sample(leaves, limit):
            nodes = [Node(zone=node.zone) for _ in range(stems)]
            yield from nodes
            for n in nodes:
                if fwd:
                    yield node.connect(n)
                else:
                    yield n.connect(node)

    @staticmethod
    def join(items: list[Node | Edge], limit: int = None, fwd=True, stems=2, **kwargs) -> Generator[Node | Edge]:
        if fwd:
            leaves = {i for i in items if isinstance(i, Node) and len(i.connections[0]) == 0}
        else:
            leaves = {i for i in items if isinstance(i, Node) and len(i.connections[1]) == 0}

        n = 0
        limit = len(leaves) // 2 if limit is None else min(limit, len(leaves) // 2)
        while n < limit:
            n += 1
            nodes = random.sample(list(leaves), 2)
            node = Node(zone=nodes[0].zone)
            leaves -= set(nodes)
            yield node
            if fwd:
                yield nodes[0].connect(node)
                yield nodes[1].connect(node)
            else:
                yield node.connect(nodes[0])
                yield node.connect(nodes[1])

    @staticmethod
    def link(items: list[Node | Edge], limit: int = None, fwd=True, stems=2, **kwargs) -> Generator[Node | Edge]:
        if fwd:
            nodes = [i for i in items if isinstance(i, Node) and i.connections[1]]
        else:
            nodes = [i for i in items if isinstance(i, Node) and i.connections[0]]

        n = 0
        limit = len(nodes) if limit is None else min(limit, len(nodes))
        while n < limit:
            n += 1
            node = random.choice(nodes)
            other = random.choice(node.nearby)
            rv = Node(zone=node.zone)
            yield rv
            if fwd:
                yield node.connect(rv)
                yield rv.connect(other)
            else:
                yield rv.connect(node)
                yield other.connect(rv)

    @staticmethod
    def loop(items: list[Node | Edge], limit: int = 1, fwd=True, **kwargs) -> Generator[Node | Edge]:
        if fwd:
            leaves = [i for i in items if isinstance(i, Node) and len(i.connections[1]) == 0]
        else:
            leaves = [i for i in items if isinstance(i, Node) and len(i.connections[0]) == 0]

        n = 0
        limit = len(leaves) if limit is None else min(limit, len(leaves))
        while n < limit:
            n += 1
            leaf = random.choice(leaves)
            node = random.choice(leaf.nearby)
            if fwd:
                yield leaf.connect(node)
            else:
                yield node.connect(leaf)
