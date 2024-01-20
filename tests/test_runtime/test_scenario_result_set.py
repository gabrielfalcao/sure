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
"""tests for :class:`sure.runtime.ScenarioResultSet`"""

import sys
from sure import expects
from sure.doubles import stub
from sure.loader import collapse_path
from sure.runtime import (
    ErrorStack,
    RuntimeContext,
    Scenario,
    ScenarioResult,
    ScenarioResultSet,
    TestLocation,
)

description = "tests for :class:`sure.runtime.ScenarioResultSet`"


def test_scenario_result_set():
    "ScenarioResultSet discerns types of :class:`sure.runtime.ScenarioResult` instances"

    scenario_results = [
        stub(ScenarioResult, __error__=None, __failure__=None),
        stub(ScenarioResult, __error__=None, __failure__=AssertionError('y')),
        stub(ScenarioResult, __error__=InterruptedError('x'), __failure__=None),
        stub(ScenarioResult, __error__=None, __failure__=AssertionError('Y')),
        stub(ScenarioResult, __error__=InterruptedError('X'), __failure__=None),
        stub(ScenarioResult, __error__=None, __failure__=None),
    ]

    scenario_result_set = ScenarioResultSet(scenario_results, context=stub(RuntimeContext))

    expects(scenario_result_set).to.have.property('failed_scenarios').being.length_of(2)
    expects(scenario_result_set).to.have.property('errored_scenarios').being.length_of(2)
    expects(scenario_result_set).to.have.property('scenario_results').being.length_of(6)


def test_scenario_result_set_printable_error():
    "ScenarioResultSet.printable presents reference to first error occurrence"

    scenario_results = [
        stub(ScenarioResult, __error__=None, __failure__=None),
        stub(ScenarioResult, __error__=InterruptedError('x'), __failure__=None),
        stub(ScenarioResult, __error__=InterruptedError('X'), __failure__=None),
        stub(ScenarioResult, __error__=None, __failure__=None),
    ]

    scenario_result_set = ScenarioResultSet(scenario_results, context=stub(RuntimeContext))

    expects(scenario_result_set.printable()).to.equal("InterruptedError: x")


def test_scenario_result_set_printable_failure():
    "ScenarioResultSet.printable presents reference to first failure occurrence"

    scenario_results = [
        stub(ScenarioResult, __error__=None, __failure__=None),
        stub(ScenarioResult, __error__=None, __failure__=AssertionError('Y')),
        stub(ScenarioResult, __error__=InterruptedError('x'), __failure__=None),
        stub(ScenarioResult, __error__=None, __failure__=AssertionError('y')),
        stub(ScenarioResult, __error__=InterruptedError('X'), __failure__=None),
        stub(ScenarioResult, __error__=None, __failure__=None),
    ]

    scenario_result_set = ScenarioResultSet(scenario_results, context=stub(RuntimeContext))

    expects(scenario_result_set.printable()).to.equal("AssertionError: Y")


def test_scenario_result_set_printable_no_errors_or_failures():
    "ScenarioResultSet.printable presents empty string when there are no errors or failures"

    scenario_results = [
        stub(ScenarioResult, __error__=None, __failure__=None),
    ]

    scenario_result_set = ScenarioResultSet(scenario_results, context=stub(RuntimeContext))

    expects(scenario_result_set.printable()).to.be.a(str)
    expects(scenario_result_set.printable()).to.be.empty
