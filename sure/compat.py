# -*- coding: utf-8 -*-
import six

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

from sure.terminal import red, green, yellow


if six.PY2:
    def compat_repr(object_repr):
        # compat_repr is designed to return all reprs with leading 'u's
        # inserted to make all strings look like unicode strings.
        # This makes testing between py2 and py3 much easier.
        result = ''
        in_quote = False
        curr_quote = None
        for char in object_repr:
            if char in ['"', "'"] and (
                not curr_quote or char == curr_quote):
                if in_quote:
                    # Closing quote
                    curr_quote = None
                    in_quote = False
                else:
                    # Opening quote
                    curr_quote = char
                    result += 'u'
                    in_quote = True
            result += char
        return result
else:
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
            # We special case dicts to have a sorted repr. This makes testing
            # significantly easier
            val = _obj_with_safe_repr(val)
        ret = repr(val)
        if six.PY2:
            ret = ret.decode('utf-8')
    except UnicodeEncodeError:
        ret = red('a %r that cannot be represented' % type(val))
    else:
        ret = green(ret)

    return ret



text_type_name = six.text_type().__class__.__name__
