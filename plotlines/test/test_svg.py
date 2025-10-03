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
import functools
import itertools
import tkinter as tk
import turtle
from types import SimpleNamespace as NS
import unittest.mock
import xml.etree.ElementTree as ET

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.board import Port
from plotlines.coordinates import Coordinates


class SVGTests(unittest.TestCase):

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
        nodes = [Node((2, 2)), Node((7, 2)), Node((12, 2))]
        edges = [nodes[0].connect(nodes[1]), nodes[0].connect(nodes[2])]
        edges[0].ports[0].pos = Coordinates(3, 2)
        edges[0].ports[1].pos = Coordinates(6, 2)
        edges[1].ports[0].pos = Coordinates(8, 2)
        edges[1].ports[1].pos = Coordinates(11, 2)

        mock_screen = self.build_screen()
        with unittest.mock.patch.object(turtle.Turtle, "_screen", mock_screen):
            t = turtle.Turtle()
            board = Board(t)
            rv = board.style_graph(nodes + edges)
            rv = board.draw_graph(nodes + edges)
            self.assertEqual(len(board.shapes), 1, board.shapes)
            self.assertEqual(len(board.stamps), len(nodes), board.stamps)

    def test_3_nodes_svg(self):
        nodes = [Node((2, 2)), Node((7, 2)), Node((12, 2))]
        edges = [nodes[0].connect(nodes[1]), nodes[0].connect(nodes[2])]
        edges[0].ports[0].pos = Coordinates(3, 2)
        edges[0].ports[1].pos = Coordinates(6, 2)
        edges[1].ports[0].pos = Coordinates(8, 2)
        edges[1].ports[1].pos = Coordinates(11, 2)

        mock_screen = self.build_screen()
        with unittest.mock.patch.object(turtle.Turtle, "_screen", mock_screen):
            t = turtle.Turtle()
            board = Board(t)
            rv = board.style_graph(nodes + edges)
            rv = board.draw_graph(nodes + edges)

            frame = board.frame(*board.extent(nodes + edges), square=True)
            print(f"{frame=}")
            size = t.screen.screensize()
            print(f"{size=}")

            svg = board.to_svg()
            root = ET.fromstring(svg)

            ns = NS(svg="http://www.w3.org/2000/svg")
            self.assertEqual(root.tag, ET.QName(ns.svg, "svg"))
            self.assertEqual(root.attrib.get("width"), str(t.screen.screensize()[0]), root.attrib)
            self.assertEqual(root.attrib.get("height"), str(t.screen.screensize()[1]), root.attrib)
            self.assertIn("viewBox", root.attrib)
