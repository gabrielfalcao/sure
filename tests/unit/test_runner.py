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
"unit tests for :mod:`sure.runner`"
import sys
import unittest
from pathlib import Path
from mock import patch
from mock import Mock as Spy
from sure import expects
from sure.errors import ExitError, ExitFailure, ImmediateError, ImmediateFailure
from sure.doubles import stub, Dummy
from sure.runner import Runner
from sure.runtime import RuntimeOptions, Feature, FeatureResult, ScenarioResult, TestLocation, ErrorStack


@patch("sure.runner.Reporter")
def test_runner_get_reporter(Reporter):
    "sure.runner.Runner.get_reporter() should fetch an instance of :class:`sure.reporter.Reporter` class from :mod:`sure.meta`'s internal registry"
    # Given an instance of :class:`~sure.runner.Runner` whose constructor is stubbed
    runner = stub(Runner)

    # When :meth:`~sure.runner.Runner.get_reporter` is called
    reporter = runner.get_reporter("reporter-name-dummy")

    # Then :meth:`~sure.reporter.Reporter.from_name_and_runner` is called with the `name' and `runner'
    Reporter.from_name_and_runner.assert_called_once_with("reporter-name-dummy", runner)

    # And the return value of `from_name_and_runner` is returned by `get_reporter'
    expects(reporter).to.equal(Reporter.from_name_and_runner.return_value)


@patch("sure.runner.Runner.get_reporter")
def test_runner_fetches_a_reporter_during_initialization(get_reporter):
    "sure.runner.Runner() should call :meth:`sure.runner.Reporter.get_reporter`"

    get_reporter.return_value = Dummy("Reporter")
    path = Path("~")
    options_stub = stub(RuntimeOptions)

    runner = Runner(
        base_path=path, reporter="reporter-name-dummy", options=options_stub
    )

    expects(runner).to.be.a(Runner)
    expects(runner).to.have.property("reporter").being.equal(Dummy("Reporter"))
    expects(runner).to.have.property("options").being.equal(options_stub)
    expects(runner).to.have.property("base_path").being.equal(path)

    expects(repr(runner)).to.equal(
        "<Runner base_path=PosixPath('~') reporter=<Dummy Reporter>>"
    )


@patch("sure.runner.loader")
def test_runner_find_candidates(loader):
    "sure.runner.Runner.find_candidates() should call :meth:`sure.runner.Reporter.get_reporter`"

    loader.load_recursive.return_value = [Dummy("dummy-module")]

    options_stub = stub(
        RuntimeOptions, immediate=False, ignore=Dummy("excludes"), glob_pattern="*.py"
    )
    runner = stub(Runner, options=options_stub)
    modules = runner.find_candidates(["dummy-path"])

    expects(modules).to.equal([Dummy("dummy-module")])

    loader.load_recursive.assert_called_once_with(
        "dummy-path", glob_pattern="*.py", excludes=Dummy("excludes")
    )


def test_runner_is_runnable_test_unittest_testcase():
    "sure.runner.Runner.is_runnable_test() should return ``True`` when receiving a subclass of :class:`unittest.TestCase`"

    options_stub = stub(
        RuntimeOptions,
        immediate=False,
        ignore=Dummy("excludes"),
    )
    runner = stub(Runner, options=options_stub)

    class DummyUnitTest(unittest.TestCase):
        pass

    expects(runner.is_runnable_test(DummyUnitTest)).to.not_be.false
    expects(runner.is_runnable_test(unittest.TestCase)).to.be.false


def test_runner_is_runnable_class_type_seems_to_indicate_test():
    "sure.runner.Runner.is_runnable_test() should return ``True`` when receiving a class other than :class:`unittest.TestCase` whose name seem to indicate that it is a test"

    options_stub = stub(RuntimeOptions)
    runner = stub(Runner, options=options_stub)

    class NotATest:
        pass

    class TestClass:
        pass

    expects(runner.is_runnable_test(NotATest)).to.be.false
    expects(runner.is_runnable_test(TestClass)).to.not_be.false

    class NotASpec:
        pass

    class SpecClass:
        pass

    expects(runner.is_runnable_test(NotASpec)).to.be.false
    expects(runner.is_runnable_test(SpecClass)).to.not_be.false

    class NotAScenario:
        pass

    class ScenarioClass:
        pass

    expects(runner.is_runnable_test(NotAScenario)).to.be.false
    expects(runner.is_runnable_test(ScenarioClass)).to.not_be.false


def test_runner_is_runnable_test_function():
    "sure.runner.Runner.is_runnable_test() should return ``True`` when receiving a function whose name seems to indicate that it is test"

    runner = stub(Runner, options=stub(RuntimeOptions))

    def test_function():
        pass

    def dummy_function():
        pass

    expects(runner.is_runnable_test(test_function)).should_not.be.false
    expects(runner.is_runnable_test(dummy_function)).should_not.be.true


