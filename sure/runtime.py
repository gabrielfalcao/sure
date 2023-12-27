# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2023>  Gabriel Falcão <gabriel@nacaolivre.org>
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
import os
import re
import sys
import types
import inspect
import logging
import unittest
import traceback
from pathlib import Path
from functools import reduce
from typing import Dict, List, Optional, Any, Callable

from mock import Mock

from sure.errors import (
    ExitError,
    ExitFailure,
    NonValidTest,
    ImmediateError,
    ImmediateFailure,
)
from sure.loader import loader
from sure.reporter import Reporter

self = sys.modules[__name__]


log = logging.getLogger(__name__)


class BaseContainer(object):
    """base-class for runtime containers"""


def object_name(so) -> str:
    """so: stands for "some object"""
    if isinstance(so, type):
        return f"{so.__module__}.{so.__name__}"

    elif hasattr(so, "__name__"):
        return so.__name__

    elif hasattr(so, "__class__"):
        return so.__class__.__name__

    return getattr(so, "__name__", repr(so))


def seem_to_indicate_setup(name: str) -> bool:
    return re.search(r"^(setUp|setup|set_up)$", name or "")


def seem_to_indicate_teardown(name: str) -> bool:
    return re.search(r"^(tearDown|teardown|tear_down)$", name or "")


def seem_to_indicate_test(name: str) -> bool:
    return re.search(r"^(Ensure|Test|Spec|Scenario)", name or "", re.I)


def appears_to_be_runnable(name: str) -> bool:
    return any(
        tuple(
            map(
                lambda check: check(name),
                (
                    seem_to_indicate_setup,
                    seem_to_indicate_test,
                    seem_to_indicate_teardown,
                ),
            )
        )
    )


class TestLocation(object):
    def __init__(self, test, ancestor=None):
        self.test = test
        self.code = test.__code__
        self.filename = self.code.co_filename
        self.line = self.code.co_firstlineno
        self.kind = self.test.__class__
        self.name = isinstance(self.test, types.FunctionType) and self.test.__name__ or self.test.__func__.__name__
        self.ancestor = ancestor
        self.ancestral_description = ""
        self.ancestor_repr = ""
        if ancestor:
            self.ancestral_description = getattr(
                ancestor, "description", ""
            ) or getattr(
                ancestor, "__doc__", ""
            )
            if isinstance(ancestor, type):
                self.ancestor_repr = (
                    f"({self.ancestor.__module__}.{self.ancestor.__name__})"
                )
            elif isinstance(ancestor, str):
                self.ancestor_repr = ancestor
            else:
                raise NotImplementedError

        self.description = getattr(self.test, '__func__', self.test).__doc__ or ""

    def __repr__(self):
        return " ".join([self.name, "at", self.ort])

    def __str__(self):
        return "\n".join(
            [
                f'scenario "{self.description}" ',
                f"defined at {self.ort}",
            ]
        )

    @property
    def ort(self):
        return collapse_path(f"{self.filename}:{self.line}")


class Container(BaseContainer):
    owner: Optional[object]
    name: str
    runnable: callable
    location: TestLocation
    nested_containers: List[BaseContainer]

    def __init__(
        self,
        name: str,
        runnable: callable,
        location: TestLocation,
        owner: Optional[object] = None,
        nested: Optional[List[BaseContainer]] = None,
    ):
        self.name = name
        self.runnable = runnable
        self.location = location
        self.owner = owner
        self.nested = nested or []

    @property
    def unit(self):
        return self.runnable

    def __repr__(self):
        return f"<{repr(self.runnable)} at {self.location.ort}>"


class Logort(object):
    def __init__(self, scenario):
        self.internal = logging.getLogger(".".join((__name__, object_name(scenario))))
        self.internal.handlers = []
        self.internal.addHandler(self.log_handler())
        scenario_id = getattr(scenario, "id", None)
        scenario_id = callable(scenario_id) and scenario_id() or scenario_id
        self.external = logging.getLogger(scenario_id)
        self.locations = []

        self.history = [
            self.internal,
            self.external,
        ]

    @classmethod
    def log_handler(cls):
        return logging.FileHandler(f"/tmp/sure%{os.getpid()}.log")

    @property
    def current(self):
        return self.history[-1]

    def set_location(self, location):
        default_logger = logging.getLogger()
        self.locations.append(location)
        self.history.append(logging.getLogger(location.ort))
        for logger in self.history:
            logger.setLevel(default_logger.level)
            logger.handlers = [self.log_handler]


