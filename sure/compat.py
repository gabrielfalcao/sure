# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six
from collections import OrderedDict

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

# FIXME: move FakeOrderedDict to another module since it
#        does not have anything todo with compat.
#        The safe_repr function should already get a
#        FakeOrderedDict instance. Maybe the _obj_with_safe_repr
#        function should be part of the FakeOrderedDict
#        classes __repr__ method.
class FakeOrderedDict(OrderedDict):
    """ OrderedDict that has the repr of a normal dict

    We must return a string whether in py2 or py3.
    """
    def __unicode__(self):
        if not self:
            return '{}'
        key_values = []
        for key, value in self.items():
            key, value = repr(key), repr(value)
            if isinstance(value, six.binary_type) and six.PY2:
                value = value.decode("utf-8")
            key_values.append("{0}: {1}".format(key, value))
        res = "{{{0}}}".format(", ".join(key_values))
        return res

    if six.PY2:
        def __repr__(self):
            return self.__unicode__().encode('utf-8')
    else:
        def __repr__(self):
            return self.__unicode__()


def _obj_with_safe_repr(obj):
    if isinstance(obj, dict):
        ret = FakeOrderedDict()
        for key in sorted(obj.keys()):
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
