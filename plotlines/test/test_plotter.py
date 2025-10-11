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
import itertools
import textwrap
import tkinter as tk
import tomllib
import turtle
import unittest

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.board import Port
from plotlines.coordinates import Coordinates as C
from plotlines.plotter import Plotter
from plotlines.test.test_board import BoardTests


class PlotterTests(unittest.TestCase):

    @staticmethod
    def build_screen(size: tuple = (400, 300)):
        mock_image = unittest.mock.Mock(spec=tk.PhotoImage)
        mock_image._type = "image"
        mock_image._data = None

        rv = unittest.mock.MagicMock(spec=turtle.TurtleScreen)
        rv._tracing = 0
        rv._turtles = []
        rv._blankimage.return_value = mock_image
        rv._shapes = dict(blank=mock_image, classic=mock_image)
        rv._write.return_value = (None, None)

        rv.register_shape.side_effect = lambda name, shape: rv._shapes.setdefault(name, shape)
        rv.getshapes.side_effect = lambda: list(rv._shapes)
        rv._createpoly.side_effect = itertools.count()
        rv.xscale = 1.0
        rv.yscale = 1.0
        rv.mode.return_value = "world"
        rv.screensize.return_value = size
        return rv

    def test_3_nodes_draw(self):
        nodes, edges = BoardTests.build_3_nodes()
        mock_screen = self.build_screen()
        with unittest.mock.patch.object(turtle.Turtle, "_screen", mock_screen):
            board = Board()
            t = turtle.Turtle()
            plotter = Plotter(board, t)
            rv = plotter.style_graph(nodes + edges)
            rv = plotter.draw_graph(nodes + edges)
            self.assertEqual(len(board.shapes), 1, board.shapes)
            self.assertEqual(len(board.stamps), len(nodes), board.stamps)

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
            nodes[0].connect(nodes[3], C(2, 8), C(5, 9)),
            nodes[3].connect(nodes[2], C(6, 5), C(6, 4)),
            nodes[2].connect(nodes[1], C(6, 8), C(6, 7)),
            nodes[3].connect(nodes[4], C(6, 10), C(6, 11)),
            nodes[1].connect(nodes[5], C(7, 3), C(9, 3)),
            nodes[2].connect(nodes[5], C(7, 6), C(9, 5)),
            nodes[3].connect(nodes[6], C(7, 9), C(9, 8)),
            nodes[4].connect(nodes[7], C(7, 12), C(11, 12)),
            nodes[5].connect(nodes[8], C(13, 3), C(16, 1)),
            nodes[5].connect(nodes[9], C(13, 4), C(16, 4)),
            nodes[5].connect(nodes[10], C(13, 5), C(16, 7)),
            nodes[6].connect(nodes[10], C(11, 8), C(16, 7)),
            nodes[7].connect(nodes[11], C(14, 11), C(16, 10)),
            nodes[7].connect(nodes[12], C(14, 12), C(16, 13)),
        ]

        t = turtle.Turtle()
        board = Board(t, title="Multigraph")
        rv = Plotter.style_graph(nodes + edges)
        rv = Plotter.draw_graph(nodes + edges, debug=True, delay=0)
        t.screen.mainloop()
        self.assertEqual(len(board.shapes), 3, board.shapes)
        self.assertEqual(len(board.stamps), len(nodes), board.stamps)
