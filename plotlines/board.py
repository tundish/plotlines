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

from collections import defaultdict
from collections import deque
from collections import UserDict
from collections.abc import Generator
import dataclasses
import datetime
from decimal import Decimal
from fractions import Fraction
import functools
import itertools
import logging
import math
from numbers import Number
import string
import textwrap
import tkinter as tk
import turtle
import typing
import uuid
import weakref

from plotlines.coordinates import Coordinates


RGB = functools.partial(Coordinates, coerce=int)


@dataclasses.dataclass(unsafe_hash=True)
class Style:
    stroke:     RGB = dataclasses.field(default=RGB(0, 0, 0), kw_only=True)
    fill:       RGB = dataclasses.field(default=RGB(255, 255, 255), kw_only=True)
    weight:     int = dataclasses.field(default=1, kw_only=True)


@dataclasses.dataclass(unsafe_hash=True)
class Item:
    store: typing.ClassVar[set] = defaultdict(weakref.WeakSet)

    number:     int = dataclasses.field(init=False)
    style:      Style = dataclasses.field(default_factory=Style, kw_only=True)
    contents:   list = dataclasses.field(default_factory=list, compare=False, kw_only=True)

    def __post_init__(self, *args):
        self.number = max([j.number for i in self.__class__.store.values() for j in i], default=0) + 1
        self.__class__.store[self.__class__].add(self)


@dataclasses.dataclass(unsafe_hash=True)
class Link:
    joins:  set[Item] = dataclasses.field(default_factory=weakref.WeakSet, compare=False, kw_only=True)


@dataclasses.dataclass(unsafe_hash=True)
class Pin(Item):
    pos:        Coordinates = None
    area:       int = dataclasses.field(default=4, kw_only=True)
    shape:      str = dataclasses.field(default="", kw_only=True)
    label:      str = dataclasses.field(default="", kw_only=True)


@dataclasses.dataclass(unsafe_hash=True)
class Port(Pin, Link):
    pass


@dataclasses.dataclass(unsafe_hash=True)
class Edge(Item):
    pos_0: dataclasses.InitVar[Coordinates | None] = None
    pos_1: dataclasses.InitVar[Coordinates | None] = None
    trail: str = ""
    ports: list[Port] = dataclasses.field(default_factory=list, compare=False)

    def __post_init__(self, pos_0: tuple, pos_1: tuple, *args):
        super().__post_init__(*args)
        coords = [Coordinates(*c) for c in (pos_0, pos_1) if c is not None]
        if coords:
            self.ports = [
                Port(joins={self}, pos=coords[0]),
                Port(joins={self}, pos=coords[-1]),
            ]
        else:
            self.ports = [Port(joins={self}), Port(joins={self})]


@dataclasses.dataclass(unsafe_hash=True)
class Node(Pin):
    ports:  dict[int, Port] = dataclasses.field(default_factory=dict, compare=False)

    def __post_init__(self, *args):
        super().__post_init__(*args)
        if not self.pos:
            return
        self.pos = Coordinates(*self.pos)

    @property
    def nearby(self):
        edges = [e for port in self.ports.values() for e in port.joins if isinstance(e, Edge)]
        return [n for edge in edges for p in edge.ports for n in p.joins if isinstance(n, Node) and n is not self]

    @property
    def density(self):
        "Degree of node divided by number of neighbours"
        return []

    @property
    def edges(self):
        return [i for p in self.ports.values() for i in p.joins if isinstance(i, Edge)]

    def connect(self, other: Pin, *pos, edge=None):
        rv = edge or Edge()
        rv.ports[0].joins.add(self)
        self.ports[len(self.ports)] = rv.ports[0]

        rv.ports[1].joins.add(other)
        other.ports[len(other.ports)] = rv.ports[1]

        try:
            rv.ports[0].pos = pos[0]
            rv.ports[1].pos = pos[-1]
        except IndexError:
            pass

        return rv

    @functools.singledispatchmethod
    def spacing(self, other: Node) -> dict[tuple[Pin, Pin], Number]:
        mine = {i: i.pos for i in self.ports.values()} | {self: self.pos}
        others = {i: i.pos for i in other.ports.values()} | {other: other.pos}
        rv = {(mk, ok): abs(ov - mv) for (mk, mv), (ok, ov) in itertools.product(mine.items(), others.items())}
        return rv

    @spacing.register
    def _(self, other: Edge) -> dict[tuple[Pin, Pin], Number]:
        mine = {i: i.pos for i in self.ports.values()} | {self: self.pos}
        others = {i: i.pos for i in other.ports}
        others.update({
            i: i.pos for i in (
                Pin(Coordinates.intercept(other.ports[0].pos, other.ports[1].pos, pos))
                for pos in mine.values()
            )
        })
        rv = {(mk, ok): abs(ov - mv) for (mk, mv), (ok, ov) in itertools.product(mine.items(), others.items())}
        return rv


