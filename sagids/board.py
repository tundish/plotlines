#! /usr/bin/env python3
# encoding: UTF-8

# This file is part of SaGiDS.

# SaGiDS is free software: You can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# SaGiDS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the
# GNU General Public License along with SaGiDS.
# If not, see <https://www.gnu.org/licenses/>.

from collections import defaultdict
from collections import deque
from collections import UserDict
from collections.abc import Generator
import dataclasses
import datetime
import logging
import string
import typing
import uuid
import weakref

from sagids.coordinates import Coordinates


@dataclasses.dataclass(unsafe_hash=True)
class Item:
    store: typing.ClassVar[set] = defaultdict(weakref.WeakSet)

    number:     int = dataclasses.field(init=False)
    contents:   list = dataclasses.field(default_factory=list, compare=False, kw_only=True)

    def __post_init__(self, *args):
        self.number = max([j.number for i in self.__class__.store.values() for j in i], default=0) + 1
        self.__class__.store[self.__class__].add(self)


@dataclasses.dataclass(unsafe_hash=True)
class Link:
    pos:    Coordinates = None
    joins:  set[Item] = dataclasses.field(default_factory=weakref.WeakSet, compare=False, kw_only=True)


@dataclasses.dataclass(unsafe_hash=True)
class Pin(Item, Link):
    label:      str = ""
    shape:      str = ""


@dataclasses.dataclass(unsafe_hash=True)
class Port(Link):
    parent: Pin = None


@dataclasses.dataclass(unsafe_hash=True)
class Node(Pin):
    ports:  dict[int, Port] = dataclasses.field(default_factory=dict, compare=False)

    def __post_init__(self, *args):
        super().__post_init__(*args)
        if not self.pos:
            return
        self.pos = Coordinates(*self.pos)

    @property
    def neighbours(self):
        nodes = [edge.exit for edge in self.ports.values()] + [edge.into for edge in self.ports.values()]
        return [i for i in nodes if i is not self]

    @property
    def density(self):
        "Degree of node divided by number of neighbours"
        return []

    def connect(self, other, trail=None):
        port = len(self.ports)
        rv = Edge(exit=self, into=other, trail=trail)
        self.ports[port] = rv
        return rv


@dataclasses.dataclass(unsafe_hash=True)
class Edge(Item):
    pos_0: dataclasses.InitVar[Coordinates | None] = None
    pos_1: dataclasses.InitVar[Coordinates | None] = None
    trail: str = ""
    ports: list[Port] = dataclasses.field(default_factory=list, compare=False)

    def __post_init__(self, pos_0: tuple, pos_1: tuple, *args):
        super().__post_init__(*args)
        coords = [Coordinates(*c) for c in (pos_0, pos_1) if c is not None]
        if not coords:
            return
        self.ports = [
            Port(parent=self, pos=coords[0]),
            Port(parent=self, pos=coords[-1]),
        ]


class Board:

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
                edge = node.connect(Node())
                frame.append(edge.exit)
                yield edge.number, edge
        else:
            # Finish with start node
            start = Node(label="start")
            for node in frame:
                edge = start.connect(node)
                yield edge.number, edge


    @staticmethod
    def layout_graph(graph: dict) -> dict:
        return graph


    @staticmethod
    def toml_graph(graph: dict) -> Generator[str]:
        yield "[[nodes]]"
        yield "[[links]]"
