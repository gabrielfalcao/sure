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
from couleur import Shell

import sure
from typing import Set
from sure.agents import Agent
from sure.reporter import Reporter


sh = Shell()


class CoReporter(Reporter):
    name = '__meta__'

    def __init__(self, runner, liaison_with: Set[Reporter]):
        for possible_liaison in liaison_with:
            if not isinstance(possible_liaison, Reporter):
                raise TypeError(f'CoReporter takes a set of reporters to broadcast data to')

        self.liaisons = liaison_with
        super().__init__(runner)

    def on_start(self):
        self.indentation = 0
        # sh.white("Running sure version ")
        # sh.yellow(sure.version)
        sh.reset("\n")

    def on_feature(self, feature):
        self.indentation += 2

        sh.reset(" " * self.indentation)
        sh.blue("Feature: ")
        sh.yellow("'")
        sh.green(feature.name)
        sh.yellow("'")
        sh.reset("\n")

    def on_feature_done(self, feature, result):
        # sh.reset(" " * self.indentation)
        # sh.white("[")
        # sh.normal(feature.name)
        # sh.white("]")
        # sh.white(checkmark)
        sh.reset("\n\n")
        self.indentation = 0

    def on_scenario(self, test):
        self.indentation += 2
        sh.reset(" " * self.indentation)
        sh.green("Scenario: ")
        sh.normal(test.description)
        sh.reset(" ")

    def on_scenario_done(self, test, result):
        self.indentation -= 2

    def on_failure(self, test, error):
        self.failures.append(test)
        self.indentation += 2
        sh.red(ballot)
        sh.reset("\n")
        sh.reset(" " * self.indentation)
        sh.red(str(error))
        sh.reset("\n")
        self.indentation -= 2

    def on_success(self, test):
        self.successes.append(test)
        sh.green(checkmark)
        sh.reset("\n")

    def on_error(self, test, error):
        self.errors.append(test)
        self.failures.append(test)
        self.indentation += 2
        sh.yellow(ballot)
        sh.reset("\n")
        sh.reset(" " * self.indentation)
        sh.yellow(error.printable())
        sh.reset("\n")
        self.indentation -= 2

    def on_finish(self):
        failed = len(self.failures)
        errors = len(self.errors)
        successful = len(self.successes)
        self.indentation -= 2
        sh.reset(" " * self.indentation)

        if failed:
            sh.red(f"{failed} failed")
            sh.reset("\n")
        if errors:
            sh.yellow(f"{errors} errors")
            sh.reset("\n")
        if successful:
            sh.green(f"{successful} successful")
            sh.reset("\n")
        sh.reset(" ")
