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

    def test_one_lfork(self):
        group = [Node()]
        group.extend(Motif.fork(group, fwd=False))
        self.assertEqual(len(group), 5)

        nodes = [i for i in group if isinstance(i, Node)]
        self.assertEqual(len(nodes), 3)
        self.assertIn(group[0], nodes)
        self.assertEqual(len(group[0].connections[0]), 2)
        self.assertEqual(len(group[0].connections[1]), 0)

    def test_one_rfork(self):
        group = [Node()]
        group.extend(Motif.fork(group, fwd=True))
        self.assertEqual(len(group), 5)

        nodes = [i for i in group if isinstance(i, Node)]
        self.assertEqual(len(nodes), 3)
        self.assertIn(group[0], nodes)
        self.assertEqual(len(group[0].connections[0]), 0)
        self.assertEqual(len(group[0].connections[1]), 2)

    def test_limit_lfork(self):
        group = [Node(), Node()]
        items = list(Motif.fork(group, limit=1, fwd=False))
        self.assertEqual(len(items), 4)

        nodes = [i for i in items if isinstance(i, Node)]
        self.assertEqual(len(nodes), 2)
        self.assertIn(nodes[0].nearby[0], group)
        self.assertIn(nodes[1].nearby[0], group)
        self.assertEqual(nodes[0].nearby[0], nodes[1].nearby[0])

    def test_stem(self):
        group = [Node()]
        group.extend(Motif.fork(group, fwd=False))
        self.assertEqual(len(group), 5)

        nodes = [i for i in group if isinstance(i, Node)]
        self.assertEqual(len(nodes), 3)
        self.assertIn(group[0], nodes)
        self.assertEqual(len(group[0].connections[0]), 2)
        self.assertEqual(len(group[0].connections[1]), 0)
