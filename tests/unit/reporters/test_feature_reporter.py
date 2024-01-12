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
"unit tests for :mod:`sure.reporters.feature`"

from unittest.mock import patch, call
from unittest.mock import Mock as Spy
from sure import expects
from sure.runner import Runner
from sure.runtime import Feature, Scenario, TestLocation, ScenarioResult
from sure.reporters import FeatureReporter
from sure.doubles import stub


def test_feature_reporter_on_start():
    "FeatureReporter.on_start"

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_start()

    expects(sh.mock_calls).to.equal([call.reset("\n")])


def test_feature_reporter_on_feature():
    "FeatureReporter.on_feature"

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_feature(stub(Feature, name="stubbed feature"))

    expects(sh.mock_calls).to.equal(
        [
            call.reset("  "),
            call.bold_blue("Feature: "),
            call.yellow("'"),
            call.green("stubbed feature"),
            call.yellow("'"),
            call.reset(" "),
        ]
    )


def test_feature_reporter_on_feature_done():
    "FeatureReporter.on_feature_done"

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_feature_done(
        stub(Feature, name="stubbed feature"),
        Spy(name="feature_result"),
    )

    expects(sh.mock_calls).to.equal(
        [
            call.reset("\n\n"),
        ]
    )


def test_feature_reporter_on_scenario():
    "FeatureReporter.on_scenario"

    location_stub = stub(TestLocation, description="Location of Scenario Stub")
    scenario_stub = stub(Scenario, location=location_stub)
    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_scenario(scenario_stub)

    expects(sh.mock_calls).to.equal(
        [
            call.reset("  "),
            call.bold_green("\n   Scenario: "),
            call.normal("Location of Scenario Stub"),
            call.reset(" "),
        ]
    )


def test_feature_reporter_on_scenario_avoids_reporting_twice():
    "FeatureReporter.on_scenario() should avoid reporting the same scenario twice per session"

    location_stub = stub(TestLocation, description="Location of Scenario Stub")
    scenario_stub = stub(Scenario, location=location_stub)
    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_scenario(scenario_stub)

    expects(sh.mock_calls).to.equal(
        [
            call.reset("  "),
            call.bold_green("\n   Scenario: "),
            call.normal("Location of Scenario Stub"),
            call.reset(" "),
        ]
    )
    reporter.on_scenario(scenario_stub)


def test_feature_reporter_on_scenario_test():
    "FeatureReporter.on_scenario() when a scenario does not have description"

    location_stub = stub(TestLocation, description="", name="test")
    scenario_stub = stub(Scenario, location=location_stub)
    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_scenario(scenario_stub)

    expects(sh.mock_calls).to.equal(
        [
            call.reset("  "),
            call.green("\n     Test: "),
            call.normal("test"),
            call.reset(" "),
        ]
    )


def test_feature_reporter_on_scenario_done_success():
    "FeatureReporter.on_scenario_done() on success"

    location_stub = stub(TestLocation)
    scenario_stub = stub(
        Scenario, location=location_stub, description="Description of Scenario Stub"
    )
    scenario_result_stub = stub(ScenarioResult, __error__=None, __failure__=None)

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_scenario_done(scenario_stub, scenario_result_stub)

    expects(sh.mock_calls).to.equal(
        [
            call.bold_green("✓"),
            call.reset(""),
        ]
    )
    # should not report twice
    reporter.on_scenario_done(scenario_stub, scenario_result_stub)
    expects(sh.mock_calls).to.equal(
        [
            call.bold_green("✓"),
            call.reset(""),
        ]
    )


def test_feature_reporter_on_scenario_done_failure():
    "FeatureReporter.on_scenario_done() on failure should not failure error because that's done by on_failure"

    location_stub = stub(TestLocation)
    scenario_stub = stub(
        Scenario, location=location_stub, description="Description of Scenario Stub"
    )
    scenario_result_stub = stub(
        ScenarioResult, __error__=None, __failure__=AssertionError("contrived failure")
    )

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_scenario_done(scenario_stub, scenario_result_stub)

    expects(sh.mock_calls).to.be.empty


def test_feature_reporter_on_scenario_done_error():
    "FeatureReporter.on_scenario_done() on error should not report error because that's done by on_error"

    location_stub = stub(TestLocation)
    scenario_stub = stub(
        Scenario, location=location_stub, description="Description of Scenario Stub"
    )
    scenario_result_stub = stub(
        ScenarioResult, __failure__=None, __error__=RuntimeError("contrived error")
    )

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_scenario_done(scenario_stub, scenario_result_stub)

    expects(sh.mock_calls).to.be.empty
