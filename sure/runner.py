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
from typing import Optional
from sure.errors import NonValidTest
from sure.importer import importer
from sure.reporter import Reporter
from mock import Mock


def stripped(string):
    return "\n".join(filter(bool, [s.strip() for s in string.splitlines()]))


class SpecContext(object):
    reporter: Reporter
    current_test: Optional[object]

    def __init__(self, reporter):
        self.reporter = reporter
        self.current_test = None

    def set_current_test(self, test):
        self.current_test = test


class BaseResult(object):
    def __init__(self, results):
        self.results = results

    def __nonzero__(self):
        return self.ok

    @property
    def ok(self):
        return all([x.ok for x in self.results])


class ScenarioResult(BaseResult):
    def __init__(self, case, error=None):
        self.case = case
        self.error = error

    def printable(self):
        if self.is_error:
            return self.error.printable()
        elif self.is_failure:
            return str(self.error)
        else:
            return ""

    @property
    def is_error(self):
        return isinstance(self.error, ErrorStack)

    @property
    def is_failure(self):
        return isinstance(self.error, AssertionError)

    @property
    def is_success(self):
        return self.error is None

    @property
    def ok(self):
        return self.is_success


class TestSuiteResult(BaseResult):
    pass


class FinalTestSuiteResult(BaseResult):
    pass


class Feature(object):
    def __init__(self, module):
        name = getattr(module, 'suite_name', getattr(module, 'feature', getattr(module, 'name', module.__name__)))
        description = getattr(module, 'suite_description', getattr(module, 'description', ""))

        self.name = stripped(name)
        self.description = stripped(description)

        self.module = module
        self.ready = False
        self.testcases = []

    def read_scenarios(self, executables):
        self.testcases = list(map((lambda e: Scenario(e, self)), executables))
        self.ready = True
        return self.testcases

    def run(self, reporter):
        results = []
        for case in self.testcases:
            context = SpecContext(reporter)

            reporter.on_test(case)
            self.run_predicates(context)

            result = case.run(context)

            self.run_complements(context)
            results.append(result)

            if result.is_error:
                reporter.on_error(case, result)

            elif result.is_failure:
                reporter.on_failure(case, result)

            else:
                reporter.on_success(case)

            reporter.on_test_done(case, result)

        return TestSuiteResult(results)

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
        if isinstance(class_or_callable, type):
            if issubclass(class_or_callable, unittest.TestCase):
                self.object = class_or_callable()

        self.suite = suite

    def run_unittesttestcase(self, context):
        for name, member in inspect.getmembers(self.object):
            if isinstance(member, types.MethodType):
                # XXX: log debug else
                self.run_single_test(member, context)

    def run_single_test(self, test, context):
        argcount = test.__code__.co_argcount
        try:
            if argcount == 0:
                test()
            elif argcount == 1:
                test(context)
            else:
                raise RuntimeError(f'it appears that the test function {self.object} takes more than one argument')

        except AssertionError as failure:
            return ScenarioResult(self, failure)
        except Exception:
            return ScenarioResult(self, ErrorStack(sys.exc_info()))

        return ScenarioResult(self)

    def run(self, context):
        if isinstance(self.object, unittest.TestCase):
            return self.run_unittesttestcase(context)

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
            return re.search(r'(^Ensure|^Test|^Spec|Spec$|Test$)', name, re.I)

    def extract_members(self, candidate):
        all_members = [m[1] for m in inspect.getmembers(candidate)]
        members = list(filter(self.is_runnable_test, all_members))
        return candidate, members

    def load_suites(self, lookup_paths):
        suites = []
        cases = []
        candidates = self.find_candidates(lookup_paths)
        for module, executables in map(self.extract_members, candidates):
            suite = Feature(module)
            cases.extend(suite.read_scenarios(executables))
            suites.append(suite)

        return suites

    def run(self, lookup_paths):
        results = []
        self.reporter.on_start()

        for suite in self.load_suites(lookup_paths):
            self.reporter.on_suite(suite)
            result = suite.run(self.reporter)
            results.append(result)
            self.reporter.on_suite_done(suite, result)

        self.reporter.on_finish()

        return FinalTestSuiteResult(results)
