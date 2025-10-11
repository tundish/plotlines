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
    def build_graph(ending: list[str], loading: list[int], trails: int, **kwargs) -> Generator[int, Edge]:
        frame = deque([Node(label=name) for name in ending])

        while len(Pin.store[Node]) + len(Pin.store[Edge]) < max(loading):
            # Connect each node to one or more trail edges
            try:
                node = frame.popleft()
            except IndexError:
                break
            else:
                frame.append(Node())
                edge = node.connect(frame[-1])
                yield edge.uid, edge
        else:
            # Finish with start node
            start = Node(label="start")
            for node in frame:
                edge = start.connect(node)
                yield edge.uid, edge

    @staticmethod
    def layout_graph(t: RawTurtle, graph: dict, **kwargs) -> dict:
        return graph

    def style_graph(self, items: list, **kwargs) -> dict:
        screen = self.turtle.getscreen()
        screen.colormode(255)

        frame = self.board.frame(*self.board.extent(items), square=True)
        screen.setworldcoordinates(*[float(i) for c in frame for i in c])

        size = screen.screensize()
        scale = self.board.scale_factor(size, frame)

        for item in items:
            try:
                size = math.sqrt(item.area)
                item.shape = self.build_shape(size=size, scale=scale).key
            except AttributeError:
                assert isinstance(item, Edge)
        return items

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
