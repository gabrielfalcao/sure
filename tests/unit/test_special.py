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
import io
import sys
import warnings
from datetime import datetime
from unittest.mock import patch
from sure import expects
from sure.loader import collapse_path
from sure.doubles.dummies import anything, Dummy, anything_of_type
from sure.special import (
    determine_python_implementation,
    runtime_is_cpython,
    get_py_ssize_t,
    noop_patchable_builtin,
    craft_patchable_builtin,
    load_ctypes,
    WarningReaper,
)
description = "tests for :class:`sure.special`"


@patch("sure.special.load_ctypes")
def test_get_py_ssize_t_64(load_ctypes_mock):
    "sure.special.get_py_ssize_t() in 64 bits platform"

    ctypes = load_ctypes_mock.return_value
    ctypes.pythonapi.Py_InitModule4_64 = anything
    ctypes.c_int64 = Dummy("ctypes.c_int64")
    expects(get_py_ssize_t()).to.equal(ctypes.c_int64)


@patch("sure.special.load_ctypes")
def test_runtime_is_cpython_without_ctypes(load_ctypes_mock):
    "sure.special.runtime_is_cpython() returns False when :mod:`ctypes` is not available"

    load_ctypes_mock.return_value = None
    expects(runtime_is_cpython()).to.equal(False)


def test_noop_patchable_builtin():
    "sure.special.noop_patchable_builtin() returns performs no action"
    expects(noop_patchable_builtin()).to.be.none


@patch("sure.special.runtime_is_cpython")
def test_craft_patchable_builtin_noop(runtime_is_cpython):
    "sure.special.craft_patchable_builtin() returns noop_patchable_builtin when runtime is not cpython"

    runtime_is_cpython.return_value = False
    expects(craft_patchable_builtin()).to.equal(noop_patchable_builtin)


@patch.dict(sys.modules, ctypes=None)
def test_load_ctypes_unavailable():
    "sure.special.load_ctypes() returns None when ctypes cannot be imported"

    expects(load_ctypes()).to.equal(None)


def test_warning_reaper():
    "sure.special.WarningReaper should (toggle-) feature an interface to capture warnings"

    warning_reaper = WarningReaper().enable_capture()
    warning_reaper.clear()
    warnings.showwarning("test", ResourceWarning, filename=__file__, lineno=81)

    warning_reaper.warnings.should.equal([{"message": "test", "category": ResourceWarning, "filename": __file__, "lineno": 81, "occurrence": anything_of_type(datetime), "line": None, "file": None}])
