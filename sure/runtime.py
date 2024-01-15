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
# along with this program. If not, see <http://www.gnu.org/licenses/>.
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
from typing import Dict, List, Optional, Any, Callable, Union
from mock import Mock

from sure.reporter import Reporter
from sure.errors import InternalRuntimeError
from sure.special import WarningReaper
from sure import types as stypes

from sure.errors import (
    exit_code,
    ExitError,
    ExitFailure,
    ImmediateError,
    ImmediateFailure,
    SpecialSyntaxDisabledError,
    ExceptionManager,
    treat_error,
    collapse_path,
    send_runtime_warning
)
from sure.loader import (
    loader,
    get_file_name,
    get_line_number,
    get_type_definition_filename_and_firstlineno,
    object_belongs_to_sure,
)

self = sys.modules[__name__]
log = logging.getLogger(__name__)


class BaseContainer(object):
    """base-class for runtime containers"""


class RuntimeRole:
    Setup = reduce(lambda L, R: L ^ R, b"Setup")
    Unit = reduce(lambda L, R: L ^ R, b"Unit")
    Teardown = reduce(lambda L, R: L ^ R, b"Teardown")


def inspect_constructor_arguments(cls: type) -> bool:
    signature = inspect.signature(cls)
    return signature.parameters


def is_class_initializable_without_params(cls: type) -> bool:
    if object_belongs_to_sure(cls) or not isinstance(cls, type):
        return False

    return len(inspect_constructor_arguments(cls)) == 0


def object_name(so: object) -> str:
    """
    :param so: stands for "some object" - a :class:`object` from which some kind of "name" - :class:`str` can be derived.
    :returns: string with the name of the object
    """
    if isinstance(so, type):
        return f"{so.__module__}.{so.__name__}"

    elif hasattr(so, "__name__"):
        return so.__name__

    return f"{so.__class__.__module__}.{so.__class__.__name__}"


def investigation_indicates_object_to_be_a_user_defined_class_instance(
    source: object,
) -> bool:
    return not object_belongs_to_sure(source) and all(
        map(lambda attr: hasattr(source, f"__{attr}__"), ("module", "class"))
    )


def seem_to_indicate_setup(name: str) -> bool:
    return bool(re.search(r"^(setUp|setup|set_up)$", name or ""))


def seem_to_indicate_teardown(name: str) -> bool:
    return bool(re.search(r"^(tearDown|teardown|tear_down)$", name or ""))


def seem_to_indicate_test(name: str) -> bool:
    return bool(re.search(r"^(Test|Spec|Scenario)[\w_]+$", name or "", re.I))


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


class RuntimeOptions(object):
    """Container for command-line options which originate at
    :mod:`sure.cli`. The goal is to isolate options specific to
    test-runtime into a hermetically sealed object which in its turn
    is kept and handled exclusively by each instance of
    :class:`sure.runtime.RuntimeContext` which in its turn is
    contextual to each executable test.

    .. note:: In the mid-to-long-term future :class:`sure.runtime.RuntimeOptions` class *might* also receive options provided by plugins.


    List of Options:

    - ``immediate`` - quit entire test-run session immediately after a failure
    - ``ignore`` - optional list of paths to be ignored
    - ``glob_pattern`` - optional string representing a valid :mod:`fnmatch` pattern to be matched against every "full" :class:`~pathlib.Path` in lookup paths of :meth:`~sure.runner.Runner.find_candidates` and :class:`~sure.loader.loader`. Defaults to ``**test*.py``
    - ``reap_warnings`` - optional bool to flag that warnings should be reaped, captured during runtime and displayed by the chosen reporter at the end of the test execution session. Defaults to ``False``
    """

    immediate: bool
    ignore: Optional[List[Union[str, Path]]]
    glob_pattern: str
    reap_warnings: bool

    def __init__(
        self,
        immediate: bool,
        ignore: Optional[List[Union[str, Path]]] = None,
        glob_pattern: str = "**test*.py",
        reap_warnings: bool = False
    ):
        self.immediate = bool(immediate)
        self.ignore = ignore and list(ignore) or []
        self.glob_pattern = glob_pattern
        self.reap_warnings = bool(reap_warnings)

    def __repr__(self):
        return f"<RuntimeOptions immediate={self.immediate} glob_pattern={repr(self.glob_pattern)} reap_warnings={repr(self.reap_warnings)}>"


