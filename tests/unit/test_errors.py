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
"unit tests for :mod:`sure.errors`"

from sure import expects
from sure.errors import CallerLocation
from sure.loader import collapse_path


def test_caller_location_most_recent_path_and_lineno():
    "sure.errors.Callerlocation.most_recent().path_and_lineno should point to the path and line number"

    caller_location = CallerLocation.most_recent()
    expects(caller_location.path_and_lineno).to.equal(f"{collapse_path(__file__)}:27")
