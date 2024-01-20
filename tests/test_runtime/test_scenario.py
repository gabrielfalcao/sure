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

"""tests for :class:`sure.runtime.Scenario`"""


from unittest.mock import patch, call
from unittest.mock import Mock as Spy
from sure import expects
from sure.runtime import (
    Scenario,
    RuntimeOptions,
    ScenarioResult,
    RuntimeRole,
    RuntimeContext,
    ScenarioResultSet,
)
from sure.doubles import stub, Dummy, anything
from sure.errors import ExitFailure, ExitError


description = "tests for :class:`sure.runtime.Scenario`"


@patch("sure.errors.sys.exit")
@patch("sure.runtime.ScenarioArrangement")
def test_scenario_run_when_result_is_failure(ScenarioArrangement, exit):
    "Scenario.run() should raise :class:`sure.errors.ExitError` when a failure occurs"

    scenario_stub = stub(
        Scenario,
        object=Dummy("scenario.object"),
    )
    reporter_spy = Spy(name="Reporter")
    scenario_arrangement = ScenarioArrangement.return_value
    scenario_arrangement.scenario = scenario_stub
    ScenarioArrangement.from_generic_object.return_value = scenario_arrangement
    scenario_arrangement.uncollapse_nested.return_value = [scenario_arrangement]
    scenario_result = stub(
        ScenarioResult,
        is_failure=True,
        is_success=False,
        is_error=False,
        scenario=scenario_stub,
    )
    scenario_arrangement.run.return_value = [(scenario_result, RuntimeRole.Unit)]

    context = stub(
        RuntimeContext, options=RuntimeOptions(immediate=False), reporter=reporter_spy
    )
    scenario_result_set = scenario_stub.run(context)

    expects(scenario_result_set).to.be.a(ScenarioResultSet)
    expects(reporter_spy.mock_calls).to.equal(
        [
            call.on_scenario(scenario_arrangement.scenario),
            call.on_failure(scenario_stub, scenario_result),
            call.on_scenario_done(scenario_arrangement.scenario, scenario_result),
        ]
    )


@patch("sure.errors.sys.exit")
@patch("sure.runtime.ScenarioArrangement")
def test_scenario_run_when_result_is_failure_and_runtime_options_immediate(
    ScenarioArrangement, exit
):
    'Scenario.run() should raise :class:`sure.errors.ExitError` when a failure occurs and the runtime context is configured to "fail immediately"'

    reporter_spy = Spy(name="Reporter")
    scenario_arrangement = ScenarioArrangement.return_value
    ScenarioArrangement.from_generic_object.return_value = scenario_arrangement
    scenario_arrangement.uncollapse_nested.return_value = [scenario_arrangement]
    scenario_stub = stub(
        Scenario,
        object=Dummy("scenario.object"),
    )
    scenario_result = stub(
        ScenarioResult,
        is_failure=True,
        is_success=False,
        is_error=False,
        scenario=scenario_stub,
    )
    scenario_arrangement.run.return_value = [(scenario_result, RuntimeRole.Unit)]

    context = stub(
        RuntimeContext, options=RuntimeOptions(immediate=True), reporter=reporter_spy
    )
    expects(scenario_stub.run).when.called_with(context).should.have.raised(ExitFailure)

    expects(reporter_spy.mock_calls).to.equal(
        [
            call.on_scenario(scenario_arrangement.scenario),
            call.on_failure(scenario_stub, scenario_result),
        ]
    )


@patch("sure.errors.sys.exit")
@patch("sure.runtime.ScenarioArrangement")
def test_scenario_run_when_result_is_error_and_runtime_options_immediate(
    ScenarioArrangement, exit
):
    'Scenario.run() should raise :class:`sure.errors.ExitError` when an error occurs and the runtime context is configured to "error immediately"'

    reporter_spy = Spy(name="Reporter")
    scenario_arrangement = ScenarioArrangement.return_value
    ScenarioArrangement.from_generic_object.return_value = scenario_arrangement
    scenario_arrangement.uncollapse_nested.return_value = [scenario_arrangement]
    scenario_stub = stub(
        Scenario,
        object=Dummy("scenario.object"),
    )
    scenario_result = stub(
        ScenarioResult,
        is_error=True,
        is_success=False,
        is_failure=False,
        scenario=scenario_stub,
    )
    scenario_arrangement.run.return_value = [(scenario_result, RuntimeRole.Unit)]

    context = stub(
        RuntimeContext, options=RuntimeOptions(immediate=True), reporter=reporter_spy
    )
    expects(scenario_stub.run).when.called_with(context).should.have.raised(ExitError)

    expects(reporter_spy.mock_calls).to.equal(
        [
            call.on_scenario(scenario_arrangement.scenario),
            call.on_error(scenario_stub, scenario_result),
        ]
    )