class RuntimeContext(object):
    """Provides a runtime context for each executable test. Contains a
    reference to the instance of :class:`~sure.RuntimeOptions` given
    by a :class:`~sure.runner.Runner` as well as reference to the
    :class:`~sure.reporter.Reporter` chosen.
    """

    reporter: Reporter
    options: RuntimeOptions
    unittest_testcase_method_name: str

    def __init__(
        self,
        reporter: Reporter,
        options: RuntimeOptions,
        unittest_testcase_method_name: str = "runTest",
    ):
        self.reporter = reporter
        self.options = options
        self.unittest_testcase_method_name = unittest_testcase_method_name
        self.warning_reaper = WarningReaper()
        if options.reap_warnings:
            self.warning_reaper.enable_capture()

    def __repr__(self):
        return f"<RuntimeContext reporter={self.reporter} options={self.options}>"

    @property
    def warnings(self):
        return self.warning_reaper.warnings


class ErrorStack(object):
    def __init__(
        self, location: stypes.TestLocation, exc: Exception, exception_info=None
    ):
        self.exception_info = exception_info or sys.exc_info()
        self.traceback = self.exception_info[-1]
        self.exception = exc
        self.location = location
        self.code = exit_code(str(exc))

    def full(self) -> str:
        return "\n".join(
            [collapse_path(e) for e in traceback.format_tb(self.traceback)]
        )

    def location_specific_stack(self) -> List[str]:
        return [
            collapse_path(e)
            for e in traceback.format_tb(self.traceback)
            if self.location.name in e
        ]

    def location_specific_error(self) -> str:
        stack = self.location_specific_stack()
        return collapse_path(stack[-1])

    def nonlocation_specific_stack(self) -> List[str]:
        return [
            collapse_path(e)
            for e in traceback.format_tb(self.traceback)
            if self.location.name not in e
        ]

    def nonlocation_specific_error(self) -> List[str]:
        stack = self.nonlocation_specific_stack()
        return collapse_path(stack[-1])

    def __str__(self):
        return self.full()


class TestLocation(object):
    def __init__(self, test, module_or_instance=None):
        self.test = test

        if isinstance(test, (types.FunctionType, types.MethodType)):
            self.name = test.__name__
            self.filename = get_file_name(test)
            self.line = get_line_number(test)
            self.kind = test.__class__

        elif isinstance(test, unittest.TestCase):
            self.name = test.__class__.__name__
            self.filename, self.line = get_type_definition_filename_and_firstlineno(
                test.__class__
            )
            self.kind = unittest.TestCase

        elif isinstance(test, type):
            self.name = test.__name__
            self.filename, self.line = get_type_definition_filename_and_firstlineno(
                test
            )
            if issubclass(test, unittest.TestCase):
                self.kind = unittest.TestCase

        elif investigation_indicates_object_to_be_a_user_defined_class_instance(test):
            self.kind = test.__class__
            self.name = self.kind.__name__
            self.filename, self.line = get_type_definition_filename_and_firstlineno(
                test.__class__
            )

        else:
            raise TypeError(
                f"{test} of type {type(test)} is not supported by {TestLocation}"
            )

        self.description = getattr(self.test, "description", inspect.getdoc(self.test)) or ""
        if self.description == inspect.getdoc(unittest.TestCase):
            self.description = ""
        self.module_or_instance = module_or_instance
        self.ancestral_description = getattr(
            module_or_instance, "description", inspect.getdoc(module_or_instance)
        )

    def __repr__(self):
        test = " ".join([self.name, "at", self.path_and_lineno])
        return f"<TestLocation {test}>"

    def __str__(self):
        return "\n".join(
            [
                f'scenario "{self.description}" ',
                f"defined at {self.path_and_lineno}",
            ]
        )

    @property
    def path_and_lineno(self):
        return collapse_path(f"{self.filename}:{self.line}")


