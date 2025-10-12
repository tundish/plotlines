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
import importlib.resources
import logging
import math
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
    def build_graph(ending: list[str], loading: list[int], trails: int, **kwargs) -> Generator[Node | Edge]:
        nodes = [Node(), Node(), Node(), Node(), Node()]
        edges = [
            nodes[0].connect(nodes[1]),
            nodes[1].connect(nodes[2]),
            nodes[1].connect(nodes[3]),
            nodes[2].connect(nodes[4]),
            nodes[3].connect(nodes[4]),
        ]
        yield from  nodes + edges
        return

        frame = deque([Node(label=name) for name in ending])

        tally = Counter()
        while tally[Node] + tally[Edge] < max(loading):
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
    def priority(lhs: set, rhs: set, items: list, boundary: tuple, visited=None):
        # Calculate placement column pitch
        print(f"{boundary=}")
        visited = set() if visited is None else visited
        work = next(reversed(sorted((len(i), i) for i in (lhs, rhs))))[1]
        for item in work:
            area = item.area + sum(p.area for p in item.ports.values())
            lhs_edges = {edge: math.sqrt(edge.ports[1].area) for edge in item.edges if item.uid in edge.ports[1].joins}
            rhs_edges = {edge: math.sqrt(edge.ports[0].area) for edge in item.edges if item.uid in edge.ports[0].joins}
            print(f"{lhs_edges=}")
            if item not in visited:
                yield item
            visited.add(item)

        if work is lhs:
            pass
        else:
            pass

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
                size = math.sqrt(item.area)
                item.shape = self.build_shape(size=size, scale=scale).key
            except AttributeError:
                assert isinstance(item, Edge)
        return size, frame, scale

    def layout_graph(self, size, frame, scale, **kwargs) -> dict:
        print(f"{size=}", f"{frame=}", f"{scale=}")
        initial = set(self.board.initial)
        terminal = set(self.board.terminal)

        boundary = [frame[0], C(frame[1][0], frame[0][1]), C(frame[0][0], frame[1][1]), frame[1]]
        for n, node in enumerate(self.priority(initial, terminal, self.board.items, boundary=boundary)):
            print(n, f"{node.area=}")

        for item in self.board.items:
            try:
                item.pos = item.pos or frame[0]
                if item in initial:
                    item.pos = frame[0]

                elif item in terminal:
                    item.pos = frame[1]

            except AttributeError:
                assert isinstance(item, Edge)
        # Allocate pos to each node

        # Allocate pos to each port
        # Allocate label to each node and edge
        return self.board.items

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
            self.turtle.write(self.turtle.pos())
            self.turtle.down()
            self.turtle.setpos(edge.ports[1].pos)
            self.turtle.write(self.turtle.pos())
        return items
