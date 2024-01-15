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
from sure.reporter import Reporter
from sure.reporters import FeatureReporter
from sure.runner import Runner
from sure.doubles import stub, anything
from unittest.mock import patch

description = "tests for :class:`sure.reporter`"


def test_reporter_from_name():
    'sure.reporter.Reporter.from_name should return presently existing "reporters"'
    expects(Reporter.from_name('feature')).to.be(FeatureReporter)
    expects(Reporter.from_name).when.called_with('dummy').to.throw(
        RuntimeError,
        "no reporter found with name `dummy', options are: feature"
    )


def test_name_and_runner():
    'sure.reporter.Reporter.from_name_and_runner should return an instance of the given reporter type'

    runner_stub = stub(Runner)
    reporter = Reporter.from_name_and_runner('feature', runner_stub)
    expects(reporter).to.be.a(FeatureReporter)


def test_reporter_from_name_nonstring():
    'sure.reporter.Reporter.from_name raises TypeError when not receiving a string as argument'
    expects(Reporter.from_name).when.called_with(['not', 'string']).to.throw(
        TypeError,
        "name should be a str but got the list ['not', 'string'] instead"
    )


def test_reporter_instance_methods():
    "sure.reporter.Reporter() instance methods"
    runner_stub = stub(Runner)

    with patch('sure.reporter.Reporter.initialize') as initialize:
        reporter = Reporter(runner_stub, 'foo', bar='bar')
        initialize.assert_called_with('foo', bar='bar')

    reporter = Reporter(runner_stub)
    expects(repr(reporter)).to.equal('<Reporter>')

    expects(reporter.on_start).when.called.to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_feature).when.called_with(feature=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_feature_done).when.called_with(feature=anything, result=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_scenario).when.called_with(scenario=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_scenario_done).when.called_with(scenario=anything, result=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_failure).when.called_with(scenario_result=anything, error=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_success).when.called_with(scenario=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_internal_runtime_error).when.called_with(context=anything, exception=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_error).when.called_with(scenario_result=anything, error=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_finish).when.called_with(anything).to.have.raised(
        NotImplementedError
    )


@patch('sure.reporter.Reporter.initialize')
def test_from_name_and_runner(initialize):
    "sure.reporter.Reporter() instance methods"
    runner_stub = stub(Runner)

    reporter = Reporter(runner_stub, 'foo', bar='bar')

    expects(repr(reporter)).to.equal('<Reporter>')
    initialize.assert_called_with('foo', bar='bar')

    expects(reporter.on_start).when.called.to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_feature).when.called_with(feature=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_feature_done).when.called_with(feature=anything, result=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_scenario).when.called_with(scenario=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_scenario_done).when.called_with(scenario=anything, result=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_failure).when.called_with(scenario_result=anything, error=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_success).when.called_with(scenario=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_internal_runtime_error).when.called_with(context=anything, exception=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_error).when.called_with(scenario_result=anything, error=anything).to.have.raised(
        NotImplementedError
    )

    expects(reporter.on_finish).when.called_with(anything).to.have.raised(
        NotImplementedError
    )
