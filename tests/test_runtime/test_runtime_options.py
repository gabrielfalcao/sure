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
from sure.runtime import RuntimeOptions


description = "tests for :class:`sure.runtime.RuntimeOptions`"


def test_runtime_options():
    """sure.runtime.RuntimeOptions"""

    expects(RuntimeOptions(0).immediate).to.be.false
    expects(RuntimeOptions(1).immediate).to.be.true
    expects(repr(RuntimeOptions(1))).to.equal(
        "<RuntimeOptions immediate=True glob_pattern='**test*.py' reap_warnings=False>"
    )
    expects(repr(RuntimeOptions(0))).to.equal(
        "<RuntimeOptions immediate=False glob_pattern='**test*.py' reap_warnings=False>"
    )