def test_runner_is_runnable_should_return_false_when_receiving_neither_a_function_or_class_type():
    "sure.runner.Runner.is_runnable_test() should return ``False`` when receiving an object that is neither a function or a class type"

    runner = stub(Runner, options=stub(RuntimeOptions))
    expects(runner.is_runnable_test(dict())).should_not.be.true
    expects(runner.is_runnable_test(set())).should_not.be.true
    expects(runner.is_runnable_test(tuple())).should_not.be.true
    expects(runner.is_runnable_test(list())).should_not.be.true


def test_runner_extract_members_should_return_tuple_with_the_candidate_and_its_extracted_members():
    "sure.runner.Runner.is_runnable_test() should return ``True`` when receiving a class other than :class:`unittest.TestCase` whose name seem to indicate that it is a test"

    options_stub = stub(RuntimeOptions)
    runner = stub(Runner, options=options_stub)

    class TestExtractMembers(unittest.TestCase):
        def test_0(self):
            pass

        def test_2(self):
            pass

        def test_4(self):
            pass

        def nontest_method(self):
            pass

    expects(runner.extract_members(TestExtractMembers)).to.equal(
        (
            TestExtractMembers,
            [
                TestExtractMembers.test_0,
                TestExtractMembers.test_2,
                TestExtractMembers.test_4,
            ],
        )
    )


@patch("sure.errors.sys.exit")
@patch("sure.runner.Runner.load_features")
def test_runner_execute_behavior_on_immediate_failure(load_features, exit):
    """sure.runner.Runner.execute() should raise :exc:`sure.errors.ExitFailure`"""

    options = RuntimeOptions(immediate=True)
    reporter = Spy(name="reporter")
    runner = stub(Runner, options=options, reporter=reporter)

    feature_result_stub = stub(FeatureResult, is_failure=True)
    feature_stub = stub(
        Feature, run=lambda self, reporter, runtime: feature_result_stub
    )
    load_features.return_value = [feature_stub]
    dummy_path = Dummy("pathlib.Path")
    expects(runner.execute).when.called_with([dummy_path]).to.have.raised(ExitFailure)
    exit.assert_called_once_with(64)


@patch("sure.errors.sys.exit")
@patch("sure.runner.Runner.load_features")
def test_runner_execute_behavior_on_immediate_error(load_features, exit):
    """sure.runner.Runner.execute() should raise :exc:`sure.errors.ExitError`"""

    options = RuntimeOptions(immediate=True)
    reporter = Spy(name="reporter")
    runner = stub(Runner, options=options, reporter=reporter)

    feature_result_stub = stub(FeatureResult, is_error=True, is_failure=False)
    feature_stub = stub(
        Feature, run=lambda self, reporter, runtime: feature_result_stub
    )
    load_features.return_value = [feature_stub]
    dummy_path = Dummy("pathlib.Path")
    expects(runner.execute).when.called_with([dummy_path]).to.have.raised(ExitError)
    exit.assert_called_once_with(88)


@patch("sure.runner.Runner.execute")
def test_runner_run_behavior_on_immediate_failure(execute):
    """sure.runner.Runner.run() should raise :exc:`sure.errors.ExitFailure`"""

    def contrive_failure():
        try:
            raise AssertionError("test")
        except Exception as e:
            return e, sys.exc_info()

    exc, exc_info = contrive_failure()
    options = RuntimeOptions(immediate=True)
    reporter = Spy(name="reporter")
    runner = stub(Runner, options=options, reporter=reporter)

    location = TestLocation(contrive_failure)
    scenario_result_stub = stub(
        ScenarioResult,
        result=Dummy("failure.result"),
        scenario=Dummy("scenario_dummy"),
        context=Dummy("context"),
        location=location,
        __error__=None,
        __failure__=exc,
        stack=ErrorStack(location, exc, exc_info),
    )
    execute.side_effect = ImmediateFailure(scenario_result_stub)
    expects(runner.run(Dummy("path"))).to.equal(scenario_result_stub)

    execute.assert_called_once_with(Dummy("path"))


@patch("sure.runner.Runner.execute")
def test_runner_run_behavior_on_immediate_error(execute):
    """sure.runner.Runner.run() should raise :exc:`sure.errors.ExitError`"""

    def contrive_error():
        try:
            raise RuntimeError("test")
        except Exception as e:
            return e, sys.exc_info()

    exc, exc_info = contrive_error()
    options = RuntimeOptions(immediate=True)
    reporter = Spy(name="reporter")
    runner = stub(Runner, options=options, reporter=reporter)

    location = TestLocation(contrive_error)
    error = ErrorStack(location, exc, exc_info)
    scenario_result_stub = stub(
        ScenarioResult,
        result=Dummy("error.result"),
        scenario=Dummy("scenario_dummy"),
        context=Dummy("context"),
        location=location,
        __error__=exc,
        __failure__=None,
        stack=error,
    )

    execute.side_effect = ImmediateError(scenario_result_stub)
    expects(runner.run(Dummy("path"))).to.equal(scenario_result_stub)

    execute.assert_called_once_with(Dummy("path"))