class Container(BaseContainer):
    module_or_instance: Optional[object]
    name: str
    runnable: callable
    location: stypes.TestLocation
    scenario: stypes.Scenario

    def __init__(
        self,
        name: str,
        runnable: Union[
            callable, unittest.TestCase, object
        ],  # TODO: think about enhanced interoperability with :func:`sure.scenario`
        scenario: stypes.Scenario,
        module_or_instance: Optional[object] = None,
    ):
        self.name = name
        self.runnable = runnable
        self.location = TestLocation(runnable)
        self.scenario = scenario
        self.module_or_instance = module_or_instance

    @property
    def unit(self):
        return self.runnable

    def __repr__(self):
        return (
            f"<Container of {repr(self.runnable)} at {self.location.path_and_lineno}>"
        )


class ScenarioArrangement(BaseContainer):
    """Thought with the goal of providing a hermetically isolated
    environment where the runtime context and associated reporters are
    kept in sync with potentially nested occurrences of scenarios

    Contains a setup/teardown and a list of runnable tests associated
    with a :class:`unittest.TestCase` along with a reference to the
    original instance and a runtime context.
    """

    source: Any
    context: RuntimeContext
    scenario: stypes.Scenario
    setup_methods: List[Callable]
    teardown_methods: List[Callable]
    test_methods: List[BaseContainer]
    nested_containers: List[BaseContainer]

    def __init__(
        self,
        source: Any,
        context: RuntimeContext,
        scenario: stypes.Scenario,
        setup_methods: List[Callable],
        teardown_methods: List[Callable],
        test_methods: List[Callable],
        nested_containers: List[BaseContainer],
    ):
        self.location = TestLocation(source)
        self.name = self.location.name
        self.error = None
        self.failure = None
        self.source_instance = source
        if isinstance(
            source, unittest.TestCase
        ):
            self.source_instance = source
        elif is_class_initializable_without_params(source):
            self.source_instance = source()
        elif isinstance(source, (types.FunctionType, types.MethodType)):
            test_methods.insert(
                0,
                Container(
                    name=source.__name__,
                    runnable=source,
                    module_or_instance=source.__module__,
                    scenario=scenario,
                ),
            )
            self.source_instance = source.__module__
        else:
            send_runtime_warning(
                f"ScenarioArrangement received unexpected type: {source} ({type(source)})",
            )

        self.log = logging.getLogger(self.location.path_and_lineno)
        self.context = context
        self.scenario = scenario
        self.setup_methods = setup_methods
        self.teardown_methods = teardown_methods
        self.test_methods = test_methods
        self.nested_containers = nested_containers
        self.runnable = any(map(lambda list: len(list) > 0, [self.test_methods, self.nested_containers]))

    @property
    def tests(self):
        return self.test_methods

    def __repr__(self):
        return f"<ScenarioArrangement:{self.name} {self.location}>"

    @classmethod
    def from_generic_object(
        cls, some_object, context: RuntimeContext, scenario: stypes.Scenario
    ) -> Optional[stypes.ScenarioArrangement]:
        test_methods = []
        setup_methods = []
        teardown_methods = []
        nested_containers = []

        if isinstance(some_object, type) and not object_belongs_to_sure(some_object):
            #     <unittest.TestCase.__init__>
            #   constructs instance of unittest.TestCase and filter out each instance_or_function
            if issubclass(some_object, unittest.TestCase):
                instance_or_function = some_object(
                    context.unittest_testcase_method_name
                )
            else:
                params_count = len(inspect_constructor_arguments(some_object))
                if params_count == 0:
                    instance_or_function = some_object()
                else:
                    return cls(
                        source=some_object,
                        context=context,
                        scenario=scenario,
                        setup_methods=[],
                        teardown_methods=[],
                        test_methods=[],
                        nested_containers=[],
                    )

        elif isinstance(some_object, types.FunctionType):
            instance_or_function = some_object
            # TODO: refactor :mod:`sure.runner` and
            # :mod:`sure.runtime` to provide a test function's
            # module as ``some_object`` so that setup and teardown
            # methods can be fetched from within the module's scope
            return cls(
                source=instance_or_function,
                context=context,
                scenario=scenario,
                setup_methods=[],
                teardown_methods=[],
                test_methods=[],
                nested_containers=[],
            )

        else:
            send_runtime_warning(
                f"ScenarioArrangement received unexpected type: {some_object} ({type(some_object)})",
            )
            return cls(
                source=some_object,
                context=context,
                scenario=scenario,
                setup_methods=[],
                teardown_methods=[],
                test_methods=[],
                nested_containers=[],
            )

        for name, runnable in inspect.getmembers(instance_or_function):
            if not appears_to_be_runnable(name):
                self.log.debug(f"ignoring {some_object}.{name}")
                continue

            if isinstance(runnable, type) and not issubclass(runnable, (types.FunctionType, types.MethodType)):
                module_or_instance = runnable.__module__
            elif isinstance(runnable, (types.ModuleType, unittest.TestCase, types.FunctionType, types.MethodType)) or is_class_initializable_without_params(runnable):
                module_or_instance = instance_or_function

            if isinstance(runnable, (types.FunctionType, types.MethodType)):
                if seem_to_indicate_setup(name):
                    setup_methods.append(
                        Container(
                            name=name,
                            runnable=runnable,
                            module_or_instance=module_or_instance,
                            scenario=scenario,
                        )
                    )
                elif seem_to_indicate_test(name):
                    test_methods.append(
                        Container(
                            name=name,
                            runnable=runnable,
                            module_or_instance=module_or_instance,
                            scenario=scenario,
                        )
                    )
                elif seem_to_indicate_teardown(name):
                    teardown_methods.append(
                        Container(
                            name=name,
                            runnable=runnable,
                            module_or_instance=module_or_instance,
                            scenario=scenario,
                        )
                    )
            elif is_class_initializable_without_params(runnable):
                nested_containers.append(
                    cls.from_generic_object(runnable, context, scenario=scenario)
                )

            else:
                send_runtime_warning(
                    f"ignoring {instance_or_function}.{name} for being a {type(some_object)}",
                )
                continue

        return cls(
            source=instance_or_function,
            context=context,
            scenario=scenario,
            setup_methods=setup_methods,
            teardown_methods=teardown_methods,
            test_methods=test_methods,
            nested_containers=nested_containers,
        )

    def uncollapse_nested(self) -> List[stypes.ScenarioArrangement]:
        """uncollapses nested instances of
        :class:`~sure.ScenarioArrangement` and returns
        flattened list of this type.
        """
        flattened = [self]
        for ptc in self.nested_containers:
            flattened.extend(ptc.uncollapse_nested())
        return flattened

    def run(self, context):
        for setup_container in self.setup_methods:
            yield self.invoke_contextualized(
                setup_container, context
            ), RuntimeRole.Setup

        for container in self.tests:
            if len(self.tests) > 1:
                context.reporter.on_scenario(container.scenario)
            for result, role in self.run_container(container, context):
                if len(self.tests) > 1:
                    context.reporter.on_scenario_done(container.scenario, result)
                yield result, role

        for teardown_container in self.teardown_methods:
            yield self.invoke_contextualized(
                teardown_container, context
            ), RuntimeRole.Teardown

    def run_container(self, container, context):
        result = self.invoke_contextualized(
            container=container,
            context=context,
        )
        if context.options.immediate:
            if result.error is not None:
                raise ImmediateError(result)

            if result.failure is not None:
                raise ImmediateFailure(result)

        yield result, RuntimeRole.Unit

    def invoke_contextualized(self, container, context):
        """Calls the unit of code within *container* - :attr:`~sure.runtime.Container.unit` - and returns a :class:`~sure.runtime.ScenarioResult`.

        If a python exception happens during that call then a
        distinction is made between :class:`AssertionError` or
        :class:`Exception` and forwarded to the
        :class:`~sure.runtime.ScenarioResult` as "failure" or
        "error", respectively.

        .. note:: The given :attr:`~sure.runtime.Container.unit` may optionally take one argument: ``context`` which may or may not be an instance of :class:`~sure.StagingArea`

        :param container: :class:`~sure.runtime.Container`
        :param context: :class:`~sure.runtime.RuntimeContext`
        :param name: :class:`str`
        :param location: :class:`~sure.runtime.TestLocation`
        """
        if not isinstance(container, BaseContainer):
            raise InternalRuntimeError(
                f"expected {container} to be an instance of BaseContainer in this instance"
            )

        try:
            return_value = container.unit()
            return ScenarioResult(
                self, container.location, context, return_value=return_value
            )

        except AssertionError as failure:
            return ScenarioResult(self, container.location, context, failure)

        except Exception as error:
            return ScenarioResult(self, container.location, context, error)


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

    def __repr__(self):
        if self.description:
            return f'<Feature "{self.description}" {self.name}>'
        else:
            return f'<Feature "{self.name}">'

    def read_scenarios(self, suts):
        self.scenarios = list(map((lambda e: Scenario(e, self)), suts))
        self.ready = True
        return self.scenarios

    def run(self, reporter: Reporter, runtime: RuntimeOptions) -> stypes.FeatureResult:
        results = []
        for scenario in self.scenarios:
            context = RuntimeContext(reporter, runtime)

            result = scenario.run(context)

            results.append(result)
            if result.is_failure:
                reporter.on_failure(scenario, result)
                if runtime.immediate:
                    raise ExitFailure(context, result)

            elif result.is_error:
                reporter.on_error(result.scenario, result)
                if runtime.immediate:
                    raise ExitError(context, result)

        return FeatureResult(results)