class RuntimeOptions(object):
    immediate: bool

    def __init__(self, immediate: bool):
        self.immediate = immediate

    def __repr__(self):
        return f"<RuntimeOptions immediate={self.immediate}>"


class RuntimeContext(object):
    reporter: Reporter
    runtime: RuntimeOptions

    def __init__(self, reporter: Reporter, runtime: RuntimeOptions):
        self.reporter = reporter
        self.runtime = runtime

    def __repr__(self):
        return f"<RuntimeContext reporter={self.reporter} runtime={self.runtime}>"


class BaseResult(object):
    def __init__(self, results, reporter: Reporter):
        self.results = results
        self.reporter = reporter

    def __nonzero__(self):
        return self.ok

    @property
    def ok(self):
        errors = set([x.is_error for x in self.results])
        failures = set([x.is_failure for x in self.results])
        return len(errors.union(failures)) == 0


class RuntimeRole:
    Setup = reduce(lambda L, R: L ^ R, b"Setup")
    Unit = reduce(lambda L, R: L ^ R, b"Unit")
    Teardown = reduce(lambda L, R: L ^ R, b"Teardown")


class PreparedTestSuiteContainer(BaseContainer):
    """Thought with the goal of providing a hermetically isolated
    environment where the runtime context and associated reporters are
    kept in sync with potentially nested occurrences of scenarios

    Contains a setup/teardown and a list of runnable tests associated
    with a :py:class:`unittest.TestCase` along with a reference to the
    original instance and a runtime context.
    """

    source: Any
    context: RuntimeContext
    setup_methods: List[Callable]
    teardown_methods: List[Callable]
    test_methods: List[BaseContainer]
    nested_suites: List[BaseContainer]

    def __init__(
        self,
        source: Any,
        context: RuntimeContext,
        setup_methods: List[Callable],
        teardown_methods: List[Callable],
        test_methods: List[Callable],
        nested_suites: List[BaseContainer],
    ):
        self.error = None
        self.failure = None
        if isinstance(source, type):
            self.source_instance = source()
        elif callable(source):
            test_methods.insert(0, Container(source.__name__, source, TestLocation(
                source, source.__module__
            ), source.__module__))
            self.source_instance = source.__module__
        else:
            raise NotImplementedError(f"PreparedTestSuiteContainer received unexpected type: {source}")

        self.log = Logort(self.source_instance)
        self.context = context
        self.setup_methods = setup_methods
        self.teardown_methods = teardown_methods
        self.test_methods = test_methods

    @property
    def tests(self):
        return self.test_methods

    def run_predicates(self, context):
        for name, setup, location in self.setup_methods:
            yield self.invoke_contextualized(
                setup, context, name=name, location=location
            )

    def run_complements(self, context):
        for name, setup, location in self.teardown_methods:
            yield self.invoke_contextualized(
                setup, context, name=name, location=location
            )

    @classmethod
    def from_generic_object(cls, some_object, context: RuntimeContext):
        test_methods = []
        setup_methods = []
        teardown_methods = []
        nested_suites = []
        for name in dir(some_object):
            if not appears_to_be_runnable(name):
                log.debug(f"ignoring {some_object}.{name}")
                continue

            # <unittest.TestCase.__init__>
            #   constructs instance of unittest.TestCase and filter out each runnable
            if isinstance(some_object, type) and issubclass(
                some_object, unittest.TestCase
            ):
                # TODO: warn about possibility of abuse of TestCase constructor taking wrong arguments
                runnable = getattr(some_object(name), name, None)
            else:
                # TODO: support non-unittest.TestCase classes
                runnable = getattr(some_object, name, None)
            # </unittest.TestCase.__init__>

            if isinstance(runnable, types.MethodType):
                location = TestLocation(
                    runnable, isinstance(some_object, type) and some_object or None
                )

                if seem_to_indicate_setup(name):
                    # TODO: warn about probability of abuse of TestCase constructor taking non-standard arguments
                    setup_methods.append(
                        Container(name, runnable, location, some_object)
                    )
                elif seem_to_indicate_test(name):
                    test_methods.append(
                        Container(name, runnable, location, some_object)
                    )
                elif seem_to_indicate_teardown(name):
                    teardown_methods.append(
                        Container(name, runnable, location, some_object)
                    )

            elif isinstance(runnable, type):
                nested_suites.append((name, cls.from_generic_object(runnable, context)))
            else:
                raise NotImplementedError

        return cls(
            source=some_object,
            context=context,
            setup_methods=setup_methods,
            teardown_methods=teardown_methods,
            test_methods=test_methods,
            nested_suites=nested_suites,
        )

    def run(self, context, tests):
        last_failure = None
        last_error = None

        try:
            for result in self.run_predicates(context):
                yield result, RuntimeRole.Setup
        except Exception as error:
            # the apparent non-distinguishingly catching of
            # AssertionError instances is intentional to the present
            # conceptual context during this period of ponderation in
            # regards to the status-quo of what begs the non-essential
            # whole-truth to be exposed, coming from the current
            # presupposition that predicates are inherently
            # non-supposed to make assertions of any kind, but rather
            # prepare the subject-under-test to undergo a test process
            # in such way that the process itself is, in its turn,
            # presupposed not to raise any exceptions other than
            # assertions whose purpose is not to fail unreasonably but
            # to expose the failures of the system comprised of the
            # referred subject along with other subject-object targets
            # which beg scrutinity from a careful developer.
            return ScenarioResult(self, location=None, context=context, error=error)

        try:
            for container in tests:
                for result, role in self.run_container(container, context):
                    yield result, role
        finally:
            for result in self.run_complements(context):
                yield result, RuntimeRole.Teardown

    def run_container(self, container, context):
        result = self.perform_unit(
            container=container,
            context=context,
            name=container.name,
            location=container.location,
        )
        if result.failure:
            last_failure = result
        if result.error:
            last_error = result

        if context.runtime.immediate:
            if last_error is not None:
                raise ImmediateError(last_error)
            if last_failure is not None:
                raise ImmediateFailure(last_failure)

        yield result, RuntimeRole.Unit

    def perform_unit(self, container, context, name, location):
        self.log.set_location(location)
        try:
            self.invoke_contextualized(container, context, name, location)
        except AssertionError as failure:
            return ScenarioResult(self, location, context, failure)

        except Exception as error:
            return ScenarioResult(self, location, context, error)

        return ScenarioResult(self, location, context)

    def invoke_contextualized(self, container, context, name, location):
        """exception handling is left to the caller"""
        if not isinstance(container, BaseContainer):
            raise RuntimeError(f"expected {container} to be an instance of BaseContainer in this instance")
        self.log.set_location(location)
        code = container.unit.__code__
        varnames = set(code.co_varnames).intersection({"context"})
        argcount = len(varnames)

        if argcount == 0:
            return container.unit()
        elif argcount == 1:
            return container.unit(context)
        else:
            raise NonValidTest(
                f"it appears that the test function {name} {location} takes more than one argument: {argcount}"
            )


