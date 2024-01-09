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
from sure import expects
from sure import terminal
from mock import patch


description = "tests for :class:`sure.terminal`"


@patch('sure.terminal.os')
def test_has_ansi_support_disabled_env_var_set(os):
    "sure.terminal.has_ansi_support() returns False when environment variable SURE_NO_COLORS is set"

    os.getenv.return_value = 'true'

    expects(terminal.has_ansi_support(os=os)).to.equal(False)


@patch('sure.terminal.platform')
@patch('sure.terminal.sys')
@patch('sure.terminal.os')
def test_has_ansi_support_enabled(os, sys, platform):
    "sure.terminal.has_ansi_support() returns True"

    platform.system.return_value = "Unix"
    sys.stdout.isatty.return_value = True
    sys.stderr.isatty.return_value = True
    os.getenv.return_value = False
    os.environ = {
        'TERM': 'ANSI'
    }

    expects(terminal.has_ansi_support(os, sys, platform)).to.equal(True)


@patch('sure.terminal.platform')
@patch('sure.terminal.sys')
@patch('sure.terminal.os')
def test_has_ansi_support_disabled_for_windows(os, sys, platform):
    "sure.terminal.has_ansi_support() returns False when on Windows™ platform"

    platform.system.return_value = "Windows"
    sys.stdout.isatty.return_value = True
    sys.stderr.isatty.return_value = True
    os.getenv.return_value = False
    os.environ = {
        'TERM': 'ANSI'
    }

    expects(terminal.has_ansi_support(os, sys, platform)).to.equal(False)


@patch('sure.terminal.platform')
@patch('sure.terminal.sys')
@patch('sure.terminal.os')
def test_has_ansi_support_disabled_with_term_env_var_non_ansi(os, sys, platform):
    "sure.terminal.has_ansi_support() returns True"

    platform.system.return_value = "Unix"
    sys.stdout.isatty.return_value = True
    sys.stderr.isatty.return_value = True
    os.getenv.return_value = False
    os.environ = {
        'TERM': ''
    }

    expects(terminal.has_ansi_support(os, sys, platform)).to.equal(False)


@patch('sure.terminal.has_ansi_support')
def test_red_with_ansi_support(has_ansi_support):
    "sure.terminal.red() with ANSI support"

    has_ansi_support.return_value = True

    expects(terminal.red("blue")).to.equal(r"\033[1;31mblue\033[0m")


@patch('sure.terminal.has_ansi_support')
def test_red_without_ansi_support(has_ansi_support):
    "sure.terminal.red() without ANSI support"

    has_ansi_support.return_value = False

    expects(terminal.red("blue")).to.equal(r"blue")


@patch('sure.terminal.has_ansi_support')
def test_white_with_ansi_support(has_ansi_support):
    "sure.terminal.white() with ANSI support"

    has_ansi_support.return_value = True

    expects(terminal.white("green")).to.equal(r"\033[1;37mgreen\033[0m")


@patch('sure.terminal.has_ansi_support')
def test_white_without_ansi_support(has_ansi_support):
    "sure.terminal.white() without ANSI support"

    has_ansi_support.return_value = False

    expects(terminal.white("green")).to.equal(r"green")


@patch('sure.terminal.has_ansi_support')
def test_yellow_with_ansi_support(has_ansi_support):
    "sure.terminal.yellow() with ANSI support"

    has_ansi_support.return_value = True

    expects(terminal.yellow("blue")).to.equal(r"\033[1;33mblue\033[0m")


@patch('sure.terminal.has_ansi_support')
def test_yellow_without_ansi_support(has_ansi_support):
    "sure.terminal.yellow() without ANSI support"

    has_ansi_support.return_value = False

    expects(terminal.yellow("blue")).to.equal(r"blue")


@patch('sure.terminal.has_ansi_support')
def test_green_with_ansi_support(has_ansi_support):
    "sure.terminal.green() with ANSI support"

    has_ansi_support.return_value = True

    expects(terminal.green("blue")).to.equal(r"\033[1;32mblue\033[0m")


@patch('sure.terminal.has_ansi_support')
def test_green_without_ansi_support(has_ansi_support):
    "sure.terminal.green() without ANSI support"

    has_ansi_support.return_value = False

    expects(terminal.green("blue")).to.equal(r"blue")
