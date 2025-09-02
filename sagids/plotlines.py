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
import datetime
import logging
import sys


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


def gen_exits():
    yield "[[exits]]"


def main(args):
    level = logging.DEBUG if args.debug else logging.INFO
    # setup_logger(level=level)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("plotlines")

    logger.info(f"Start")
    for line in gen_exits():
        print(line)
    return 0


def run():
    ts = datetime.datetime.now(tz=datetime.timezone.utc)
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("--debug", action="store_true", default=False, help="Display debug logs")
    parser.add_argument(
        "--ending", action="append", help="Declare a named ending"
    )
    """
    parser.add_argument(
        "--ending", type=int, default=3, help="Set the number of scenes [3]"
    )
    parser.add_argument(
        "--ending", type=int, default=3, help="Set the number of paths [1]"
    )
    """
    args = parser.parse_args()
    rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()
