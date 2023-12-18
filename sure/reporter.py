#!/usr/bin/env python3
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
from pathlib import Path
from typing import Dict
from sure.meta import MetaReporter, get_reporter, gather_reporter_names

__path__ = Path(__file__).absolute().parent


class Reporter(object, metaclass=MetaReporter):
    """Base class for reporters.

    The following non-optional methods should be implemented:

    * :py:meth:`~sure.reporter.Reporter.on_start`
    * :py:meth:`~sure.reporter.Reporter.on_feature`
    * :py:meth:`~sure.reporter.Reporter.on_feature_done`
    * :py:meth:`~sure.reporter.Reporter.on_scenario`
    * :py:meth:`~sure.reporter.Reporter.on_scenario_done`
    * :py:meth:`~sure.reporter.Reporter.on_feature`
    * :py:meth:`~sure.reporter.Reporter.on_feature_done`
    * :py:meth:`~sure.reporter.Reporter.on_failure`
    * :py:meth:`~sure.reporter.Reporter.on_error`
    * :py:meth:`~sure.reporter.Reporter.on_success`
    * :py:meth:`~sure.reporter.Reporter.on_finish`

    .. admonition:: The default reference reporter implementation is :py:class:`sure.reporters.feature.FeatureReporter`
    """

    __metaclass__ = MetaReporter
    name = None

    def __init__(self, runner, *args, **kw):
        self.runner = runner
        self.successes = []
        self.failures = []
        self.errors = []
        self.initialize(*args, **kw)

    def initialize(self, *args, **kw):
        pass

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    def on_start(self):
        """Called as soon as `sure' starts running.

        .. code:: python

           from sure.reporter import Reporter

           class FeatureReporter(Reporter):
               def on_start(self):
                   sys.stderr.write('Reporter.on_start works')

           FeatureReporter('a <sure.runner.Runner()>').on_start()
        """
        raise NotImplementedError

    def on_feature(self, feature):
        """Called when a scenario feature is about to run

        .. code:: python

           from sure.reporter import Reporter

           class FeatureReporter(Reporter):
               def on_feature(self, feature):
                   sys.stderr.write('Reporter.on_feature reported {}'.format(feature.name))

           class feature:
               name = 'a simple scenario feature'

           FeatureReporter('a <sure.runner.Runner()>').on_feature(feature)
        """
        raise NotImplementedError

    def on_feature_done(self, feature, result):
        """Called when a scenario feature_done is about to run

        .. code:: python

           from sure.reporter import Reporter

           class FeatureReporter(Reporter):
               def on_feature_done(self, feature):
                   sys.stderr.write('Reporter.on_feature_done reported {}'.format(feature.name))

           class feature_done:
               name = 'a simple scenario'

           FeatureReporter('a <sure.runner.Runner()>').on_feature_done(feature_done)
        """
        raise NotImplementedError

    def on_scenario(self, scenario, result):
        """Called when a scenario test_done is about to run

        .. code:: python

           from sure.reporter import Reporter

           class TestReporter(Reporter):
               def on_scenario_done(self, scenario):
                   sys.stderr.write('Reporter.on_scenario_done reported {}'.format(scenario.name))

           class test_done:
               name = 'a simple scenario'

           TestReporter('a <sure.runner.Runner()>').on_scenario_done(test_done)
        """
        raise NotImplementedError

    def on_scenario_done(self, scenario):
        """Called when a scenario test_done is about to run

        .. code:: python

           from sure.reporter import Reporter

           class TestReporter(Reporter):
               def on_scenario_done(self, scenario):
                   sys.stderr.write('Reporter.on_scenario_done reported {}'.format(scenario.name))

           class test_done:
               name = 'a simple scenario'

           TestReporter('a <sure.runner.Runner()>').on_scenario_done(test_done)
        """
        raise NotImplementedError

    def on_failure(self, scenario, error):
        """Called when a scenario fails without crashing

        .. code:: python

           from sure.reporter import Reporter

           class FailureReporter(Reporter):
               def on_failure(self, scenario, error):
                   sys.stderr.write('Reporter.on_failure reported {}'.format(scenario.name))

           class failure:
               name = 'a simple failure'

           FailureReporter('a <sure.runner.Runner()>').on_failure(failure)
        """
        raise NotImplementedError

    def on_success(self, scenario):
        """Called when a scenario passes

        .. code:: python

           from sure.reporter import Reporter

           class SuccessReporter(Reporter):
               def on_success(self, scenario):
                   sys.stderr.write('Reporter.on_success reported {}'.format(scenario.name))

           class success:
               name = 'a simple success'

           SuccessReporter('a <sure.runner.Runner()>').on_success(success)
        """
        raise NotImplementedError

    def on_error(self, scenario, error):
        """Called when a scenario fails with exception

        .. code:: python

           from sure.reporter import Reporter

           class ErrorReporter(Reporter):
               def on_error(self, scenario):
                   sys.stderr.write('Reporter.on_error reported {}'.format(scenario.name))

           class error:
               name = 'a simple error'

           ErrorReporter('a <sure.runner.Runner()>').on_error(error)
        """
        raise NotImplementedError

    def on_finish(self):
        """Called as soon as `sure' finishes running.

        .. code:: python

           from sure.reporter import Reporter

           class HelloReporter(Reporter):
           def on_finish(self):
               sys.stderr.write('Reporter.on_finish works')

           HelloReporter('a <sure.runner.Runner()>').on_finish()
        """
        raise NotImplementedError

    @classmethod
    def from_name(cls, name):
        """`def from_name(name)`

        Finds a suitable Reporter class for the given name, after any
        `Reporter` subclasses with a `name` class attribute are registered
        and returned by this method.

        # Usage

        from sure.reporter import Reporter

        Reporter.from_name('feature')
        ```
        """
        if not isinstance(name, str):
            raise TypeError(f'name should be a {str.__name__} but got the {type(name).__name__} {name} instead')

        found = get_reporter(name)
        if not found:
            raise RuntimeError(
                "no reporter found with name {}, options are: {}".format(
                    name, ", ".join(gather_reporter_names())
                )
            )

        return found

    @classmethod
    def from_name_and_runner(cls, name, runner):
        """
        .. code:: python

           from sure.runner import Runner
           from sure.reporter import Reporter

           runner = Runner('/some/path')

           ReporterClass = Reporter.from_name('feature')
           reporter = ReporterClass(runner)

        Example usage:

        .. code:: python

           reporter = Reporter.from_name_and_runner('feature', runner)
        """
        cls.importer.load_recursive(
            __path__.joinpath("reporters"),
            ignore_errors=False,
        )
        return cls.from_name(name)(runner)
