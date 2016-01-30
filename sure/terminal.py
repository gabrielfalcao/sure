# -*- coding: utf-8 -*-

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
