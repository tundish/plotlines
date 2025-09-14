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


import unittest

from sagids.board import Board
from sagids.board import Edge
from sagids.board import Node
from sagids.board import Port
from sagids.coordinates import Coordinates


class BoardTests(unittest.TestCase):

    def test_edge_init(self):
        edge = Edge((1, 3), (19, 12))
        self.assertEqual(len(edge.ports), 2)
        self.assertTrue(all(isinstance(p.pos, Coordinates) for p in edge.ports), edge.ports)
        self.assertEqual(edge.ports[0].pos, (1, 3))
        self.assertEqual(edge.ports[1].pos, (19, 12))

    def test_node_init(self):
        node = Node((13, 14))
        self.assertIsInstance(node.pos, Coordinates)
        self.assertEqual(node.pos, (13, 14))

    def test_node_connect(self):
        nodes = [Node(), Node()]
        edge = nodes[0].connect(nodes[1])
        self.assertIsInstance(edge, Edge)
        self.assertEqual(edge.ports[0].joins, {edge, nodes[0]})
        self.assertEqual(edge.ports[1].joins, {edge, nodes[1]})
        self.assertEqual(nodes[0].ports[0].joins, {edge, nodes[0]})
        self.assertEqual(nodes[1].ports[0].joins, {edge, nodes[1]})

        self.assertIn(nodes[1], nodes[0].nearby)
        self.assertNotIn(nodes[0], nodes[0].nearby)
        self.assertIn(nodes[0], nodes[1].nearby)
        self.assertNotIn(nodes[1], nodes[1].nearby)
