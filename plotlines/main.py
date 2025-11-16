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

import argparse
import datetime
import logging
import pprint
import string
import sys
import tkinter as tk
import tkinter.font
import tomllib
import turtle

from plotlines.board import Board
from plotlines.plotter import Plotter


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


def main(args):
    level = logging.DEBUG if args.debug else logging.INFO
    # setup_logger(level=level)
    logging.basicConfig(level=level)
    logger = logging.getLogger("plotlines")

    logger.debug(f"{args=}")
    logger.info(f"Format option: {args.format.upper()}")

    if args.read:
        text = stdin.read()
        data = tomllib.loads(text)
        pprint.pprint(data)
        return 0
    else:
        items = []
        steps = args.limit // 10
        try:
            items = list(Plotter.build_graph(steps=steps, **vars(args)))
        except KeyboardInterrupt:
            pass

    board = Board(items=items)
    if args.format == "plot":
        plotter = Plotter(board, t=turtle.Turtle())
        size = plotter.turtle.screen.screensize()
        items = plotter.layout_board(size)
        frame, scale = plotter.style_items(board.items, size=size)

        logger.debug(tk.font.families())
        items = plotter.draw_items(items, debug=args.debug, delay=0)
        plotter.turtle.screen.mainloop()
    elif args.format == "svg":
        # TODO: implement Renderer
        # text = sys.stdin.read()
        # data = tomllib.loads(text)
        logger.warning("SVG output not yet implemented")
    elif args.format == "text":
        pprint.pprint(board, depth=3)
    elif args.format == "toml":
        print(*board.toml(), sep="\n", file=sys.stdout)

    return 0


class InlineValues:

    def __init__(self, type_=str):
        self.type = type_

    def __call__(self, text, sep=","):
        return [self.type(i.strip()) for i in text.split(sep)]


def parser():
    rv = argparse.ArgumentParser(usage=__doc__, fromfile_prefix_chars="=")
    rv.add_argument("--debug", action="store_true", default=False, help="Display debug information")
    rv.add_argument("--read", action="store_true", default=False, help="Read a TOML graph from stdin [False]")
    rv.add_argument("--ending", type=int, default=4, help="Set the number of endings [4].")
    rv.add_argument(
        "--limit", type=int, default=100,
        help="Limit the number of Nodes and Edges in the graph [100]"
    )
    rv.add_argument(
        "--exits", type=int, default=4,
        help="Fix the number of exiting Edges from each Node [4]"
    )
    rv.add_argument(
        "--format", choices=["plot", "svg", "text", "toml"], default="toml",
        help="Specify format of output [text]"
    )
    rv.convert_arg_line_to_args = lambda x: x.split()
    return rv


def run():
    ts = datetime.datetime.now(tz=datetime.timezone.utc)
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()
