# -*- coding: utf-8 -*-
# <sure - sophisticated automated test library and runner>
# Copyright (C) <2010-2024>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import platform
from functools import cache


@cache
def has_ansi_support(os=os, sys=sys, platform=platform):
    if os.getenv("SURE_NO_COLORS"):
        return False

    for handle in [sys.stdout, sys.stderr]:
        if (hasattr(handle, "isatty") and handle.isatty()) or (
            "TERM" in os.environ and os.environ["TERM"] == "ANSI"
        ):
            if platform.system() != "Windows" and (
                "TERM" in os.environ and os.environ["TERM"] == "ANSI"
            ):
                return True

    return False


def white(msg):
    if not has_ansi_support():
        return msg
    return r"\033[1;37m{0}\033[0m".format(msg)


def yellow(msg):
    if not has_ansi_support():
        return msg
    return r"\033[1;33m{0}\033[0m".format(msg)


def red(msg):
    if not has_ansi_support():
        return msg
    return r"\033[1;31m{0}\033[0m".format(msg)


def green(msg):
    if not has_ansi_support():
        return msg
    return r"\033[1;32m{0}\033[0m".format(msg)
