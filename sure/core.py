#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2013>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from __future__ import unicode_literals

try:
    from collections import OrderedDict
except ImportError:
    from sure.ordereddict import OrderedDict

import os

try:
    from mock import _CallList
except ImportError:
    from mock.mock import _CallList

import inspect
from six import (
    text_type, integer_types, string_types, binary_type,
    PY3, get_function_code
)
from sure.terminal import red, green, yellow


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
            if isinstance(value, binary_type) and not PY3:
                value = value.decode("utf-8")
            key_values.append("{0}: {1}".format(key, value))
        res = "{{{0}}}".format(", ".join(key_values))
        return res

    if PY3:
        def __repr__(self):
            return self.__unicode__()
    else:
        def __repr__(self):
            return self.__unicode__().encode('utf-8')


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
        if not PY3:
            ret = ret.decode('utf-8')
    except UnicodeEncodeError:
        ret = red('a %r that cannot be represented' % type(val))
    else:
        ret = green(ret)

    return ret


class DeepExplanation(text_type):
    def get_header(self, X, Y, suffix):
        params = (safe_repr(X), safe_repr(Y), text_type(suffix))
        header = "given\nX = %s\n    and\nY = %s\n%s" % params

        return yellow(header).strip()

    def get_assertion(self, X, Y):
        return AssertionError(self.get_header(X, Y, self))

    def as_assertion(self, X, Y):
        raise self.get_assertion(X, Y)


class DeepComparison(object):
    def __init__(self, X, Y, epsilon=None, parent=None):
        self.operands = X, Y
        self.epsilon = epsilon
        self.parent = parent
        self._context = None

    def is_simple(self, obj):
        return isinstance(obj, (
            string_types, integer_types
        ))

    def compare_complex_stuff(self, X, Y):
        kind = type(X)
        mapping = {
            float: self.compare_floats,
            dict: self.compare_dicts,
            list: self.compare_iterables,
            tuple: self.compare_iterables,
        }
        return mapping.get(kind, self.compare_generic)(X, Y)

    def compare_generic(self, X, Y):
        c = self.get_context()
        if X == Y:
            return True
        else:
            m = 'X%s != Y%s' % (red(c.current_X_keys), green(c.current_Y_keys))
            return DeepExplanation(m)

    def compare_floats(self, X, Y):
        c = self.get_context()
        if self.epsilon is None:
            return self.compare_generic(X, Y)

        if abs(X - Y) <= self.epsilon:
            return True
        else:
            m = 'X%s±%s != Y%s±%s' % (red(c.current_X_keys), self.epsilon, green(c.current_Y_keys), self.epsilon)
            return DeepExplanation(m)

    def compare_dicts(self, X, Y):
        c = self.get_context()

        x_keys = list(sorted(X.keys()))
        y_keys = list(sorted(Y.keys()))

        diff_x = list(set(x_keys).difference(set(y_keys)))
        diff_y = list(set(y_keys).difference(set(x_keys)))
        if diff_x:
            msg = "X%s has the key %%r whereas Y%s does not" % (
                red(c.current_X_keys),
                green(c.current_Y_keys),
            ) % safe_repr(diff_x[0])
            return DeepExplanation(msg)

        elif diff_y:
            msg = "X%s does not have the key %%r whereas Y%s has it" % (
                red(c.current_X_keys),
                green(c.current_Y_keys),
            ) % safe_repr(diff_y[0])
            return DeepExplanation(msg)

        elif X == Y:
            return True

        else:
            for key_X, key_Y in zip(x_keys, y_keys):
                self.key_X = key_X
                self.key_Y = key_Y
                value_X = X[key_X]
                value_Y = Y[key_Y]
                child = DeepComparison(
                    value_X,
                    value_Y,
                    epsilon=self.epsilon,
                    parent=self,
                ).compare()
                if isinstance(child, DeepExplanation):
                    return child

    def get_context(self):
        if self._context:
            return self._context

        X_keys = []
        Y_keys = []

        comp = self
        while comp.parent:
            X_keys.insert(0, comp.parent.key_X)
            Y_keys.insert(0, comp.parent.key_Y)
            comp = comp.parent

        def get_keys(i):
            if not i:
                return ''

            return '[%s]' % ']['.join(map(safe_repr, i))

        class ComparisonContext:
            current_X_keys = get_keys(X_keys)
            current_Y_keys = get_keys(Y_keys)
            parent = comp

        self._context = ComparisonContext()
        return self._context

    def compare_iterables(self, X, Y):
        len_X, len_Y = map(len, (X, Y))
        if len_X > len_Y:
            msg = "X has %d items whereas Y has only %d" % (len_X, len_Y)
            return DeepExplanation(msg)
        elif len_X < len_Y:
            msg = "Y has %d items whereas X has only %d" % (len_Y, len_X)
            return DeepExplanation(msg)
        elif X == Y:
            return True
        else:
            for i, (value_X, value_Y) in enumerate(zip(X, Y)):
                self.key_X = self.key_Y = i
                child = DeepComparison(
                    value_X,
                    value_Y,
                    epsilon=self.epsilon,
                    parent=self,
                ).compare()
                if isinstance(child, DeepExplanation):
                    return child

    def compare(self):
        X, Y = self.operands

        if isinstance(X, _CallList):
            X = list(X)

        if isinstance(Y, _CallList):
            X = list(Y)

        c = self.get_context()
        if self.is_simple(X) and self.is_simple(Y):  # both simple
            if X == Y:
                return True
            c = self.get_context()
            m = "X%s is %%r whereas Y%s is %%r"
            msg = m % (red(c.current_X_keys), green(c.current_Y_keys)) % (X, Y)
            return DeepExplanation(msg)

        elif type(X) is not type(Y):  # different types
            xname, yname = map(lambda _: type(_).__name__, (X, Y))
            msg = 'X%s is a %%s and Y%s is a %%s instead' % (
                red(c.current_X_keys),
                green(c.current_Y_keys),
            ) % (xname, yname)
            exp = DeepExplanation(msg)

        else:
            exp = self.compare_complex_stuff(X, Y)

        if isinstance(exp, DeepExplanation):

            original_X, original_Y = c.parent.operands
            raise exp.as_assertion(original_X, original_Y)

        return exp

    def explanation(self):
        return self._explanation


def _get_file_name(func):
    try:
        name = inspect.getfile(func)
    except AttributeError:
        name = get_function_code(func).co_filename

    return os.path.abspath(name)


def _get_line_number(func):
    try:
        return inspect.getlineno(func)
    except AttributeError:
        return get_function_code(func).co_firstlineno


def itemize_length(items):
    length = len(items)
    return '%d item%s' % (length, length > 1 and "s" or "")
