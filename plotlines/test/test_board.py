
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


from decimal import Decimal
from fractions import Fraction
import tkinter as tk
import turtle
import unittest

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.board import Port
from plotlines.coordinates import Coordinates


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

    def test_node_nearby(self):
        nodes = [Node(), Node()]
        edge = nodes[0].connect(nodes[1])
        self.assertIn(nodes[1], nodes[0].nearby)
        self.assertNotIn(nodes[0], nodes[0].nearby)
        self.assertIn(nodes[0], nodes[1].nearby)
        self.assertNotIn(nodes[1], nodes[1].nearby)

    def test_node_edges(self):
        nodes = [Node(), Node()]
        edge = nodes[0].connect(nodes[1])

        for node in nodes:
            with self.subTest(node=node):
                self.assertIsInstance(node.edges, list)
                self.assertIn(edge, node.edges)
                self.assertEqual(len(node.edges), 1)

    def test_node_spacing_node_self(self):
        node = Node((1, 3))

        spacing = node.spacing(node)
        self.assertEqual(len(spacing), 1)
        space = min(spacing.values())
        self.assertEqual(space, 0)

    def test_node_spacing_node_other(self):
        nodes = [Node((1, 3)), Node((19, 12))]

        spacing = nodes[0].spacing(nodes[1])
        self.assertEqual(len(spacing), 1)
        space = min(spacing.values())
        self.assertAlmostEqual(space, 20, places=0)

    def test_node_spacing_edge(self):
        edge = Edge((1, 3), (19, 12))
        node = Node((13, 4))

        spacing = node.spacing(edge)
        self.assertEqual(len(spacing), 3, spacing)
        space = min(spacing.values())
        self.assertAlmostEqual(space, 4.5, places=1)

    def test_frame(self):
        points = (Coordinates(0, 0), Coordinates(10, 10))
        check = (Coordinates(-0.5, -0.5), Coordinates(10.5, 10.5))
        self.assertEqual(Board.frame(*points), check)

        points = (Coordinates(0, 0), Coordinates(0, 10))
        check = (Coordinates(-0.5, -0.5), Coordinates(0.5, 10.5))
        self.assertEqual(Board.frame(*points), check)

    def test_scale_factor(self):
        geom = (400, 300)
        frame = (Coordinates(1.50, 1.50, coerce=Decimal), Coordinates(12.50, 2.50, coerce=Decimal))
        scale = Board.scale_factor(geom, frame)
        check = Fraction(909, 25)
        self.assertEqual(scale, check)

    def test_style_graph(self):
        nodes = [
            Node((1, 8)),
            Node((6, 3)),
            Node((6, 6)),
            Node((6, 9)),
            Node((6, 12)),
            Node((11, 4), area=16),
            Node((10, 8)),
            Node((12.5, 11.5), area=9),
            Node((17, 1)),
            Node((17, 4)),
            Node((17, 7)),
            Node((17, 10)),
            Node((17, 13)),
        ]
        edges = [
            nodes[0].connect(nodes[3]),
            nodes[3].connect(nodes[2]),
            nodes[2].connect(nodes[1]),
            nodes[3].connect(nodes[4]),
            nodes[1].connect(nodes[5]),
            nodes[2].connect(nodes[5]),
            nodes[3].connect(nodes[6]),
            nodes[4].connect(nodes[7]),
            nodes[5].connect(nodes[8]),
            nodes[5].connect(nodes[9]),
            nodes[5].connect(nodes[10]),
            nodes[6].connect(nodes[10]),
            nodes[7].connect(nodes[11]),
            nodes[7].connect(nodes[12]),
        ]
        edges[0].ports[0].pos = Coordinates(2, 8)
        edges[0].ports[1].pos = Coordinates(5, 9)

        edges[1].ports[0].pos = Coordinates(6, 5)
        edges[1].ports[1].pos = Coordinates(6, 4)

        edges[2].ports[0].pos = Coordinates(6, 8)
        edges[2].ports[1].pos = Coordinates(6, 7)

        edges[3].ports[0].pos = Coordinates(6, 10)
        edges[3].ports[1].pos = Coordinates(6, 11)

        edges[4].ports[0].pos = Coordinates(7, 3)
        edges[4].ports[1].pos = Coordinates(9, 3)

        edges[5].ports[0].pos = Coordinates(7, 6)
        edges[5].ports[1].pos = Coordinates(9, 5)

        edges[6].ports[0].pos = Coordinates(7, 9)
        edges[6].ports[1].pos = Coordinates(9, 8)

        edges[7].ports[0].pos = Coordinates(7, 12)
        edges[7].ports[1].pos = Coordinates(11, 12)

        edges[8].ports[0].pos = Coordinates(13, 3)
        edges[8].ports[1].pos = Coordinates(16, 1)

        edges[9].ports[0].pos = Coordinates(13, 4)
        edges[9].ports[1].pos = Coordinates(16, 4)

        edges[10].ports[0].pos = Coordinates(13, 5)
        edges[10].ports[1].pos = Coordinates(16, 7)

        edges[11].ports[0].pos = Coordinates(11, 8)
        edges[11].ports[1].pos = Coordinates(16, 7)

        edges[12].ports[0].pos = Coordinates(14, 11)
        edges[12].ports[1].pos = Coordinates(16, 10)

        edges[13].ports[0].pos = Coordinates(14, 12)
        edges[13].ports[1].pos = Coordinates(16, 13)

        t = turtle.Turtle()
        board = Board(t)
        rv = board.style_graph(nodes + edges)
        rv = board.draw_graph(nodes + edges, debug=True, delay=0)
        t.screen.mainloop()
        self.assertEqual(len(board.shapes), 3, board.shapes)
        self.assertEqual(len(board.stamps), len(nodes), board.stamps)