class Scenario(object):
    def __init__(self, class_or_callable, feature):
        self.name = class_or_callable.__name__
        self.log = logging.getLogger(self.name)
        self.description = stripped(class_or_callable.__doc__ or "")
        self.location = TestLocation(class_or_callable, feature)
        self.object = class_or_callable
        self.object_ancestor = None
        if isinstance(class_or_callable, type):
            if issubclass(class_or_callable, unittest.TestCase):
                self.object_ancestor = class_or_callable

        self.feature = feature

    def run(self, context: RuntimeContext):
        collectors = ScenarioArrangement.from_generic_object(
            self.object,
            context,
            self,
        ).uncollapse_nested()
        results = []
        for collector in collectors:
            collector_results = []
            context.reporter.on_scenario(collector.scenario)

            for result, role in collector.run(context):
                if role == RuntimeRole.Unit:
                    collector_results.append(result)
                elif not result.is_success:
                    if result.is_failure:
                        context.reporter.on_failure(result.scenario, result)
                        if context.options.immediate:
                            raise ExitFailure(context, result)

                    elif result.is_error:
                        context.reporter.on_error(result.scenario, result)
                        if context.options.immediate:
                            raise ExitError(context, result)

            context.reporter.on_scenario_done(
                collector.scenario, ScenarioResultSet(collector_results, context)
            )
            results.extend(collector_results)
        return ScenarioResultSet(results, context)