class Feature(object):
    def __init__(self, module):
        name = getattr(
            module,
            "suite_name",
            getattr(module, "feature", getattr(module, "name", module.__name__)),
        )
        description = getattr(
            module, "suite_description", getattr(module, "description", "")
        )

        self.name = stripped(name)
        self.description = stripped(description)

        self.module = module
        self.ready = False
        self.scenarios = []

    def read_scenarios(self, suts):
        self.scenarios = list(map((lambda e: Scenario(e, self)), suts))
        self.ready = True
        return self.scenarios

    def run(self, reporter, runtime: RuntimeOptions):
        results = []
        for scenario in self.scenarios:
            context = RuntimeContext(reporter, runtime)

            reporter.on_scenario(scenario)

            result = scenario.run(context)

            results.append(result)
            if result.is_failure:
                reporter.on_failure(scenario, result)
                if runtime.immediate:
                    raise ExitFailure(context, result)

            elif result.is_error:
                reporter.on_error(scenario, result)
                if runtime.immediate:
                    raise ExitError(context, result)

            else:
                reporter.on_success(scenario)

            reporter.on_scenario_done(scenario, result)

        return FeatureResult(results)


class ErrorStack(object):
    def __init__(self, location: TestLocation, exc: Exception, exception_info=None):
        self.exception_info = exception_info or sys.exc_info()
        self.traceback = self.exception_info[-1]
        self.exception = exc
        self.location = location

    def location_specific_stack(self):
        return [collapse_path(e) for e in traceback.format_tb(self.traceback) if self.location.name in e]

    def location_specific_error(self):
        stack = self.location_specific_stack()
        return collapse_path(stack and stack[-1] or str(self.exception))

    def nonlocation_specific_stack(self):
        return [collapse_path(e) for e in traceback.format_tb(self.traceback) if self.location.name not in e]

    def nonlocation_specific_error(self):
        stack = self.nonlocation_specific_stack()
        return collapse_path(stack and stack[-1] or str(self.exception))

    def __str__(self):
        return "\n".join(self.location_specific_stack())


