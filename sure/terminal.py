#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2013>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from __future__ import unicode_literals

import os
import sys
import platform

SUPPORTS_ANSI = False
for handle in [sys.stdout, sys.stderr]:
    if (hasattr(handle, "isatty") and handle.isatty()) or \
        ('TERM' in os.environ and os.environ['TERM'] == 'ANSI'):
        if platform.system() == 'Windows' and not (
            'TERM' in os.environ and os.environ['TERM'] == 'ANSI'):
            SUPPORTS_ANSI = False
        else:
            SUPPORTS_ANSI = True

if os.getenv('SURE_NO_COLORS'):
    SUPPORTS_ANSI = False

SUPPORTS_ANSI = False


def red(string):
    if not SUPPORTS_ANSI:
        return string
    return r"\033[1;31m{0}\033[0m".format(string)


def green(string):
    if not SUPPORTS_ANSI:
        return string
    return r"\033[1;32m{0}\033[0m".format(string)


def yellow(string):
    if not SUPPORTS_ANSI:
        return string
    return r"\033[1;33m{0}\033[0m".format(string)


def white(string):
    if not SUPPORTS_ANSI:
        return string
    return r"\033[1;37m{0}\033[0m".format(string)
