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

import argparse
import dataclasses
import datetime
import logging
import sys
from turtle import Turtle
from turtle import Shape
import typing
import uuid

try:
    from svg_turtle import SvgTurtle
except ImportError:
    SvgTurtle = Turtle


@dataclasses.dataclass
class Pin:
    total: typing.ClassVar[int] = 0

    label:      str = ""
    number:     int = dataclasses.field(init=False)
    contents:   list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.number = self.__class__.total + 1
        self.__class__.total = self.number


@dataclasses.dataclass
class Node(Pin):
    shape: str = ""


@dataclasses.dataclass
class Edge(Pin):
    exit: Node = None
    into: Node = None
    trail: str = ""


def setup_logger(level=logging.INFO):
    logging.basicConfig(level=level)
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.setFormatter(
            logging.Formatter(
                fmt="{asctime}|{levelname:>8}|{phase.name:^8}| {name:<16}| {path!s:<72}| {message}",
                datefmt=None, style='{',
                # defaults=dict(phase=Phase.CONFIG, path="")
            )
        )


class InlineValues:

    def __init__(self, _type=str):
        self.type = _type

    def __call__(self, text, sep=","):
        return [i.strip() for i in text.split(sep)]

def gen_graph(ending: list[str], loading: list[int], trails: int, **kwargs):
    print(f"{kwargs=}")
    a = Edge()
    yield a.number, a

def gen_exits(graph: dict):
    yield "[[nodes]]"
    yield "[[links]]"


def parser():
    rv = argparse.ArgumentParser(usage=__doc__, fromfile_prefix_chars="=")
    rv.add_argument("--debug", action="store_true", default=False, help="Display debug logs")
    rv.add_argument(
        "--ending", type=InlineValues(), default=["A"], help="Declare named endings"
    )
    rv.add_argument(
        "--loading", type=InlineValues(int), default=[10, 100],
        help="Define limits for the number of nodes of the story graph"
    )
    rv.add_argument(
        "--trails", type=InlineValues(str), default=None,
        help="Define the number of trails through the story graph"
    )
    rv.add_argument(
        "--format", choices=["plot", "svg", "text", "toml"], default="text",
        help="Specify format of output [text]"
    )
    """
    parser.add_argument(
        "--ending", type=int, default=3, help="Set the number of scenes [3]"
    )
    parser.add_argument(
        "--ending", type=int, default=3, help="Set the number of paths [1]"
    )
    """
    rv.convert_arg_line_to_args = lambda x: x.split()
    return rv


def main(args):
    level = logging.DEBUG if args.debug else logging.INFO
    # setup_logger(level=level)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("plotlines")

    args.trails = args.trails or len(args.ending)
    logger.info(f"Start")
    logger.info(f"{args=}")

    graph = dict(gen_graph(**vars(args)))
    print(f"{graph=}")

    for line in gen_exits(graph):
        print(line)

    t = SvgTurtle()
    print(f"{t.screen.getshapes()=}")
    t.screen.mainloop()
    t.save_as("plotlines.svg")
    return 0


def run():
    ts = datetime.datetime.now(tz=datetime.timezone.utc)
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()
