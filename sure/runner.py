#!/usr/bin/env python
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
import traceback
import unittest
from typing import List, Optional, Dict
from sure.errors import NonValidTest
from sure.importer import importer
from sure.reporter import Reporter
from mock import Mock


def stripped(string):
    return "\n".join(filter(bool, [s.strip() for s in string.splitlines()]))


def seem_to_indicate_test(name: str) -> bool:
    return re.search(r'^(Ensure|Test|Spec|Scenario)', name, re.I)


class RuntimeOptions(object):
    immediate: bool

    def __init__(self, immediate: bool):
        self.immediate = immediate

    def __repr__(self):
        return f'<RuntimeOptions immediate={self.immediate}>'


class SpecContext(object):
    reporter: Reporter
    runtime: RuntimeOptions

    def __init__(self, reporter: Reporter, runtime: RuntimeOptions):
        self.reporter = reporter
        self.runtime = runtime

    def __repr__(self):
        return f'<SpecContext reporter={self.reporter} runtime={self.runtime}>'


class BaseResult(object):
    def __init__(self, results):
        self.results = results

    def __nonzero__(self):
        return self.ok

    @property
    def ok(self):
        return len(set([x.is_error for x in self.results]).union(set([x.is_failure for x in self.results]))) == 0


class Feature(object):
    def __init__(self, module):
        name = getattr(module, 'suite_name', getattr(module, 'feature', getattr(module, 'name', module.__name__)))
        description = getattr(module, 'suite_description', getattr(module, 'description', ""))

        self.name = stripped(name)
        self.description = stripped(description)

        self.module = module
        self.ready = False
        self.scenarios = []

    def read_scenarios(self, executables):
        self.scenarios = list(map((lambda e: Scenario(e, self)), executables))
        self.ready = True
        return self.scenarios

    def run(self, reporter, runtime: RuntimeOptions):
        results = []
        for scenario in self.scenarios:
            context = SpecContext(reporter, runtime)

            reporter.on_scenario(scenario)
            self.run_predicates(context)

            result = scenario.run(context)

            self.run_complements(context)
            results.append(result)

            if result.is_failure:
                reporter.on_failure(scenario, result.failure)

            elif result.is_error:
                reporter.on_error(scenario, result.error)

            else:
                reporter.on_success(scenario)

            reporter.on_scenario_done(scenario, result)

        return FeatureResult(results)

    def run_predicates(self, context):
        pass

    def run_complements(self, context):
        pass


class ErrorStack(object):
    def __init__(self, exception_info):
        self.exception_info = exception_info
        self.traceback = traceback.format_exception(*exception_info)

    def printable(self):
        return "\n".join(self.traceback)


class Scenario(object):
    def __init__(self, class_or_callable, suite):
        fallback = class_or_callable.__name__

        self.description = stripped(class_or_callable.__doc__ or fallback)

        self.object = class_or_callable
        self.object_ancestor = None
        if isinstance(class_or_callable, type):
            if issubclass(class_or_callable, unittest.TestCase):
                self.object_ancestor = unittest.TestCase

        self.suite = suite
        self.fail_immediately = False

    def run_unittesttestcase(self, context):
        last_failure = None
        last_error = None
        for name in dir(self.object):
            if last_failure and context.runtime.immediate:
                # XXX: log
                break

            if last_error and context.runtime.immediate:
                # XXX: log
                break

            if not seem_to_indicate_test(name):
                # XXX: log
                continue

            member = getattr(self.object(name), name, None)
            if isinstance(member, types.MethodType) and seem_to_indicate_test(name):
                result = self.run_single_test(member, context)
                last_failure = result.failure
                last_error = result.error
                yield result

    def run_single_test(self, test, context):
        code = test.__code__
        varnames = set(code.co_varnames).intersection({'context'})
        argcount = len(varnames)
        try:
            if argcount == 0:
                test()
            elif argcount == 1:
                test(context)
            else:
                raise NonValidTest(f'it appears that the test function {self.object} takes more than one argument: {argcount}')

        except AssertionError as failure:
            return ScenarioResult(self, failure)
        except Exception:
            return ScenarioResult(self, ErrorStack(sys.exc_info()))

        return ScenarioResult(self)

    def run(self, context):
        if self.object_ancestor in (unittest.TestCase, ):
            return ScenarioResultSet(self.run_unittesttestcase(context))

        return self.run_single_test(self.object, context)


