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
"""tests for :class:`sure.AssertionBuilder` properties defined with the
decorator :func:`sure.assertionproperty`"""

from sure import expects
from sure.doubles import anything_of_type


def test_not_have():
    "expects().to.not_have"

    class WaveFunctionParameters:
        period = anything_of_type(float)
        amplitude = anything_of_type(float)
        frequency = anything_of_type(float)

    expects(WaveFunctionParameters).to.not_have.property("unrequested_phase_change")
    expects(WaveFunctionParameters).to.have.property("frequency").which.should.equal(anything_of_type(float))
