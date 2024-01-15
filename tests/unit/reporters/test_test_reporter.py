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
"unit tests for :mod:`sure.reporters.test`"

from unittest.mock import patch, call
from sure import expects
from sure.runner import Runner
from sure.runtime import Feature, Scenario, TestLocation, ScenarioResult, RuntimeContext
from sure.reporters.test import TestReporter
from sure.doubles import stub
from sure.errors import InternalRuntimeError


@patch("sure.reporters.test.events")
@patch("sure.reporters.test.time")
def test_test_reporter_on_failure(time, events):
    "TestReporter.on_failure()"

    time.time.return_value = "on_failure"
    reporter = TestReporter(stub(Runner))
    scenario = stub(Scenario, name="scenario-stub-name")
    scenario_result = stub(
        ScenarioResult, __error__=None, __failure__=AssertionError("test")
    )
    reporter.on_failure(scenario, scenario_result)

    expects(events.mock_calls).to.equal(
        [
            call.__getitem__("on_failure"),
            call.__getitem__().append(("on_failure", "scenario-stub-name", "failure")),
        ]
    )


@patch("sure.reporters.test.events")
@patch("sure.reporters.test.time")
def test_test_reporter_on_success(time, events):
    "TestReporter.on_success()"

    time.time.return_value = "on_success"
    reporter = TestReporter(stub(Runner))
    scenario = stub(Scenario, name="scenario-stub-name")
    reporter.on_success(scenario)

    expects(events.mock_calls).to.equal(
        [
            call.__getitem__("on_success"),
            call.__getitem__().append(("on_success", "scenario-stub-name")),
        ]
    )


@patch("sure.reporters.test.events")
@patch("sure.reporters.test.time")
def test_test_reporter_on_error(time, events):
    "TestReporter.on_error()"

    time.time.return_value = "on_error"
    reporter = TestReporter(stub(Runner))
    scenario = stub(Scenario, name="scenario-stub-name")
    scenario_result = stub(
        ScenarioResult, __failure__=None, __error__=RuntimeError("test")
    )
    reporter.on_error(scenario, scenario_result)

    expects(events.mock_calls).to.equal(
        [
            call.__getitem__("on_error"),
            call.__getitem__().append(("on_error", "scenario-stub-name", "error")),
        ]
    )


@patch("sure.reporters.test.events")
@patch("sure.reporters.test.time")
def test_test_reporter_on_internal_runtime_error(time, events):
    "TestReporter.on_internal_runtime_error()"

    time.time.return_value = "on_internal_runtime_error"
    reporter = TestReporter(stub(Runner))
    context = stub(RuntimeContext, name="scenario-stub-name", reporter=reporter)
    error = InternalRuntimeError(context, TypeError("test"))
    scenario_result = stub(ScenarioResult, __failure__=None, __error__=error)
    reporter.on_internal_runtime_error(context, scenario_result)

    expects(events.mock_calls).to.equal(
        [
            call.__getitem__("on_internal_runtime_error"),
            call.__getitem__().append(("on_internal_runtime_error", context, error)),
            call.__getitem__("on_internal_runtime_error"),
            call.__getitem__().append(
                ("on_internal_runtime_error", context, scenario_result)
            ),
        ]
    )
