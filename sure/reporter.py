#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2013>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from sure import importer
_registry = {}

__path__ = os.path.abspath(os.path.dirname(__file__))


class MetaReporter(type):
    def __init__(cls, name, bases, attrs):
        if cls.__module__ != __name__:
            _registry[cls.name] = cls

        super(MetaReporter, cls).__init__(name, bases, attrs)


class Reporter(object):
    """# Base class for implementing reporters.

    To create a reporter all you need is to inherit from this class
    and implement (optionally) the following methods:

    * [`on_start()`](@sure.reporter.Reporter.on_start)
    * [`on_suite(suite)`](@sure.reporter.Reporter.on_suite)
    * [`on_suite_done(suite, result)`](@sure.reporter.Reporter.on_suite_done)
    * [`on_test(test)`](@sure.reporter.Reporter.on_test)
    * [`on_test_done(test, result)`](@sure.reporter.Reporter.on_test_done)
    * [`on_failure(test, error)`](@sure.reporter.Reporter.on_failure)
    * [`on_error(test, error)`](@sure.reporter.Reporter.on_error)
    * [`on_success(test)`](@sure.reporter.Reporter.on_success)
    * [`on_finish()`](@sure.reporter.Reporter.on_finish)
    """
    __metaclass__ = MetaReporter
    name = None

    def __init__(self, runner):
        self.runner = runner

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def on_start(self):
        """### `def on_start()`

        Called as soon as sure starts running.

        Example:
        ```python
        from sure.reporter import Reporter

        class HelloReporter(Reporter):
            def on_start(self):
                steaymark.aka('Reporter.on_start works')

        HelloReporter('a <sure.runner.Runner()>').on_start()
        ```"""

    def on_suite(self, suite):
        """### `def on_suite(suite)`

        Called when a test suite is about to run

        Example:
        ```python
        from sure.reporter import Reporter

        class SuiteReporter(Reporter):
            def on_suite(self, suite):
                steaymark.aka('Reporter.on_suite reported {}'.format(suite.name))

        class suite:
            name = 'a simple test suite'

        SuiteReporter('a <sure.runner.Runner()>').on_suite(suite)
        ```"""

    def on_suite_done(self, suite, result):
        """### `def on_suite_done(suite, result)`

        Called when a test suite_done is about to run

        Example:
        ```python
        from sure.reporter import Reporter

        class SuiteReporter(Reporter):
            def on_suite_done(self, suite):
                steaymark.aka('Reporter.on_suite_done reported {}'.format(suite.name))

        class suite_done:
            name = 'a simple test'

        Suite_doneReporter('a <sure.runner.Runner()>').on_suite_done(suite_done)
        ```"""

    def on_test(self, test, result):
        """### `def on_test_done(test, result)`

        Called when a test test_done is about to run

        Example:
        ```python
        from sure.reporter import Reporter

        class TestReporter(Reporter):
            def on_test_done(self, test):
                steaymark.aka('Reporter.on_test_done reported {}'.format(test.name))

        class test_done:
            name = 'a simple test'

        Test_doneReporter('a <sure.runner.Runner()>').on_test_done(test_done)
        ```"""

    def on_test_done(self, test):
        """### `def on_test_done(test)`

        Called when a test test_done is about to run

        Example:
        ```python
        from sure.reporter import Reporter

        class TestReporter(Reporter):
            def on_test_done(self, test):
                steaymark.aka('Reporter.on_test_done reported {}'.format(test.name))

        class test_done:
            name = 'a simple test'

        Test_doneReporter('a <sure.runner.Runner()>').on_test_done(test_done)
        ```"""

    def on_failure(self, test, error):
        """### `def on_failure(test, error)`

        Called when a test fails without crashing

        Example:
        ```python
        from sure.reporter import Reporter

        class FailureReporter(Reporter):
            def on_failure(self, test):
                steaymark.aka('Reporter.on_failure reported {}'.format(test.name))

        class failure:
            name = 'a simple failure'

        FailureReporter('a <sure.runner.Runner()>').on_failure(failure)
        ```"""

    def on_success(self, test):
        """### `def on_success(test)`

        Called when a test passes

        Example:
        ```python
        from sure.reporter import Reporter

        class SuccessReporter(Reporter):
            def on_success(self, test):
                steaymark.aka('Reporter.on_success reported {}'.format(test.name))

        class success:
            name = 'a simple success'

        SuccessReporter('a <sure.runner.Runner()>').on_success(success)
        ```"""

    def on_error(self, test, error):
        """### `def on_error(test, error)`

        Called when a test fails with exception

        Example:
        ```python
        from sure.reporter import Reporter

        class ErrorReporter(Reporter):
            def on_error(self, test):
                steaymark.aka('Reporter.on_error reported {}'.format(test.name))

        class error:
            name = 'a simple error'

        ErrorReporter('a <sure.runner.Runner()>').on_error(error)
        ```"""

    def on_finish(self):
        """### `def on_finish()`

        Called as soon as sure finishes running.

        Example:
        ```python
        from sure.reporter import Reporter

        class HelloReporter(Reporter):
            def on_finish(self):
                steaymark.aka('Reporter.on_finish works')

        HelloReporter('a <sure.runner.Runner()>').on_finish()
        ```"""

    @classmethod
    def from_name(cls, name):
        """### `def from_name(name)`

        Finds a suitable Reporter class for the given name, after any
        `Reporter` subclasses with a `name` class attribute are registered
        and returned by this method.

        # Usage

        from sure.reporter import Reporter

        Reporter.from_name('spec')
        ```
        """

        found = _registry.get(name)
        if not found:
            raise RuntimeError(
                'no Reporter found for name {}, options are: {}'.format(
                    name,
                    ',\n'.join(_registry.keys())
                ))

        return found

    @classmethod
    def from_name_and_runner(cls, name, runner):
        """### `def from_name_and_runner(name, runner)`

        Shorthand for:
        ```python
        from sure.runner import Runner
        from sure.reporter import Reporter

        runner = Runner('/some/path')

        ReporterClass = Reporter.from_name('spec')
        reporter = ReporterClass(runner)

        ```

        Example usage:

        ```python
        reporter = Reporter.from_name_and_runner('spec', runner)
        ```"""
        importer.load_recursive(
            os.path.join(__path__, 'reporters'),
            ignore_errors=False,
        )
        return cls.from_name(name)(runner)
