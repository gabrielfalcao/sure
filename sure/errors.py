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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import traceback
from functools import reduce


def xor(lhs, rhs):
    return lhs ^ rhs


def exit_code(codeword: str) -> int:
    return reduce(xor, list(map(ord, codeword)))


class FileSystemError(IOError):
    """IOError specific for occurrences within :mod:`sure`'s runtime"""


class ImmediateExit(Exception):
    """base-exception to immediate runtime abortion"""
    def __init__(self, code):
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
        self.message = scenario_result.succinct_failure
        super().__init__(scenario_result)


class ExitError(ImmediateExit):
    def __init__(self, context, result):
        context.reporter.on_error(context, result)
        return super().__init__(exit_code('ERROR'))


class ExitFailure(ImmediateExit):
    def __init__(self, context, result):
        return super().__init__(exit_code('FAILURE'))


class InternalRuntimeError(Exception):
    def __init__(self, context, exception: Exception):
        self.traceback = traceback.format_exc()
        self.exception = exception
        self.code = exit_code(self.traceback)
        super().__init__(self.traceback)
        context.reporter.on_internal_runtime_error(context, self)


class WrongUsageError(Exception):
    """raised when :class:`~sure.AssertionBuilder` is used
    incorrectly, such as passing a value of the wrong type as argument
    to an assertion method or as source of comparison.

    This exception should be clearly indicated by reporters so that
    the offending action can be understood and corrected quickly.
    """


class SpecialSyntaxDisabledError(Exception):
    """raised when a :class:`AttributeError` occurs and the traceback
    contains evidence indicating that the probable cause is an attempt
    to employ the special syntax when such behavior is not permitted
    """
