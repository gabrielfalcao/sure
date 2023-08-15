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
from sure.meta import get_reporter, MetaReporter, gather_reporter_names

__path__ = os.path.abspath(os.path.dirname(__file__))


class Reporter(object, metaclass=MetaReporter):
    """# Base class for implementing reporters.

    To create a reporter all you need is to inherit from this class
    and implement (optionally) the following methods:

    * [`on_start()`](@sure.reporter.Reporter.on_start)
    * [`on_feature(feature)`](@sure.reporter.Reporter.on_feature)
    * [`on_feature_done(feature, result)`](@sure.reporter.Reporter.on_feature_done)
    * [`on_scenario(test)`](@sure.reporter.Reporter.on_scenario)
    * [`on_scenario_done(test, result)`](@sure.reporter.Reporter.on_scenario_done)
    * [`on_failure(test, error)`](@sure.reporter.Reporter.on_failure)
    * [`on_error(test, error)`](@sure.reporter.Reporter.on_error)
    * [`on_success(test)`](@sure.reporter.Reporter.on_success)
    * [`on_finish()`](@sure.reporter.Reporter.on_finish)
    """
    __metaclass__ = MetaReporter
    name = None

    def __init__(self, runner):
        self.runner = runner
        self.successes = []
        self.failures = []
        self.errors = []

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

    def on_feature(self, feature):
        """### `def on_feature(feature)`

        Called when a test feature is about to run

        Example:
        ```python
        from sure.reporter import Reporter

        class FeatureReporter(Reporter):
            def on_feature(self, feature):
                steaymark.aka('Reporter.on_feature reported {}'.format(feature.name))

        class feature:
            name = 'a simple test feature'

        FeatureReporter('a <sure.runner.Runner()>').on_feature(feature)
        ```"""

    def on_feature_done(self, feature, result):
        """### `def on_feature_done(feature, result)`

        Called when a test feature_done is about to run

        Example:
        ```python
        from sure.reporter import Reporter

        class FeatureReporter(Reporter):
            def on_feature_done(self, feature):
                steaymark.aka('Reporter.on_feature_done reported {}'.format(feature.name))

        class feature_done:
            name = 'a simple test'

        Feature_doneReporter('a <sure.runner.Runner()>').on_feature_done(feature_done)
        ```"""

    def on_scenario(self, test, result):
        """### `def on_scenario_done(test, result)`

        Called when a test test_done is about to run

        Example:
        ```python
        from sure.reporter import Reporter

        class TestReporter(Reporter):
            def on_scenario_done(self, test):
                steaymark.aka('Reporter.on_scenario_done reported {}'.format(test.name))

        class test_done:
            name = 'a simple test'

        TestReporter('a <sure.runner.Runner()>').on_scenario_done(test_done)
        ```"""

    def on_scenario_done(self, test):
        """### `def on_scenario_done(test)`

        Called when a test test_done is about to run

        Example:
        ```python
        from sure.reporter import Reporter

        class TestReporter(Reporter):
            def on_scenario_done(self, test):
                steaymark.aka('Reporter.on_scenario_done reported {}'.format(test.name))

        class test_done:
            name = 'a simple test'

        TestReporter('a <sure.runner.Runner()>').on_scenario_done(test_done)
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

        found = get_reporter(name)
        if not found:
            raise RuntimeError(
                'no Reporter found for name {}, options are: {}'.format(
                    name,
                    ',\n'.join(gather_reporter_names())
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
        cls.importer.load_recursive(
            os.path.join(__path__, 'reporters'),
            ignore_errors=False,
        )
        return cls.from_name(name)(runner)
