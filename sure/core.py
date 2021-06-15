# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2021>  Gabriel Falcão <gabriel@nacaolivre.org>
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

import os

try:
    from mock import _CallList
except ImportError:
    from mock.mock import _CallList

import inspect
from six import (
    text_type, integer_types, string_types, binary_type,
    get_function_code
)

from sure.terminal import red, green, yellow
from sure.compat import safe_repr, OrderedDict


class Anything(object):
    """Represents any possible value. Its existence is solely for
    idiomatic purposes.
    """
    def __eq__(self, _):
        return True

anything = Anything()


class DeepExplanation(text_type):
    def get_header(self, X, Y, suffix):
        params = (safe_repr(X), safe_repr(Y), text_type(suffix))
        header = "given\nX = {0}\n    and\nY = {1}\n{2}".format(*params)

        return yellow(header).strip()

    def get_assertion(self, X, Y):
        return AssertionError(self.get_header(X, Y, self))

    def as_assertion(self, X, Y):
        raise self.get_assertion(X, Y)


class DeepComparison(object):
    def __init__(self, X, Y, epsilon=None, parent=None):
        self.complex_cmp_funcs = {
            float: self.compare_floats,
            dict: self.compare_dicts,
            list: self.compare_iterables,
            tuple: self.compare_iterables,
            OrderedDict: self.compare_ordereddict
        }

        self.operands = X, Y
        self.epsilon = epsilon
        self.parent = parent
        self._context = None

    def is_simple(self, obj):
        return isinstance(obj, (
            string_types, integer_types, binary_type, Anything
        ))

    def is_complex(self, obj):
        return isinstance(obj, tuple(self.complex_cmp_funcs.keys()))

    def compare_complex_stuff(self, X, Y):
        return self.complex_cmp_funcs.get(type(X), self.compare_generic)(X, Y)

    def compare_generic(self, X, Y, msg_format='X{0} != Y{1}'):
        c = self.get_context()
        if X == Y:
            return True
        else:
            m = msg_format.format(red(c.current_X_keys), green(c.current_Y_keys))
            return DeepExplanation(m)

    def compare_floats(self, X, Y):
        c = self.get_context()
        if self.epsilon is None:
            return self.compare_generic(X, Y)

        if abs(X - Y) <= self.epsilon:
            return True
        else:
            m = 'X{0}±{1} != Y{2}±{3}'.format(
                red(c.current_X_keys), self.epsilon, green(c.current_Y_keys), self.epsilon)
            return DeepExplanation(m)

    def compare_dicts(self, X, Y):
        c = self.get_context()

        x_keys = list(X.keys())
        y_keys = list(Y.keys())

        diff_x = list(set(x_keys).difference(set(y_keys)))
        diff_y = list(set(y_keys).difference(set(x_keys)))
        if diff_x:
            msg = "X{0} has the key {1!r} whereas Y{2} does not".format(
                red(c.current_X_keys),
                safe_repr(diff_x[0]),
                green(c.current_Y_keys))
            return DeepExplanation(msg)

        elif diff_y:
            msg = "X{0} does not have the key {1!r} whereas Y{2} has it".format(
                red(c.current_X_keys),
                safe_repr(diff_y[0]),
                green(c.current_Y_keys))
            return DeepExplanation(msg)

        elif X == Y:
            return True

        else:
            for key_X in x_keys:
                self.key_X = key_X
                self.key_Y = key_X
                value_X = X[key_X]
                value_Y = Y[key_X]
                child = DeepComparison(
                    value_X,
                    value_Y,
                    epsilon=self.epsilon,
                    parent=self,
                ).compare()
                if isinstance(child, DeepExplanation):
                    return child

    def compare_ordereddict(self, X, Y):
        """Compares two instances of an OrderedDict."""

        # check if OrderedDict instances have the same keys and values
        child = self.compare_dicts(X, Y)
        if isinstance(child, DeepExplanation):
            return child

        # check if the order of the keys is the same
        for i, j in zip(X.items(), Y.items()):
            if i[0] != j[0]:
                c = self.get_context()
                msg = "X{0} and Y{1} are in a different order".format(
                    red(c.current_X_keys), green(c.current_Y_keys)
                )
                return DeepExplanation(msg)
        return True

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

            return '[{0}]'.format(']['.join(map(safe_repr, i)))

        class ComparisonContext:
            current_X_keys = get_keys(X_keys)
            current_Y_keys = get_keys(Y_keys)
            parent = comp

        self._context = ComparisonContext()
        return self._context

    def compare_iterables(self, X, Y):
        len_X, len_Y = map(len, (X, Y))
        if len_X > len_Y:
            msg = "X has {0} items whereas Y has only {1}".format(len_X, len_Y)
            return DeepExplanation(msg)
        elif len_X < len_Y:
            msg = "Y has {0} items whereas X has only {1}".format(len_Y, len_X)
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
        if self.is_complex(X) and type(X) is type(Y):
            return self.compare_complex_stuff(X, Y)

        def safe_format_repr(string):
            "Escape '{' and '}' in string for use with str.format()"
            if not isinstance(string, (string_types, binary_type)):
                return string

            orig_str_type = type(string)
            if isinstance(string, binary_type):
                safe_repr = string.replace(b'{', b'{{').replace(b'}', b'}}')
            else:
                safe_repr = string.replace('{', '{{').replace('}', '}}')

            # NOTE: str.replace() automatically converted the 'string' to 'unicode' in Python 2
            return orig_str_type(safe_repr)

        # get safe representation for X and Y
        safe_X, safe_Y = safe_format_repr(X), safe_format_repr(Y)

        # maintaining backwards compatibility between error messages
        kwargs = {}
        if self.is_simple(X) and self.is_simple(Y):
            kwargs['msg_format'] = 'X{{0}} is {0!r} whereas Y{{1}} is {1!r}'.format(safe_X, safe_Y)
        elif type(X) is not type(Y):
            kwargs['msg_format'] = 'X{{0}} is a {0} and Y{{1}} is a {1} instead'.format(
                type(X).__name__, type(Y).__name__)
        exp = self.compare_generic(X, Y, **kwargs)

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
    return '{0} item{1}'.format(length, length > 1 and "s" or "")
