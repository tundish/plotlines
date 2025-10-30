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


import unittest

from plotlines.board import Edge
from plotlines.board import Node
from plotlines.motif import Motif


class MotifTests(unittest.TestCase):

    def test_one_ljoin(self):
        group = [Node()]
        items = Motif.ljoin(group)
        self.assertEqual(len(items), 5)

        nodes = [i for i in items if isinstance(i, Node)]
        self.assertEqual(len(nodes), 3)
        self.assertIn(group[0], nodes)
        self.assertEqual(len(group[0].connections[0]), 2)
        self.assertEqual(len(group[0].connections[1]), 0)

    def test_diamond(self):
        items = list(Motif.diamond())