class Scenario(object):
    def __init__(self, class_or_callable, feature):
        self.id = class_or_callable.__name__
        self.log = Logort(self)
        self.description = stripped(class_or_callable.__doc__ or self.id)

        self.object = class_or_callable
        self.object_ancestor = None
        if isinstance(class_or_callable, type):
            if issubclass(class_or_callable, unittest.TestCase):
                self.object_ancestor = class_or_callable

        self.feature = feature

    def run(self, context):
        collector = PreparedTestSuiteContainer.from_generic_object(self.object, context)

        results = []
        for result, role in collector.run(context, collector.tests):
            if role != RuntimeRole.Unit:
                continue
            results.append(result)
            if result.is_success:
                continue
            if context.runtime.immediate:
                # TODO: consider non-reliance on ScenarioResultSet.__getattr__ proxying attributes from results[-1]
                return ScenarioResultSet(results, context)

        return ScenarioResultSet(results, context)


class ScenarioResult(BaseResult):
    scenario: Scenario
    error: Optional[Exception]
    failure: Optional[AssertionError]
    location: TestLocation

    def __init__(
        self, scenario, location: TestLocation, context: RuntimeContext, error=None
    ):
        self.scenario = scenario
        self.location = location
        self.context = context
        self.exc_info = sys.exc_info()
        self.stack = ErrorStack(location, error, self.exc_info)
        self.__error__ = None
        self.__failure__ = None

        if isinstance(error, AssertionError):
            self.__failure__ = error
        else:
            self.__error__ = error

    def tb(self):
        return traceback.format_exception(*self.exc_info)

    @property
    def label(self) -> str:
        if self.ok:
            return "OK"
        if self.is_failure:
            return "FAILURE"
        if self.is_error:
            return "ERROR"

        raise "..."

    def __str__(self):
        return "\n".join(
            [
                f"{self.printable()}",
            ]
        )

    def printable(self):
        prelude = f"{self.location}"
        hook = ""
        if callable(getattr(self.error, "printable", None)):
            hook = self.error.printable()

        return " ".join(filter(bool, [prelude, hook]))

    @property
    def is_error(self):
        return isinstance(self.error, (ErrorStack, Exception))

    @property
    def error(self) -> Optional[Exception]:
        if not isinstance(self.__error__, AssertionError):
            return self.__error__

    def set_error(self, error: Optional[Exception]):
        self.__error__ = error

    @property
    def is_failure(self):
        return isinstance(self.__failure__, AssertionError)

    @property
    def failure(self) -> Optional[AssertionError]:
        if self.is_failure:
            return self.__failure__

    @property
    def is_success(self) -> bool:
        return not self.is_error and not self.is_failure

    @property
    def ok(self):
        return self.is_success

    @property
    def succinct_failure(self) -> str:
        if not self.is_failure:
            return ""

        return self.stack.location_specific_error()


class ScenarioResultSet(ScenarioResult):
    error: Optional[ScenarioResult]
    failure: Optional[ScenarioResult]

    def __init__(self, scenario_results: List[ScenarioResult], context: RuntimeContext):
        self.scenario_results = scenario_results
        self.failed_scenarios = []
        self.errored_scenarios = []

        for scenario in scenario_results:
            if scenario.is_failure:
                self.failed_scenarios.append(scenario)
            if scenario.is_error:
                self.errored_scenarios.append(scenario)

    def __getattr__(self, attr, fallback=None):
        try:
            return self.__getattribute__(attr)
        except AttributeError:
            return getattr(self.scenario_results[-1], attr, fallback)

    def printable(self):
        if self.failure is not None:
            return self.failure
        if self.error:
            return self.error.printable()

        return ""

    @property
    def is_error(self):
        return len(self.errored_scenarios) > 0

    @property
    def error(self) -> Optional[Exception]:
        for scenario in self.errored_scenarios:
            if scenario.is_error:
                return scenario.error

    @property
    def is_failure(self):
        return len(self.failed_scenarios) > 0

    @property
    def failure(self) -> Optional[Exception]:
        for scenario in self.failed_scenarios:
            if scenario.is_failure:
                return scenario.failure

    @property
    def succinct_failure(self) -> Optional[str]:
        for scenario in self.failed_scenarios:
            if scenario.is_failure:
                return scenario.succinct_failure

    @property
    def first_scenario_result_error(self) -> Optional[ScenarioResult]:
        for scenario in self.errored_scenarios:
            if scenario.is_error:
                return scenario

    @property
    def first_scenario_result_fail(self) -> Optional[ScenarioResult]:
        for scenario in self.failed_scenarios:
            if scenario.is_failure:
                return scenario

    @property
    def first_nonsuccessful_result(self) -> Optional[ScenarioResult]:
        return self.first_scenario_result_error or self.first_scenario_result_fail


