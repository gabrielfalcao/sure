# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - assertion toolbox>
# Copyright (C) <2012>  Gabriel Falcão <gabriel@nacaolivre.org>
# Copyright (C) <2012>  Lincoln Clarete <lincoln@comum.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
import platform


if platform.python_implementation() == 'CPython':

    import ctypes
    from types import DictProxyType

    Py_ssize_t = \
        hasattr(ctypes.pythonapi, 'Py_InitModule4_64') \
            and ctypes.c_int64 or ctypes.c_int

    class PyObject(ctypes.Structure):
        pass

    PyObject._fields_ = [
        ('ob_refcnt', Py_ssize_t),
        ('ob_type', ctypes.POINTER(PyObject)),
    ]

    class SlotsProxy(PyObject):
        _fields_ = [('dict', ctypes.POINTER(PyObject))]

    def patchable_builtin(klass):
        name = klass.__name__
        target = getattr(klass, '__dict__', name)

        if not isinstance(target, DictProxyType):
            return target

        proxy_dict = SlotsProxy.from_address(id(target))
        namespace = {}

        ctypes.pythonapi.PyDict_SetItem(
            ctypes.py_object(namespace),
            ctypes.py_object(name),
            proxy_dict.dict,
        )

        return namespace[name]
