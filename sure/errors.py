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
import os
import re
import sys
import inspect
import traceback
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from functools import reduce
from sure import registry
from sure.types import TestLocation, ScenarioResult, RuntimeContext


__sure_package_path__ = str(Path(__file__).parent)


def collapse_path(e: Union[str, Path]) -> str:
    return str(e).replace(os.getenv("HOME"), "~")


def send_runtime_warning(message: str):
    caller = CallerLocation.most_recent()
    warnings.showwarning(message, RuntimeWarning, filename=caller.filename, lineno=caller.lineno)


def get_stack_frames():
    return list(
        filter(
            lambda sf: not sf.filename.startswith(__sure_package_path__),
            traceback.extract_stack(inspect.currentframe()),
        )
    )


def get_most_recent_call_frame() -> traceback.FrameSummary:
    stack = get_stack_frames()
    return stack[-1]


def treat_error(error: Exception, location: Optional[TestLocation] = None) -> Exception:
    manager = ExceptionManager(error, location)
    return manager.perform_handoff()


def xor(lhs, rhs):
    return lhs ^ rhs


def exit_code(codeword: str) -> int:
    return reduce(xor, list(map(ord, codeword)))


class BaseSureError(Exception):
    def __init__(self, message):
        self.message = str(message)
        super().__init__(message)

    def __str__(self):
        return getattr(self, 'message', self.__class__.__name__)

    def __repr__(self):
        return getattr(self, 'message', self.__class__.__name__)


class FileSystemError(IOError):
    """IOError specific for occurrences within :mod:`sure`'s runtime"""


class ImmediateExit(BaseSureError):
    """base-exception to immediate runtime abortion"""

    def __init__(self, code):
        sys.exit(code)


class RuntimeInterruption(BaseSureError):
    def __init__(self, scenario_result: ScenarioResult):
        self.result = scenario_result
        self.scenario = scenario_result.scenario
        self.context = scenario_result.context
        super().__init__(f"{self.result}")


class ImmediateError(RuntimeInterruption):
    def __init__(self, scenario_result: ScenarioResult):
        super().__init__(scenario_result)
        self.args = scenario_result.error.args
        self.message = "".join(self.args)


class ImmediateFailure(RuntimeInterruption):
    def __init__(self, scenario_result: ScenarioResult):
        super().__init__(scenario_result)
        self.args = scenario_result.failure.args
        self.message = scenario_result.succinct_failure


class ExitError(ImmediateExit):
    def __init__(self, context: RuntimeContext, result: ScenarioResult):
        context.reporter.on_error(context, result)
        return super().__init__(exit_code("ERROR"))


class ExitFailure(ImmediateExit):
    def __init__(self, context: RuntimeContext, result: ScenarioResult):
        return super().__init__(exit_code("FAILURE"))


class InternalRuntimeError(BaseSureError):
    def __init__(self, context, exception: Exception):
        self.traceback = traceback.format_exc()
        self.exception = exception
        self.code = exit_code(self.traceback)
        self.context = context
        super().__init__(f"InternalRuntimeError: {exception}")
        context.reporter.on_internal_runtime_error(context, self)


class WrongUsageError(BaseSureError):
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
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"{message}")


class CallerLocation(object):
    def __init__(self, name: str, filename: str, lineno: int, display_info: str):
        self.name = name
        self.filename = filename
        self.lineno = lineno
        self.display_info = display_info

    @classmethod
    def most_recent(cls):
        summary = get_most_recent_call_frame()
        return cls(
            name=summary.name,
            filename=summary.filename,
            lineno=summary.lineno,
            display_info=summary.line,
        )

    @property
    def path_and_lineno(self):
        return collapse_path(f"{self.filename}:{self.lineno}")

    def __repr__(self):
        return f"<CallerLocation:{self.name} {self.path_and_lineno}>"

    def __str__(self):
        return f"{self.display_info} called within {self.name} defined at {self.path_and_lineno}>"


class ExceptionManager(object):
    """Designed for use at strategic locations of exception handling
    within :mod:`sure` and possibly in system exception hooks as well.

    Transforms builtin python errors into :mod:`sure`-specific
    exceptions based heuristics performed on methods prefixed with
    ``handle_`` returning the original error otherwise.
    """

    def __init__(self, exc: Exception, test_location: Optional[TestLocation] = None):
        self.info = sys.exc_info()
        if test_location is None:
            test_location = CallerLocation.most_recent()

        self.test_location = test_location
        self.exc = exc

    def handle_special_syntax_disabled(self) -> Exception:
        if not isinstance(self.exc, AttributeError):
            return self.exc

        has_potential = re.search(
            r"^'(?P<object_type>[^']+)' object has no attribute '(?P<attribute>[a-zA-Z][a-zA-Z0-9_]+)'",
            str(self.exc),
        )
        if not has_potential:
            return self.exc

        attribute_name = has_potential.group("attribute")
        object_type = has_potential.group("object_type")
        if attribute_name in registry.KNOWN_ASSERTIONS:
            return SpecialSyntaxDisabledError(
                f"{self.test_location.path_and_lineno}\nattempt to access special syntax attribute `{attribute_name}' with a `{object_type}' "
                f"without explicitly enabling Sure's special syntax\n"
            )

        return self.exc

    def perform_handoff(self) -> Exception:
        queue = [
            self.handle_special_syntax_disabled,
        ]
        for method in queue:
            val = method()
            if val != self.exc:
                return val

        return self.exc
