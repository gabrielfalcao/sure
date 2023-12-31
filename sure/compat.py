# -*- coding: utf-8 -*-
import six

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

from sure.terminal import red, green, yellow


def compat_repr(object_repr):
    return object_repr


def _obj_with_safe_repr(obj):
    if isinstance(obj, dict):
        ret = {}
        try:
            keys = sorted(obj.keys())
        except TypeError:  # happens for obj types which are not orderable, like ``Enum``
            keys = obj.keys()
        for key in keys:
            ret[_obj_with_safe_repr(key)] = _obj_with_safe_repr(obj[key])
    elif isinstance(obj, list):
        ret = []
        for x in obj:
            if isinstance(x, dict):
                ret.append(_obj_with_safe_repr(x))
            else:
                ret.append(x)
    else:
        ret = obj
    return ret


def safe_repr(val):
    try:
        if isinstance(val, dict):
            # We special case dicts to have a sorted __repr__. This makes testing
            # significantly easier
            val = _obj_with_safe_repr(val)
        ret = repr(val)
    except UnicodeEncodeError:
        ret = red('a %r that cannot be represented' % type(val))
    else:
        ret = green(ret)

    return ret