class Runner(object):
    u"""Manages I/O operations to find tests and execute them"""

    def __init__(self, base_path, reporter_name, plugin_paths=None, **kwargs):
        self.base_path = base_path
        self.reporter = self.get_reporter(reporter_name)

        for k in kwargs:
            setattr(self, k, kwargs.get(k))

    def __repr__(self):
        return u'<Runner: {} {}>'.format(self.base_path, self.reporter)

    def get_reporter(self, name):
        return Reporter.from_name_and_runner(name, self)

    def find_candidates(self, lookup_paths):
        candidate_modules = []
        for path in lookup_paths:
            modules = importer.load_recursive(
                path,
                glob_pattern='test*.py'
            )
            candidate_modules.extend(modules)

        return candidate_modules

    def is_runnable_test(self, item):
        if isinstance(item, type):
            if not issubclass(item, unittest.TestCase):
                return
            if item == unittest.TestCase:
                return

        elif not isinstance(item, types.FunctionType):
            return

        try:
            name = item.__name__
        except AttributeError:
            return
        else:
            return seem_to_indicate_test(name)

    def extract_members(self, candidate):
        all_members = [m[1] for m in inspect.getmembers(candidate)]
        members = list(filter(self.is_runnable_test, all_members))
        return candidate, members

    def load_features(self, lookup_paths):
        features = []
        cases = []
        candidates = self.find_candidates(lookup_paths)
        for module, executables in map(self.extract_members, candidates):
            feature = Feature(module)
            cases.extend(feature.read_scenarios(executables))
            features.append(feature)

        return features

    def run(self, lookup_paths, immediate: bool = False):
        results = []
        self.reporter.on_start()

        for feature in self.load_features(lookup_paths):
            self.reporter.on_feature(feature)
            runtime = RuntimeOptions(immediate=immediate)
            result = feature.run(self.reporter, runtime=runtime)

            results.append(result)
            self.reporter.on_feature_done(feature, result)

        self.reporter.on_finish()

        return FeatureResultSet(results)


class ScenarioResult(BaseResult):
    scenario: Scenario
    error: Optional[Exception]
    failure: Optional[AssertionError]

    def __init__(self, scenario, error=None):
        self.scenario = scenario
        self.__error__ = None
        self.__failure__ = None

        if isinstance(error, AssertionError):
            self.__failure__ = error
        else:
            self.__error__ = error

    def printable(self):
        if self.is_failure:
            return str(self.error)

        if callable(getattr(self.error, 'printable', None)):
            return self.error.printable()

        return ""

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


class ScenarioResultSet(ScenarioResult):
    error: Optional[ScenarioResult]
    failure: Optional[ScenarioResult]

    def __init__(self, scenario_results: List[ScenarioResult]):
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


class FeatureResult(BaseResult):
    scenario_results: ScenarioResultSet
    error: Optional[Exception]
    failure: Optional[AssertionError]

    def __init__(self, feature, error=None):
        self.feature = feature
        self.__error__ = None
        self.__failure__ = None

        if isinstance(error, AssertionError):
            self.__failure__ = error
        else:
            self.__error__ = error

    def printable(self):
        if self.is_failure:
            return str(self.error)

        if callable(getattr(self.error, 'printable', None)):
            return self.error.printable()

        return ""

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


class FeatureResultSet(FeatureResult):
    error: Optional[FeatureResult]
    failure: Optional[FeatureResult]

    def __init__(self, feature_results: List[FeatureResult]):
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
                return feature.error

    @property
    def is_failure(self):
        return len(self.failed_features) > 0

    @property
    def failure(self) -> Optional[Exception]:
        for feature in self.failed_features:
            if feature.is_failure:
                return feature.failure