class Board:

    def __init__(self, t = None):
        self.stamps = {}
        self.shapes = {}
        self.turtle = t or turtle.RawTurtle(None)

    @staticmethod
    def extent(items: list) -> tuple[Coordinates]:
        nodes = [i for i in items if isinstance(i, Node)]
        x_vals = sorted([p.pos[0] for node in nodes for p in [node] + list(node.ports.values()) if p.pos])
        y_vals = sorted([p.pos[1] for node in nodes for p in [node] + list(node.ports.values()) if p.pos])

        min_pos = Coordinates(x_vals[0], y_vals[0])
        max_pos = Coordinates(x_vals[-1], y_vals[-1])
        return min_pos, max_pos

    @staticmethod
    def frame(*points: tuple[Coordinates], margin: Decimal = Decimal("0.05"), square=False):
        x_vals = sorted([point[0] for point in points])
        y_vals = sorted([point[1] for point in points])

        span_x = x_vals[-1] - x_vals[0] or y_vals[-1] - y_vals[0]
        span_y = y_vals[-1] - y_vals[0] or x_vals[-1] - x_vals[0]

        min_x = x_vals[0] - margin * span_x
        max_x = x_vals[1] + margin * span_x
        min_y = y_vals[0] - margin * span_y
        max_y = y_vals[1] + margin * span_y

        if square:
            min_pos = Coordinates(min(min_x, min_y), min(min_x, min_y))
            max_pos = Coordinates(max(max_x, max_y), max(max_x, max_y))
        else:
            min_pos = Coordinates(min_x, min_y)
            max_pos = Coordinates(max_x, max_y)
        return (min_pos, max_pos)

    @staticmethod
    def scale_factor(geom: tuple[Number], frame: tuple[Coordinates, Coordinates], quant: str = ".01"):
        return Fraction(*min(
            Decimal(geom[0]) / (frame[1][0] - frame[0][0]),
            Decimal(geom[1]) / (frame[1][1] - frame[0][1])
        ).quantize(Decimal(quant)).as_integer_ratio())

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
                yield edge.number, edge
        else:
            # Finish with start node
            start = Node(label="start")
            for node in frame:
                edge = start.connect(node)
                yield edge.number, edge

    @staticmethod
    def layout_graph(t: RawTurtle, graph: dict, **kwargs) -> dict:
        return graph

    def style_graph(self, items: list, **kwargs) -> dict:
        screen = self.turtle.getscreen()
        screen.colormode(255)

        frame = Board.frame(*Board.extent(items), square=True)
        screen.setworldcoordinates(*[float(i) for c in frame for i in c])

        size = screen.screensize()
        scale = self.scale_factor(size, frame)

        for item in items:
            try:
                size = math.sqrt(item.area)
                item.shape = self.build_shape(size=size, scale=scale).key
            except AttributeError:
                pass
        return items

    def draw_graph(self, edges: list[Edges], debug=False, delay: int = 10) -> RawTurtle:
        screen = self.turtle.getscreen()
        screen.delay(delay)
        self.turtle.shape("blank")
        self.turtle.color((0, 0, 0), (255, 255, 255))
        nodes = set()
        for edge in [i for i in edges if isinstance(i, Edge)]:
            self.turtle.up()
            for port in edge.ports:
                for node in port.joins:
                    if node in nodes:
                        continue

                    try:
                        self.turtle.shape(node.shape)
                        self.turtle.setpos(node.pos)
                    except AttributeError:
                        pass
                    else:
                        self.stamps[self.turtle.stamp()] = node.shape
                        nodes.add(node)
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

    @staticmethod
    def toml_graph(graph: dict) -> Generator[str]:
        yield "[[nodes]]"
        yield "[[links]]"

    def build_shape(self, size, scale=1) -> turtle.Shape:
        key = f"sq{size:.02f}x{size:.02f}-{scale}"
        try:
            return self.shapes[key]
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
            self.shapes[key] = shape
            self.turtle.screen.register_shape(key, shape)
            return shape

    def to_svg(self):
        return textwrap.dedent(f"""
        <svg height="220" width="500" xmlns="http://www.w3.org/2000/svg">
        </svg>
        """)
