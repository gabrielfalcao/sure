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
import sys
from unittest.mock import patch, call
from unittest.mock import Mock as Spy
from sure import expects
from sure.runner import Runner
from sure.runtime import (
    Feature,
    Scenario,
    TestLocation,
    RuntimeContext,
    RuntimeOptions,
    ScenarioResult,
    ErrorStack,
    collapse_path,
)
from sure.reporters import FeatureReporter
from sure.doubles import stub, anything
from sure.errors import SpecialSyntaxDisabledError, InternalRuntimeError, exit_code


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

    reporter.on_feature(stub(Feature, name="Conflicts"))

    expects(sh.mock_calls).to.equal(
        [
            call.reset("  "),
            call.bold_blue("Feature: "),
            call.yellow("'"),
            call.green("Conflicts"),
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
    reporter.indentation = 5
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
    expects(reporter.indentation).to.equal(3)


def test_feature_reporter_on_scenario_done_without_description():
    "FeatureReporter.on_scenario_done() on success without scenario description"

    location_stub = stub(TestLocation)
    scenario_stub = stub(Scenario, location=location_stub, description="")
    scenario_result_stub = stub(ScenarioResult, __error__=None, __failure__=None)

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.indentation = 5
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
    expects(reporter.indentation).to.equal(1)


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


def test_feature_reporter_on_failure_failure():
    "FeatureReporter.on_failure() on failure should not failure error because that's done by on_failure"

    def contrive_exception_info():
        """contrives an exception to retrieve a list of traceback objects"""
        try:
            ErrorStack()
        except Exception as e:
            return e, sys.exc_info()

    exc, exc_info = contrive_exception_info()
    location = TestLocation(contrive_exception_info)
    error = ErrorStack(location=location, exc=exc, exception_info=exc_info)
    scenario_stub = stub(
        Scenario, location=location, description="Description of Scenario Stub"
    )
    scenario_result_stub = stub(
        ScenarioResult,
        __error__=None,
        __failure__=AssertionError("contrived failure"),
        stack=error,
        location=location,
    )

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.indentation = 5
    reporter.sh = sh
    reporter.on_failure(scenario_stub, scenario_result_stub)

    expects(sh.mock_calls).to.equal(
        [
            call.reset("\n"),
            call.reset("       "),
            call.yellow(
                f'Failure: contrived failure\n  File "{collapse_path(__file__)}", line 253, in contrive_exception_info\n    ErrorStack()\n'
            ),
            call.reset("         "),
            call.bold_blue("\n          Scenario:"),
            call.bold_blue(
                "\n              contrives an exception to retrieve a list of traceback objects"
            ),
            anything,
            call.reset("\n"),
        ]
    )


def test_feature_reporter_on_success():
    "FeatureReporter.on_success"

    location_stub = stub(TestLocation, description="Location of Scenario Stub")
    scenario_stub = stub(Scenario, location=location_stub)
    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_success(scenario_stub)

    expects(sh.mock_calls).to.equal(
        [
            call.bold_green("✓"),
            call.reset(""),
        ]
    )


def test_feature_reporter_on_error():
    "FeatureReporter.on_error"

    def contrive_exception_info():
        """contrives an exception to retrieve a list of traceback objects"""
        try:
            sys.exc_info(sys)
        except Exception as e:
            return e, sys.exc_info()

    exc, exc_info = contrive_exception_info()
    location = TestLocation(contrive_exception_info)
    scenario_stub = stub(Scenario, location=location)
    error = ErrorStack(location=location, exc=exc, exception_info=exc_info)
    scenario_result_stub = stub(
        ScenarioResult,
        __error__=exc,
        __failure__=None,
        stack=error,
        location=location,
    )

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_error(scenario_stub, scenario_result_stub)
    reporter.on_error(scenario_stub, scenario_result_stub)

    expects(sh.mock_calls).to.equal(
        [
            call.reset("\n"),
            call.bold_red(
                "Error TypeError('sys.exc_info() takes no arguments (1 given)')\n"
            ),
            call.bold_red(
                f'  File "{collapse_path(__file__)}", line 319, in contrive_exception_info\n    sys.exc_info(sys)\n'
            ),
            call.reset("  "),
            call.reset("\n"),
            call.bold_red(f"{collapse_path(__file__)}:316\n"),
        ]
    )


@patch("sure.reporters.feature.sys")
def test_feature_reporter_on_internal_runtime_error_special_syntax_error(sys):
    "FeatureReporter.on_internal_runtime_error() displays SpecialSyntaxDisabledError in yellow"

    def contrive_special_syntax_disabled_error():
        try:
            raise SpecialSyntaxDisabledError("yellow")
        except Exception as e:
            return e, sys.exc_info()

    exc, exc_info = contrive_special_syntax_disabled_error()
    location = TestLocation(contrive_special_syntax_disabled_error)
    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    context = stub(RuntimeContext, name="runtime-context-stub-name", reporter=reporter)
    error = ErrorStack(location=location, exc=exc, exception_info=exc_info)

    reporter.on_internal_runtime_error(context, error)

    expects(sh.mock_calls).to.equal([call.bold_yellow("\n yellow")])
    sys.exit.assert_called_once_with(exit_code(str(exc)))


@patch("sure.reporters.feature.sys.exit")
def test_feature_reporter_on_internal_runtime_error(exit):
    "FeatureReporter.on_internal_runtime_error() displays InternalRuntimeError in red"

    reporter = FeatureReporter(stub(Runner))
    context = stub(RuntimeContext, name="runtime-context-stub-name", reporter=reporter)
    sh = Spy(name="Shell")
    reporter.sh = sh

    def contrive_special_syntax_disabled_error():
        try:
            raise InternalRuntimeError(context, RuntimeError("fail"))
        except Exception as e:
            return e, sys.exc_info()

    exc, exc_info = contrive_special_syntax_disabled_error()
    location = TestLocation(contrive_special_syntax_disabled_error)
    error = ErrorStack(location=location, exc=exc, exception_info=exc_info)

    reporter.on_internal_runtime_error(context, error)

    expects(sh.mock_calls).to.equal(
        [
            call.bold_red(
                f'  File "{collapse_path(__file__)}", line 392, in contrive_special_syntax_disabled_error\n    raise InternalRuntimeError(context, RuntimeError("fail"))\n'
            )
        ]
    )
    exit.assert_called_once_with(exit_code(str(exc)))


def test_feature_reporter_on_finish():
    "FeatureReporter.on_finish() displays stats"

    reporter = FeatureReporter(stub(Runner))
    sh = Spy(name="Shell")
    reporter.sh = sh
    reporter.failures = {None}
    reporter.errors = {None}
    reporter.successes = list(range(8))
    options = RuntimeOptions(immediate=True, reap_warnings=True)
    context = stub(
        RuntimeContext,
        name="runtime-context-stub-name",
        reporter=reporter,
        options=options,
        warnings=[],
    )

    reporter.on_finish(context)
    expects(sh.mock_calls).to.equal(
        [
            call.reset(""),
            call.yellow("1 failed"),
            call.reset("\n"),
            call.red("1 errors"),
            call.reset("\n"),
            call.green("8 successful"),
            call.reset("\n"),
            call.reset(""),
        ]
    )


def test_feature_reporter_on_finish_with_warnings():
    "FeatureReporter.on_finish() displays stats and warnings"

    reporter = FeatureReporter(stub(Runner))
    sh = Spy(name="Shell")
    reporter.sh = sh
    reporter.failures = {None}
    reporter.errors = {None}
    reporter.successes = list(range(8))
    options = RuntimeOptions(immediate=True, reap_warnings=True)
    context = stub(
        RuntimeContext,
        name="runtime-context-stub-name",
        reporter=reporter,
        options=options,
        warnings=[{"message": "dangerous", "category": ResourceWarning}],
    )

    reporter.on_finish(context)
    expects(sh.mock_calls).to.equal(
        [
            call.reset(""),
            call.yellow("1 failed"),
            call.reset("\n"),
            call.red("1 errors"),
            call.reset("\n"),
            call.green("8 successful"),
            call.reset("\n"),
            call.reset(""),
            call.yellow("1 warnings"),
            call.reset("\n"),
            call.yellow("ResourceWarning: "),
            call.bold_black("dangerous\n"),
            call.reset("\n"),
        ]
    )
