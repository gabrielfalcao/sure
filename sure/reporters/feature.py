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
from sure.reporter import Reporter


sh = Shell()

checkmark = '✓'
ballot = '✗'


class FeatureReporter(Reporter):
    name = 'feature'

    def on_start(self):
        self.indentation = 0
        # sh.white("Running sure version ")
        # sh.yellow(sure.version)
        sh.reset("\n")

    def on_suite(self, suite):
        self.indentation += 2

        sh.reset(" " * self.indentation)
        sh.blue("Feature: ")
        sh.yellow("'")
        sh.green(suite.name)
        sh.yellow("'")
        sh.reset("\n")

    def on_suite_done(self, suite, result):
        # sh.reset(" " * self.indentation)
        # sh.white("[")
        # sh.normal(suite.name)
        # sh.white("]")
        # sh.white(checkmark)
        sh.reset("\n\n")
        self.indentation = 0

    def on_test(self, test):
        self.indentation += 2
        sh.reset(" " * self.indentation)
        sh.green("Scenario: ")
        sh.normal(test.description)
        sh.reset(" ")

    def on_test_done(self, test, result):
        self.indentation -= 2

    def on_failure(self, test, error):
        sh.bold_red(ballot)
        sh.reset("\n")
        sh.red(error.printable())
        sh.reset("\n")

    def on_success(self, test):
        sh.bold_green(checkmark)
        sh.reset("\n")

    def on_error(self, test, error):
        self.on_failure(test, error)

    def on_finish(self):
        pass
