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
import sys
from mock import patch
from mock import Mock as Spy
from sure import expects
from sure.doubles import stub, Dummy
from sure.runtime import (
    ScenarioResult,
    Scenario,
    RuntimeContext,
    TestLocation,
    ErrorStack,
)
from sure.errors import (
    CallerLocation,
    xor,
    exit_code,
    BaseSureError,
    ImmediateExit,
    RuntimeInterruption,
    ImmediateError,
    ImmediateFailure,
    ExitError,
    ExitFailure,
    InternalRuntimeError, SpecialSyntaxDisabledError, ExceptionManager
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
    expects(caller_location.path_and_lineno).to.equal(f"{collapse_path(__file__)}:81")


def test_runtime_interruption():
    "sure.errors.RuntimeInterruption should contain metadata about the given :class:`sure.runtime.ScenarioResult`"

    context = stub(RuntimeContext)
    scenario = stub(Scenario)
    scenario_result = stub(
        ScenarioResult,
        context=context,
        scenario=scenario,
        location=TestLocation(test_runtime_interruption),
        __error__=None,
        __failure__=None,
    )

    ri = RuntimeInterruption(scenario_result)

    expects(ri).to.have.property("result").being.equal(scenario_result)
    expects(ri).to.have.property("context").being.equal(context)
    expects(ri).to.have.property("scenario").being.equal(scenario)
    expects(repr(ri)).to.equal(
        f'scenario "sure.errors.RuntimeInterruption should contain metadata about the given :class:`sure.runtime.ScenarioResult`" \ndefined at {collapse_path(__file__)}:85'
    )
    expects(str(ri)).to.equal(
        f'scenario "sure.errors.RuntimeInterruption should contain metadata about the given :class:`sure.runtime.ScenarioResult`" \ndefined at {collapse_path(__file__)}:85'
    )


def test_immediate_error():
    "sure.errors.ImmediateError should store the error args and message"

    def make_error():
        try:
            raise RuntimeError("test")
        except RuntimeError as e:
            return e

    context = stub(RuntimeContext)
    scenario = stub(Scenario)
    location = TestLocation(make_error)
    error = make_error()
    scenario_result = stub(
        ScenarioResult,
        context=context,
        scenario=scenario,
        location=location,
        __error__=error,
        __failure__=None,
    )

    im_error = ImmediateError(scenario_result)
    expects(im_error).to.have.property("result").being.equal(scenario_result)
    expects(im_error).to.have.property("context").being.equal(context)
    expects(im_error).to.have.property("scenario").being.equal(scenario)
    expects(im_error).to.have.property("message").being.equal("test")
    expects(im_error).to.have.property("args").being.equal(("test",))
    expects(repr(im_error)).to.equal("test")


def test_immediate_failure():
    "sure.errors.ImmediateFailure should store the failure args and message"

    def make_failure():
        try:
            raise AssertionError("test")
        except AssertionError as e:
            return e, sys.exc_info()

    context = stub(RuntimeContext)
    scenario = stub(Scenario)
    location = TestLocation(make_failure)
    error, exc_info = make_failure()
    stack = ErrorStack(
        location=location,
        exc=error,
        exception_info=exc_info,
    )
    scenario_result = stub(
        ScenarioResult,
        context=context,
        scenario=scenario,
        location=location,
        stack=stack,
        __error__=None,
        __failure__=error,
    )

    im_failure = ImmediateFailure(scenario_result)
    expects(im_failure).to.have.property("result").being.equal(scenario_result)
    expects(im_failure).to.have.property("context").being.equal(context)
    expects(im_failure).to.have.property("scenario").being.equal(scenario)
    expects(im_failure).to.have.property("message").being.equal(
        f'  File "{collapse_path(__file__)}", line 148, in make_failure\n    raise AssertionError("test")\n'
    )
    expects(im_failure).to.have.property("args").being.equal(("test",))


@patch("sure.errors.sys")
def test_exit_error(sys):
    "sure.errors.ExitError() should call :meth:`sure.reporter.Reporter.on_error` and call :func:`sys.exit`"

    reporter_spy = Spy(name="reporter_spy")
    context = stub(RuntimeContext, reporter=reporter_spy)
    result = Dummy("sure.runtime.ScenarioResult")

    exit_error = ExitError(context, result)
    expects(exit_error).to.be.an(ExitError)
    reporter_spy.on_error.assert_called_once_with(context, result)
    sys.exit.assert_called_once_with(88)


@patch("sure.errors.sys")
def test_exit_failure(sys):
    "sure.errors.ExitFailure() should call :meth:`sure.reporter.Reporter.on_error` and call :func:`sys.exit`"

    reporter_spy = Spy(name="reporter_spy")
    context = stub(RuntimeContext, reporter=reporter_spy)
    result = Dummy("sure.runtime.ScenarioResult")

    exit_failure = ExitFailure(context, result)
    expects(exit_failure).to.be.an(ExitFailure)
    expects(reporter_spy.on_failure.called).to.be.false
    sys.exit.assert_called_once_with(64)


def test_internal_runtime_error():
    "sure.errors.InternalRuntimeError should call :meth:`sure.reporter.Reporter.on_internal_runtime_error`"

    def make_error():
        try:
            raise RuntimeError("test")
        except RuntimeError as e:
            return e

    reporter_spy = Spy(name="reporter_spy")
    context = stub(RuntimeContext, reporter=reporter_spy)
    error = make_error()

    internal_runtime_error = InternalRuntimeError(context, error)
    expects(internal_runtime_error).to.have.property("code").being.equal(40)
    expects(internal_runtime_error).to.have.property("traceback").being.equal("NoneType: None\n")
    expects(internal_runtime_error).to.have.property("context").being.equal(context)
    expects(internal_runtime_error).to.have.property("exception").being.equal(error)
    reporter_spy.on_internal_runtime_error.assert_called_once_with(context, internal_runtime_error)


def test_special_syntax_error():
    "sure.errors.SpecialSyntaxDisabledError"

    error = SpecialSyntaxDisabledError("Tension")
    expects(error).to.be.a(SpecialSyntaxDisabledError)
    expects(error).to.have.property("message").being.equal("Tension")


def test_caller_location():
    "sure.errors.CallerLocation"

    location = CallerLocation.most_recent()
    expects(location).to.have.property("name").being.equal("test_caller_location")
    expects(location).to.have.property("filename").being.equal(__file__)
    expects(location).to.have.property("lineno").being.equal(241)
    expects(location).to.have.property("path_and_lineno").being.equal(f"{collapse_path(__file__)}:241")
    expects(repr(location)).to.equal(f'<CallerLocation:test_caller_location {collapse_path(__file__)}:241>')
    expects(str(location)).to.equal(
        f"location = CallerLocation.most_recent() called within test_caller_location defined at {collapse_path(__file__)}:241>"
    )


def test_exception_manager_handle_special_syntax_disabled():
    "sure.errors.ExceptionManager should detect when an AttributeError seems to indicate an attempt to use Sure's Special Syntax and raise SpecialSyntaxDisabledError instead"
    error = AttributeError(f"{repr('ring')} object has no attribute 'should_not'")

    manager = ExceptionManager(error, TestLocation(test_exception_manager_handle_special_syntax_disabled))
    exc = manager.perform_handoff()

    expects(exc).to.be.a(SpecialSyntaxDisabledError)


def test_exception_manager_should_skip_attribute_error_whose_attribute_is_not_an_assertion_explicitly_defined_within_sure():
    "sure.errors.ExceptionManager should detect when an AttributeError seems to indicate an attempt to use Sure's Special Syntax and raise SpecialSyntaxDisabledError instead"
    error = AttributeError("'ring' object has no attribute 'freedom_of_thought'")

    manager = ExceptionManager(error, TestLocation(test_exception_manager_should_skip_attribute_error_whose_attribute_is_not_an_assertion_explicitly_defined_within_sure))
    exc = manager.perform_handoff()

    expects(exc).to.be.an(AttributeError)


def test_exception_manager_bypass_raising_special_syntax_disabled_when_attribute_error_does_not_seem_to_indicate_that_it_is_so():
    "sure.errors.ExceptionManager should "

    error = AttributeError("eye-twitch")

    manager = ExceptionManager(error, TestLocation(test_exception_manager_bypass_raising_special_syntax_disabled_when_attribute_error_does_not_seem_to_indicate_that_it_is_so))
    exc = manager.perform_handoff()

    expects(exc).to.be.an(AttributeError)
    expects(str(exc)).to.equal("eye-twitch")