class BaseResult:
    """Base class for results of scenarios and features. Its entire
    purpose is to allow for distinguishing result-containing objects."""

    def __repr__(self):
        return repr(self.label.lower())


class ScenarioResult(BaseResult):
    scenario: Scenario
    error: Optional[Exception]
    failure: Optional[AssertionError]
    location: stypes.TestLocation

    def __init__(
        self,
        scenario,
        location: stypes.TestLocation,
        context: RuntimeContext,
        error=None,
        return_value=None,
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
            self.__error__ = treat_error(error, self.location)

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
    def stack(self) -> Optional[ErrorStack]:
        for scenario in self.errored_scenarios:
            return scenario.stack

    def __getattr__(self, attr):
        try:
            return self.__getattribute__(attr)
        except AttributeError:
            return getattr(self.scenario_results[-1], attr)

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
    def stack(self) -> Optional[ErrorStack]:
        for scenario in self.errored_scenarios:
            return scenario.stack

    def __getattr__(self, attr):
        try:
            return self.__getattribute__(attr)
        except AttributeError:
            return getattr(self.scenario_results[-1], attr)

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
    def stack(self) -> Optional[ErrorStack]:
        for feature in self.errored_features:
            return feature.stack

    def __getattr__(self, attr):
        try:
            return self.__getattribute__(attr)
        except AttributeError:
            return getattr(self.feature_results[-1], attr)

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
    return collapse_path(
        "\n".join(filter(bool, [s.strip() for s in string.splitlines()]))
    )
