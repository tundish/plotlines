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


from decimal import Decimal
from fractions import Fraction
import tkinter as tk
import turtle
import unittest.mock

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.board import Port
from plotlines.coordinates import Coordinates


class SVGTests(unittest.TestCase):

    class FakeTurtle(turtle.RawTurtle):
        pass

    class FakeTurtleScreen(turtle.TurtleScreen):
        def _incrementudc(self):
            return

    def test_3_nodes(self):
        nodes = [Node((2, 2)), Node((7, 2)), Node((12, 2))]
        edges = [nodes[0].connect(nodes[1]), nodes[0].connect(nodes[2])]
        edges[0].ports[0].pos = Coordinates(3, 2)
        edges[0].ports[1].pos = Coordinates(6, 2)
        edges[1].ports[0].pos = Coordinates(8, 2)
        edges[1].ports[1].pos = Coordinates(11, 2)

        canvas = tk.Canvas()
        screen = self.FakeTurtleScreen(canvas)
        t = self.FakeTurtle(screen)
        board = Board(t)
        rv = board.style_graph(nodes + edges)
        rv = board.draw_graph(nodes + edges)
        print(vars(list(board.shapes.values())[0]))
        self.assertEqual(len(board.shapes), 1)
        self.assertEqual(len(board.stamps), len(nodes))
        self.fail(board.stamps)
