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


import enum
import unittest

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
        LINE = enum.auto()
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
    def connections(node: Node):
        l_edges = [edge for edge in node.edges if node.uid in edge.ports[1].joins]
        r_edges = [edge for edge in node.edges if node.uid in edge.ports[0].joins]
        return (l_edges, r_edges)

    @staticmethod
    def ljoin(items: list[Node | Edge]) -> list[Node | Edge]:
        nodes = [i for i in items if len(Motif.connections(i)[0]) == 0]
        for node in nodes:
            lhs = [Node(zone=node.zone), Node(zone=node.zone)]
            items.extend(lhs)
            items.append(lhs[0].connect(node))
            items.append(lhs[1].connect(node))
        return items


class MotifTests(unittest.TestCase):

    def test_one_ljoin(self):
        group = [Node()]
        items = Motif.ljoin(group)
        self.assertEqual(len(items), 5)

        nodes = [i for i in items if isinstance(i, Node)]
        self.assertEqual(len(nodes), 3)
        self.assertIn(group[0], nodes)

    def test_diamond(self):
        items = list(Motif.diamond())
