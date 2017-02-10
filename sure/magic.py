# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import platform

is_cpython = (
    hasattr(platform, 'python_implementation')
    and platform.python_implementation().lower() == 'cpython')

if is_cpython:

    import ctypes
    DictProxyType = type(object.__dict__)

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
else:
    patchable_builtin = lambda *args, **kw: None