class FeatureResult(BaseResult):
    scenario_results: ScenarioResultSet
    error: Optional[Exception]
    failure: Optional[AssertionError]

    def __init__(self, scenario_results, error=None):
        self.scenario_results = scenario_results
        self.failed_scenarios = []
        self.errored_scenarios = []

        for scenario in scenario_results:
            if scenario.is_error:
                self.errored_scenarios.append(scenario)
            if scenario.is_failure:
                self.failed_scenarios.append(scenario)

    def printable(self):
        if self.failure is not None:
            return self.failure
        if self.error:
            return self.error.printable()

        return ""

    @property
    def is_error(self):
        return len(self.errored_scenarios) > 0

    @property
    def error(self) -> Optional[Exception]:
        for scenario in self.errored_scenarios:
            if scenario.is_error:
                return scenario.error

    @property
    def is_failure(self):
        return len(self.failed_scenarios) > 0

    @property
    def failure(self) -> Optional[Exception]:
        for scenario in self.failed_scenarios:
            if scenario.is_failure:
                return scenario.failure

    @property
    def succinct_failure(self) -> Optional[str]:
        for scenario in self.failed_scenarios:
            if scenario.is_failure:
                return scenario.succinct_failure

    @property
    def first_scenario_result_error(self) -> Optional[ScenarioResult]:
        for scenario in self.errored_scenarios:
            if scenario.is_error:
                return scenario

    @property
    def first_scenario_result_fail(self) -> Optional[ScenarioResult]:
        for scenario in self.failed_scenarios:
            if scenario.is_failure:
                return scenario

    @property
    def first_nonsuccessful_result(self) -> Optional[ScenarioResult]:
        return self.first_scenario_result_error or self.first_scenario_result_fail


class FeatureResultSet(BaseResult):
    error: Optional[Exception]
    failure: Optional[AssertionError]

    def __init__(self, feature_results, error=None):
        self.feature_results = feature_results
        self.failed_features = []
        self.errored_features = []

        for feature in feature_results:
            if feature.is_error:
                self.errored_features.append(feature)
            if feature.is_failure:
                self.failed_features.append(feature)

    def printable(self):
        if self.failure is not None:
            return self.failure
        if self.error:
            return self.error.printable()

        return ""

    @property
    def is_error(self):
        return len(self.errored_features) > 0

    @property
    def error(self) -> Optional[Exception]:
        for feature in self.errored_features:
            if feature.is_error:
                return collapse_path(feature.error)

    @property
    def is_failure(self):
        return len(self.failed_features) > 0

    @property
    def failure(self) -> Optional[Exception]:
        for feature in self.failed_features:
            if feature.is_failure:
                return feature.failure

    @property
    def succinct_failure(self) -> Optional[str]:
        for feature in self.failed_features:
            if feature.is_failure:
                return feature.succinct_failure

    @property
    def first_scenario_result_error(self) -> Optional[FeatureResult]:
        for feature_result in self.errored_features:
            if feature_result.is_error:
                return feature_result.first_nonsuccessful_result

    @property
    def first_scenario_result_fail(self) -> Optional[FeatureResult]:
        for feature_result in self.failed_features:
            if feature_result.is_failure:
                return feature_result.first_nonsuccessful_result

    @property
    def first_nonsuccessful_result(self) -> Optional[FeatureResult]:
        return self.first_scenario_result_error or self.first_scenario_result_fail


def stripped(string):
    return collapse_path("\n".join(filter(bool, [s.strip() for s in string.splitlines()])))


def collapse_path(e: str):
    return e.replace(os.getenv("HOME"), "~")
