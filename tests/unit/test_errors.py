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

from mock import patch
from sure import expects
from sure.doubles import stub
from sure.runtime import ScenarioResult, Scenario, RuntimeContext
from sure.errors import (
    CallerLocation,
    xor,
    exit_code,
    BaseSureError,
    ImmediateExit,
    RuntimeInterruption,
)
from sure.loader import collapse_path


def test_xor():
    "sure.errors.xor should perform an XOR operation"
    expects(xor(0b10010, 0b10110)).to.equal(0b100)


def test_exit_code():
    "sure.errors.exit_code should return a number deterministically derived from a string"

    expects(exit_code("ERO")).to.equal(88)
    expects(exit_code("USE")).to.equal(67)
    expects(exit_code("OCDE")).to.equal(13)


def test_base_sure_error():
    "sure.errors.BaseSureError should implement __str__ and __repr__"

    msg = BaseSureError("Monosodium Glutamate")
    expects(repr(msg)).to.equal("Monosodium Glutamate")
    expects(str(msg)).to.equal("Monosodium Glutamate")


@patch("sure.errors.sys")
def test_immediate_exit(sys):
    "sure.errors.ImmediateExit should call :func:`sys.exit`"

    ie = ImmediateExit(1)

    expects(str(ie)).to.equal("ImmediateExit")
    expects(repr(ie)).to.equal("ImmediateExit")
    sys.exit.assert_called_once_with(1)


def test_caller_location_most_recent_path_and_lineno():
    "sure.errors.Callerlocation.most_recent().path_and_lineno should point to the path and line number"

    caller_location = CallerLocation.most_recent()
    expects(caller_location.path_and_lineno).to.equal(f"{collapse_path(__file__)}:69")


def test_runtime_interruption():
    "sure.errors.RuntimeInterruption should contain metadata about the given :class:`sure.runtime.ScenarioResult`"

    context = stub(RuntimeContext)
    scenario = stub(Scenario)
    scenario_result = stub(
        ScenarioResult,
        context=context,
        scenario=scenario,
        location=CallerLocation.most_recent(),
        __error__=None,
        __failure__=None,
    )

    ri = RuntimeInterruption(scenario_result)

    expects(ri).to.have.property('result').being.equal(scenario_result)
    expects(ri).to.have.property('context').being.equal(context)
    expects(ri).to.have.property('scenario').being.equal(scenario)
