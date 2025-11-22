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

import enum


class Direction(enum.IntEnum):
    GUIDE_TYPE_VERT = 100
    GUIDE_TYPE_HORI = 101


class Handle(enum.IntFlag):
    HAN_TOP    = 1
    HAN_BOT    = 2
    HAN_LEFT   = 4
    HAN_RIGHT  = 8
    HAN_HANDLE = 16
    HAN_CONNPT = 32
    HAN_CENDPT = 64
    HAN_SRC    = 128
    HAN_DST    = 256
    HAN_CENTER = 512
    HAN_POINT  = 1024
    HAN_SEPARA = 2048

#  libavoidPath
"""
pathStr += str.sprintf("%d ", (int) route.size());
    for (size_t i = 0; i < route.size(); ++i)
    {
        pathStr += str.sprintf("%g %g %d %d ", route.ps[i].x, route.ps[i].y,
                route.ps[i].id, route.ps[i].vn);
    }
"""
