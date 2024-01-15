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
import sys, unittest, types
from os.path import isdir
from sure import expects
from collections import OrderedDict
from sure.loader import collapse_path, loader
from sure.runtime import object_name
from sure.runtime import seem_to_indicate_setup
from sure.runtime import seem_to_indicate_teardown
from sure.runtime import seem_to_indicate_test
from sure.runtime import appears_to_be_runnable
from sure.runtime import TestLocation
from sure.runtime import ErrorStack
from sure.runtime import RuntimeContext
from sure.runtime import RuntimeOptions
from sure.runtime import BaseResult
from sure.runtime import Container
from sure.runtime import ScenarioArrangement
from sure.runtime import Feature
from sure.runtime import Scenario
from sure.runtime import ExceptionManager
from sure.runtime import treat_error
from sure.runtime import ScenarioResult
from sure.runtime import ScenarioResultSet
from sure.runtime import FeatureResult
from sure.runtime import FeatureResultSet
from sure.runtime import stripped


loader.load_module(__file__)
description = "tests for :class:`sure.runtime.ErrorStack`"


def test_error_stack_assertion_error_location_specific_stack_traceback():
    """sure.runtime.ErrorStack.location_specific_stack()"""

    def synthesize_error_stack():
        try:
            try:
                raise ValueError("error 1")
            except Exception:
                raise ValueError("error 2")
        except Exception as e:
            return e, sys.exc_info()

    error, info = synthesize_error_stack()
    location = TestLocation(
        synthesize_error_stack,
        sys.modules[__name__]
    )
    stack = ErrorStack(location, error, info)
    expects(stack.location_specific_stack()).to.equal([
        f'  File "{collapse_path(__file__)}", line 57, in synthesize_error_stack\n    raise ValueError("error 2")\n'
    ])
    expects(stack.full()).to.equal(f'  File "{collapse_path(__file__)}", line 57, in synthesize_error_stack\n    raise ValueError("error 2")\n')
    expects(str(stack)).to.equal(f'  File "{collapse_path(__file__)}", line 57, in synthesize_error_stack\n    raise ValueError("error 2")\n')


def test_error_stack_assertion_error_nonlocation_specific_stack_traceback():
    """sure.runtime.ErrorStack.nonlocation_specific_stack()"""

    def synthesize_error_stack():
        try:
            try:
                raise ValueError("error 1")
            except Exception:
                raise ValueError("error 2")
        except Exception as e:
            return e, sys.exc_info()

    error, info = synthesize_error_stack()
    location = TestLocation(
        test_error_stack_assertion_error_nonlocation_specific_stack_traceback,
        sys.modules[__name__]
    )
    stack = ErrorStack(location, error, info)
    expects(stack.nonlocation_specific_stack()).to.equal([
        f'  File "{collapse_path(__file__)}", line 82, in synthesize_error_stack\n    raise ValueError("error 2")\n'
    ])
    expects(stack.full()).to.equal(f'  File "{collapse_path(__file__)}", line 82, in synthesize_error_stack\n    raise ValueError("error 2")\n')
    expects(str(stack)).to.equal(f'  File "{collapse_path(__file__)}", line 82, in synthesize_error_stack\n    raise ValueError("error 2")\n')


def test_error_stack_assertion_error_location_specific_error_traceback():
    """sure.runtime.ErrorStack.location_specific_error()"""

    def synthesize_error_stack():
        try:
            try:
                raise RuntimeError("error 1")
            except Exception:
                raise RuntimeError("error 2")
        except Exception as e:
            return e, sys.exc_info()

    error, info = synthesize_error_stack()
    location = TestLocation(
        synthesize_error_stack,
        sys.modules[__name__]
    )
    stack = ErrorStack(location, error, info)
    expects(stack.location_specific_error()).to.equal(
        f'  File "{collapse_path(__file__)}", line 107, in synthesize_error_stack\n    raise RuntimeError("error 2")\n'
    )
    expects(stack.full()).to.equal(f'  File "{collapse_path(__file__)}", line 107, in synthesize_error_stack\n    raise RuntimeError("error 2")\n')
    expects(str(stack)).to.equal(f'  File "{collapse_path(__file__)}", line 107, in synthesize_error_stack\n    raise RuntimeError("error 2")\n')


def test_error_stack_assertion_error_nonlocation_specific_error_traceback():
    """sure.runtime.ErrorStack.nonlocation_specific_error()"""

    def synthesize_error_stack():
        try:
            try:
                raise RuntimeError("error 1")
            except Exception:
                raise RuntimeError("error 2")
        except Exception as e:
            return e, sys.exc_info()

    error, info = synthesize_error_stack()
    location = TestLocation(
        test_error_stack_assertion_error_nonlocation_specific_error_traceback,
        sys.modules[__name__]
    )
    stack = ErrorStack(location, error, info)
    expects(stack.nonlocation_specific_error()).to.equal(
        f'  File "{collapse_path(__file__)}", line 132, in synthesize_error_stack\n    raise RuntimeError("error 2")\n'
    )
    expects(stack.full()).to.equal(f'  File "{collapse_path(__file__)}", line 132, in synthesize_error_stack\n    raise RuntimeError("error 2")\n')
    expects(str(stack)).to.equal(f'  File "{collapse_path(__file__)}", line 132, in synthesize_error_stack\n    raise RuntimeError("error 2")\n')
