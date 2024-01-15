# -*- coding: utf-8 -*-
# <sure - sophisticated automated test library and runner>
# Copyright (C) <2012-2023>  Gabriel Falcão <gabriel@nacaolivre.org>
# Copyright (C) <2012>  Lincoln Clarete <lincoln@comum.org>
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
import platform
import warnings

from datetime import datetime
from typing import Dict, List, Optional


__captured_warnings__ = []


class WarningReaper(object):
    """Captures warnings for posterior analysis"""

    builtin_showwarning = warnings.showwarning

    @property
    def warnings(self) -> List[Dict[str, object]]:
        return list(__captured_warnings__)

    def showwarning(
        self,
        message,
        category: Warning,
        filename: str,
        lineno: int,
        file: Optional[io.IOBase] = None,
        line: Optional[str] = None,
    ):
        occurrence = datetime.utcnow()
        info = locals()
        info.pop('self')
        __captured_warnings__.append(info)

    def enable_capture(self):
        warnings.showwarning = self.showwarning
        return self

    def clear(self):
        __captured_warnings__.clear()


def load_ctypes():
    try:
        import ctypes
    except (ImportError, ModuleNotFoundError):
        ctypes = None
    return ctypes


DictProxyType = type(object.__dict__)


def determine_python_implementation():
    return getattr(platform, "python_implementation", lambda: "")().lower()


def runtime_is_cpython():
    if not load_ctypes():
        return False

    return determine_python_implementation() == "cpython"


def get_py_ssize_t():
    ctypes = load_ctypes()
    pythonapi = getattr(ctypes, "pythonapi", None)
    if hasattr(pythonapi, "Py_InitModule4_64"):
        return ctypes.c_int64
    else:
        return ctypes.c_int


def noop_patchable_builtin(*args, **kw):
    pass


def craft_patchable_builtin():
    ctypes = load_ctypes()
    if not runtime_is_cpython():
        return noop_patchable_builtin

    class PyObject(ctypes.Structure):
        pass

    PyObject._fields_ = [
        ("ob_refcnt", get_py_ssize_t()),
        ("ob_type", ctypes.POINTER(PyObject)),
    ]

    def patchable_builtin(klass):
        name = klass.__name__
        target = getattr(klass, "__dict__", name)

        class SlotsProxy(PyObject):
            _fields_ = [("dict", ctypes.POINTER(PyObject))]

        proxy_dict = SlotsProxy.from_address(id(target))
        namespace = {}

        ctypes.pythonapi.PyDict_SetItem(
            ctypes.py_object(namespace),
            ctypes.py_object(name),
            proxy_dict.dict,
        )

        return namespace[name]

    return patchable_builtin


patchable_builtin = craft_patchable_builtin()
is_cpython = runtime_is_cpython()
