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

"""tests for :class:`sure.runtime.Feature`"""

from unittest.mock import patch, call
from unittest.mock import Mock as Spy
from sure import expects
from sure.runtime import Feature, RuntimeOptions, ScenarioResult, Scenario
from sure.doubles import stub
from sure.errors import ExitFailure, ExitError


description = "tests for :class:`sure.runtime.Feature`"


def test_feature_with_description():
    "repr(sure.runtime.Feature) with description"

    feature = stub(Feature, title="title", description="description")

    expects(repr(feature)).to.equal('<Feature "description" title>')


def test_feature_without_description():
    "repr(sure.runtime.Feature) with description"

    feature = stub(Feature, title="title", description=None)

    expects(repr(feature)).to.equal('<Feature "title">')


@patch('sure.errors.sys.exit')
@patch('sure.runtime.RuntimeContext')
def test_feature_run_is_failure(RuntimeContext, exit):
    'Feature.run() should raise :class:`sure.errors.ExitFailure` at the occurrence of failure within an "immediate" failure context'

    reporter_spy = Spy(name='Reporter')
    scenario_result = stub(ScenarioResult, is_failure=True, __failure__=AssertionError('contrived failure'), __error__=None)
    scenario_run_spy = Spy(name="Scenario.run", return_value=scenario_result)

    scenario_stub = stub(Scenario, run=scenario_run_spy)
    feature_stub = stub(
        Feature,
        title="failure feature test",
        description=None,
        scenarios=[scenario_stub]
    )

    expects(feature_stub.run).when.called_with(reporter=reporter_spy, runtime=RuntimeOptions(immediate=True)).to.have.raised(
        ExitFailure,
        'ExitFailure'
    )
    expects(reporter_spy.mock_calls).to.equal([
        call.on_failure(scenario_stub, scenario_result)
    ])


@patch('sure.errors.sys.exit')
@patch('sure.runtime.RuntimeContext')
def test_feature_run_is_error(RuntimeContext, exit):
    'Feature.run() should raise :class:`sure.errors.ExitError` at the occurrence of error within an "immediate" error context'

    reporter_spy = Spy(name='Reporter')
    scenario_run_spy = Spy(name="Scenario.run")
    scenario_stub = stub(Scenario, run=scenario_run_spy)
    feature_stub = stub(
        Feature,
        title="error feature test",
        description=None,
        scenarios=[scenario_stub]
    )
    scenario_result = stub(ScenarioResult, is_error=True, __error__=ValueError('contrived error'), __failure__=None, is_failure=False, scenario=scenario_stub)
    scenario_run_spy.return_value = scenario_result

    expects(feature_stub.run).when.called_with(reporter=reporter_spy, runtime=RuntimeOptions(immediate=True)).to.have.raised(
        ExitError,
        'ExitError'
    )
    expects(reporter_spy.mock_calls).to.equal([
        call.on_error(scenario_stub, scenario_result)
    ])
