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

import importlib.resources
import pathlib
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.parent = pathlib.Path(tempfile.mkdtemp(prefix="plotlines-", suffix="-test"))

    def tearDown(self):
        shutil.rmtree(self.parent)
        self.assertFalse(self.parent.exists())

    def test_n03e02(self):
        text = importlib.resources.read_text("plotlines.test.data", "inkscape_properties_n03e02.svg")
        root = ET.fromstring(text)
        board = Board()
        rv = board.merge(root)
        self.assertEqual(len(rv), 5, text)
        self.assertEqual(len(board.items), 5)
        self.assertEqual(len(board.initial), 1)
        self.assertEqual(len(board.initial[0].nearby), 2)

        node = next(i for i in board.terminal if i.id == 825)
        self.assertEqual(node.name, "825")
        self.assertEqual(node.label, "Win")
        self.assertEqual(node.edges[0].label, "A arc")
        self.assertEqual(node.contents, ["Good ending.\n\n<NARRATOR>\tOr is it?"], rv)
        self.assertEqual(node.edges[0].contents, ["This is what happens if you go left."])
