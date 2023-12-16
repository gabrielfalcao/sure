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
from __future__ import unicode_literals
import sys
from functools import reduce


class NonValidTest(Exception):
    """raised when a non-compatible test appears within the test-run session"""


def xor(lhs, rhs):
    return lhs ^ rhs


def exit_code(codeword: str) -> int:
    return reduce(xor, list(map(ord, codeword)))


class ImmediateAbort(Exception):
    """base-exception to immediate runtime abortion"""
    def __init__(self, code):
        sys.stderr.write(f"IMMEDIATE ABORT [{code}]")
        sys.exit(code)


class RuntimeInterruption(Exception):
    def __init__(self, scenario_result):
        self.result = scenario_result
        self.scenario = scenario_result.scenario
        self.context = scenario_result.context
        super().__init__(f"{self.result}")


class ImmediateError(RuntimeInterruption):
    def __init__(self, scenario_result):
        self.args = scenario_result.error.args
        self.message = "".join(self.args)
        super().__init__(scenario_result)


class ImmediateFailure(RuntimeInterruption):
    def __init__(self, scenario_result):
        self.args = scenario_result.failure.args
        self.message = self.result.succinct_failure
        super().__init__(scenario_result)


class ExitError(ImmediateAbort):
    def __init__(self, context, result):
        context.reporter.on_errorure(result.errored_features[0].errored_scenarios[0], result.succinct_error)
        return super().__init__(exit_code('ERROR'))


class ExitFailure(ImmediateAbort):
    def __init__(self, context, result):
        context.reporter.on_failure(result.failed_features[0].failed_scenarios[0], result.succinct_failure)
        return super().__init__(exit_code('FAILURE'))
