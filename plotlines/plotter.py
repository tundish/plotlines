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

from __future__ import annotations  # Until Python 3.14 is everywhere

from collections import Counter
from collections import deque
from decimal import Decimal
import importlib.resources
import itertools
import logging
import math
import operator
import tkinter as tk
import turtle

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.board import Pin
from plotlines.coordinates import Coordinates as C


class Plotter:

    def __init__(self, b: Board, t = None):
        self.board = b
        self.turtle = t or turtle.RawTurtle(None)
        self.stamps = dict()
        try:
            self.words = self.build_words()
        except Exception:
            self.words = dict()

    def build_shape(self, size, scale=1) -> turtle.Shape:
        key = f"sq{size:.02f}x{size:.02f}-{scale}"
        try:
            return self.board.shapes[key]
        except KeyError:
            unit = scale * size / 2
            shape = turtle.Shape(
                "polygon", (
                    (-unit, -unit),
                    (unit, -unit),
                    (unit, unit),
                    (-unit, unit))
            )
            shape.key = key
            self.board.shapes[key] = shape
            self.turtle.screen.register_shape(key, shape)
            return shape

    @staticmethod
    def build_words() -> dict[int, list[str]]:
        text = importlib.resources.read_text("plotlines", "assets/words.txt")
        words = text.splitlines()
        return words

    @staticmethod
    def build_graph(ending: list[str], trails: int, **kwargs) -> Generator[Node | Edge]:
        frame = deque([Node(label=name) for name in ending])

        tally = Counter()
        stack = 12
        while tally[Node] + tally[Edge] < stack:
            # Connect each node to one or more trail edges
            try:
                node = frame.popleft()
                yield node
            except IndexError:
                break
            else:
                node = Node()
                tally[Node] += 1
                frame.append(node)
                edge = node.connect(frame[-1])
                tally[Edge] += 1
                yield edge
        else:
            # Finish with start node
            start = Node(label="start")
            for node in frame:
                edge = start.connect(node)
                tally[Edge] += 1
                yield edge

    @staticmethod
    def node_size(node: Node):
        connections = node.connections
        lhs_sizes = {edge: math.sqrt(edge.ports[1].area) for edge in connections[0]}
        rhs_sizes = {edge: math.sqrt(edge.ports[0].area) for edge in connections[1]}
        height = max(sum(lhs_sizes.values()), sum(rhs_sizes.values()), math.sqrt(node.area))
        return height

    @staticmethod
    def expandex(length: int):
        "Generate indexes from the middle outwards"
        mid = length // 2
        up = range(mid, length)
        dn = range(mid - 1, -1, -1)
        for i, j in itertools.zip_longest(up, dn):
            for x in (i, j):
                if x is not None:
                    yield x

    @staticmethod
    def place(items: list = None, boundary: tuple = None, visited=None):
        visited = set() if visited is None else visited
        work = list()
        sizes = {item: Plotter.node_size(item) for item in items if isinstance(item, Node)}
        zones = dict(
            [
                (key, list(group))
                for key, group in itertools.groupby(
                    sorted((item for item in items if isinstance(item, Node)), key=operator.attrgetter("zone")),
                    key=operator.attrgetter("zone")
                )
            ]
        )

        offset_x = 0
        width_x = 0
        for zone, nodes in zones.items():
            space_y = ((boundary[2] - boundary[0])[1] - sum(sizes[i] for i in nodes)) / (2 * len(nodes) + 1)
            for n, node in enumerate(nodes):
                lhs_edges = {edge: math.sqrt(edge.ports[1].area) for edge in node.edges if node.uid in edge.ports[1].joins}
                rhs_edges = {edge: math.sqrt(edge.ports[0].area) for edge in node.edges if node.uid in edge.ports[0].joins}
                node.height = max(sum(lhs_edges.values()), sum(rhs_edges.values()))
                node.width = max(node.height, math.sqrt(node.area))
                width_x = max(width_x, node.width)

                # Allocate coordinates from lhs of boundary
                node.pos = C(
                    boundary[0][0] + offset_x + node.width / 2,
                    boundary[0][1] + n * space_y + node.height / 2,
                )

                visited.add(node)
                visited.add(node.pos)

                for n, (edge, size) in enumerate(lhs_edges.items()):
                    if n == 0:
                        pos = node.pos - C(node.width / 2, size / 2 + sum(lhs_edges.values()) / 2)
                    pos += C(0, size)
                    edge.ports[1].pos = pos
                for n, (edge, size) in enumerate(rhs_edges.items()):
                    if n == 0:
                        pos = node.pos - C(node.width / -2, size / 2 + sum(rhs_edges.values()) / 2)
                    pos += C(0, size)
                    edge.ports[0].pos = pos
            yield zone, nodes

            edge_length = 2 * width_x
            offset_x += width_x + edge_length
            width_x = 0

    def layout_graph(self, size, **kwargs) -> dict:
        nodes = set(i for i in self.board.items if isinstance(i, Node))
        placed = set()

        boundary = [C(0, 0), C(0, size[0]), C(size[1], 0), C(*size)]
        zones = dict(self.place(self.board.items, boundary=boundary))

        crowding = {
            z: min([
                val
                for node in zone
                for other in zone
                for item in other.nearby + other.edges
                for val in node.spacing(item).values()
                if val != 0
            ])
            for z, zone in zones.items()
        }
        crowded = {v: k for k, v in crowding.items()}.get(min(crowding.values()))
        zone = zones[crowded]
        for n, index in enumerate(self.expandex(len(zone))):
            node = zone[index]
            if n % 2 == 0:
                hop = node.height
            else:
                hop = -node.height
            zone[index].translate(C(0, hop))

        return self.board.items

    def style_graph(self, items: list, **kwargs) -> dict:
        screen = self.turtle.getscreen()
        screen.colormode(255)

        frame = self.board.frame(*self.board.extent(items), square=True)
        try:
            screen.setworldcoordinates(*[float(i) for c in frame for i in c])
        except ZeroDivisionError:
            frame = [C(0, 0), C(120, 120)]
            screen.setworldcoordinates(*[float(i) for c in frame for i in c])

        size = screen.screensize()
        scale = self.board.scale_factor(size, frame)

        for item in items:
            try:
                size = max(getattr(item, "width", 0), getattr(item, "height", 0)) or math.sqrt(item.area)
                item.shape = self.build_shape(size=size, scale=scale).key
            except AttributeError:
                assert isinstance(item, Edge)
        return frame, scale

    def draw_graph(self, items: list[Edge], debug=False, delay: int = 10) -> RawTurtle:
        screen = self.turtle.getscreen()
        try:
            screen.title(self.board.title)
            screen.delay(delay)
        except AttributeError:
            # Test fixture
            pass

        self.turtle.shape("blank")
        self.turtle.color((0, 0, 0), (255, 255, 255))
        nodes = set()
        for edge in [i for i in items if isinstance(i, Edge)]:
            self.turtle.up()
            for port in edge.ports:
                for node_uid in port.joins:
                    if node_uid in nodes:
                        continue

                    try:
                        node = edge.store[node_uid]
                        self.turtle.shape(node.shape)
                        self.turtle.setpos(node.pos)
                    except AttributeError:
                        pass
                    except KeyError as error:
                        raise
                    else:
                        self.stamps[self.turtle.stamp()] = node.shape
                        nodes.add(node_uid)
                        if debug:
                            self.turtle.write(self.turtle.pos())
                    finally:
                        self.turtle.shape("blank")

            if not all(i.pos for i in edge.ports):
                continue

            self.turtle.setpos(edge.ports[0].pos)
            if debug:
                self.turtle.write(self.turtle.pos())
            self.turtle.down()
            self.turtle.setpos(edge.ports[1].pos)
            if debug:
                self.turtle.write(self.turtle.pos())
        return items
