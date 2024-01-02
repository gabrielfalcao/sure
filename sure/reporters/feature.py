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

from couleur import Shell

from sure.errors import ImmediateFailure, InternalRuntimeError, SpecialSyntaxDisabledError
from sure.reporter import Reporter
from sure.runtime import ScenarioResult

sh = Shell()

checkmark = "✓"
ballot = "✗"


class FeatureReporter(Reporter):
    """Test Reporter inspired by the output of Behaviour-driven-development tools du jour"""
    name = "feature"

    def on_start(self):
        self.indentation = 0
        sh.reset("\n")

    def on_feature(self, feature):
        self.indentation += 2
        sh.reset(" " * self.indentation)
        sh.bold_blue("Feature: ")
        sh.yellow("'")
        sh.green(feature.name)
        sh.yellow("'")
        sh.reset(" ")

    def on_feature_done(self, feature, result):
        sh.reset("\n\n")
        self.indentation = 0

    def on_scenario(self, test):
        if test in self.tests_started:
            return
        self.tests_started.append(test)
        self.indentation += 2
        sh.reset(" " * self.indentation)
        if test.description:
            sh.bold_green(f"\n{' ' * self.indentation} Scenario: ")
            sh.normal(test.description)
        else:
            self.indentation += 2
            sh.green(f"\n{' ' * self.indentation} Variant: ")
            sh.normal(test.name)
        sh.reset(" ")

    def on_scenario_done(self, test, result):
        if test in self.tests_finished:
            return
        self.indentation -= 2
        if not test.description:
            self.indentation -= 2

        if result.is_success:
            self.on_success(test)
        self.tests_finished.append(test)

    def on_failure(self, test, result):
        self.failures.append(test)
        self.indentation += 2
        sh.reset("\n")
        sh.reset(" " * self.indentation)
        self.indentation += 2
        if not result.failure:
            raise RuntimeError(
                f"{self.__class__}.on_failure() called with a {ScenarioResult} which does not contain a failure"
            )
        sh.yellow(f"Failure: {result.failure}\n{result.succinct_failure}")
        sh.reset(" " * self.indentation)
        if result.location.description.strip():
            sh.bold_blue(f"\n{' ' * self.indentation} Scenario:")
            sh.bold_blue(f"\n{' ' * self.indentation}     {result.location.description}")
        if result.location:
            sh.bold_red(f"\n{' ' * self.indentation} outer location {result.location.ort}")
        sh.reset("\n")
        self.indentation -= 4

    def on_success(self, test):
        self.successes.append(test)
        sh.bold_green(checkmark)
        sh.reset("")

    def on_error(self, test, result):
        self.errors.append(test)
        self.failures.append(test)
        self.indentation += 2
        sh.reset("\n")
        sh.bold_red(f"Error {repr(result.error)}\n")
        sh.bold_red(f"{result.stack.full()}")
        sh.reset(" " * self.indentation)
        sh.reset("\n")
        sh.bold_red(f"{result.location.ort}\n")
        self.indentation -= 2

    def on_internal_runtime_error(self, context, error):
        if isinstance(error.exception, SpecialSyntaxDisabledError):
            global sh
            sh.bold_yellow(f"\n{' ' * self.indentation} {error.exception}")
        else:
            sh = Shell()
            sh.bold_yellow("Internal Runtime Error\n")
            sh.bold_red(error.traceback)
        raise SystemExit(error.code)

    def on_finish(self):
        failed = len(self.failures)
        errors = len(self.errors)
        successful = len(self.successes)
        self.indentation -= 2
        sh.reset(" " * self.indentation)

        if failed:
            sh.yellow(f"{failed} failed")
            sh.reset("\n")
        if errors:
            sh.red(f"{errors} errors")
            sh.reset("\n")
        if successful:
            sh.green(f"{successful} successful")
            sh.reset("\n")
        sh.reset(" ")
