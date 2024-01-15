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
import os
import types
from typing import Union, List, Dict, Tuple
from collections import OrderedDict
from functools import cache

from sure.terminal import yellow, red, green
from sure.doubles.dummies import Anything
from sure.doubles.mocks import MockCallListType
from sure.loader import get_file_name
from sure.loader import get_line_number
from sure.loader import resolve_path


class Explanation(str):
    def get_header(self, X, Y, suffix):
        header = f"X = {repr(X)}\n    and\nY = {repr(Y)}\n{str(suffix)}"
        return yellow(header).strip()

    def get_assertion(self, X, Y, prefix=""):
        prefix = f"{str(prefix or '').strip()}\n"

        return AssertionError(f"{prefix}{self.get_header(X, Y, self)}")

    def as_assertion(self, X, Y, *args, **kw):
        raise self.get_assertion(X, Y, *args, **kw)


class DeepComparison(object):
    """Performs a deep comparison between Python objects in the sense that complex or nested datastructures, such as :external+python:ref:`mappings <mapping>` of :external+python:ref:`sequences <sequence>`, :external+python:ref:`sequences <sequence>` of :external+python:ref:`mappings <mapping>`, :external+python:ref:`mappings <mapping>` of :external+python:ref:`sequences <sequence>` containing :external+python:ref:`mappings <mapping>` or sequences :external+python:ref:`sequences <sequence>` and so on, are recursively compared and reaching farthest accessible edges.
    """
    def __init__(self, X, Y, epsilon=None, parent=None):
        self.complex_cmp_funcs = {
            float: self.compare_floats,
            dict: self.compare_ordered_dicts,
            list: self.compare_iterables,
            set: self.compare_iterables,
            frozenset: self.compare_iterables,
            tuple: self.compare_iterables,
            OrderedDict: self.compare_ordered_dicts
        }

        self.operands = X, Y
        self.epsilon = epsilon
        self.parent = parent
        self._context = None

    def is_simple(self, obj):
        return isinstance(obj, (
            str, int, bytes, bytearray, Anything
        ))

    @cache
    def get_context(self):
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

            return '[{0}]'.format(']['.join(map(repr, i)))

        class ComparisonContext:
            current_X_keys = get_keys(X_keys)
            current_Y_keys = get_keys(Y_keys)
            parent = comp

        return ComparisonContext()

    def is_complex(self, obj):
        return isinstance(obj, tuple(self.complex_cmp_funcs.keys()))

    def compare_complex_instances(self, X, Y):
        return self.complex_cmp_funcs.get(type(X), self.compare_generic)(X, Y)

    def compare_generic(self, X, Y, msg_format='X{0} != Y{1}'):
        c = self.get_context()
        if X == Y:
            return True
        else:
            msg = msg_format.format(red(c.current_X_keys), green(c.current_Y_keys))
            return Explanation(msg)

    def compare_floats(self, X, Y):
        c = self.get_context()
        if self.epsilon is None:
            return self.compare_generic(X, Y)

        if abs(X - Y) <= self.epsilon:
            return True
        else:
            msg = 'X{0}±{1} != Y{2}±{3}'.format(
                red(c.current_X_keys),
                self.epsilon, green(c.current_Y_keys),
                self.epsilon
            )
            return Explanation(msg)

    def compare_ordered_dicts(self, X, Y):
        c = self.get_context()

        x_keys = list(X.keys())
        y_keys = list(Y.keys())

        diff_x = list(set(x_keys).difference(set(y_keys)))
        diff_y = list(set(y_keys).difference(set(x_keys)))
        if diff_x:
            msg = "X{0} has the key {1!r} whereas Y{2} does not".format(
                red(c.current_X_keys),
                repr(diff_x[0]),
                green(c.current_Y_keys),
            )
            return Explanation(msg)

        elif diff_y:
            msg = "X{0} does not have the key {1!r} whereas Y{2} has it".format(
                red(c.current_X_keys),
                repr(diff_y[0]),
                green(c.current_Y_keys)
            )
            return Explanation(msg)

        elif X == Y:
            return True

        else:
            for key_X in x_keys:
                self.key_X = key_X
                self.key_Y = key_X
                value_X = X[key_X]
                value_Y = Y[key_X]
                instance = DeepComparison(
                    value_X,
                    value_Y,
                    epsilon=self.epsilon,
                    parent=self,
                ).compare()
                if isinstance(instance, Explanation):
                    return instance

        for i, j in zip(X.items(), Y.items()):
            if i[0] != j[0]:
                c = self.get_context()
                msg = f"X{red(c.current_X_keys)} and Y{green(c.current_Y_keys)} appear have keys in different order"
                return Explanation(msg)
        return True

    def compare_iterables(self, X, Y):
        c = self.get_context()
        len_X, len_Y = map(len, (X, Y))
        if len_X > len_Y:
            if len_Y == 0:
                msg = f"X{red(c.current_X_keys)} has {len_X} items whereas Y{green(c.current_Y_keys)} is empty"
            else:
                msg = f"X{red(c.current_X_keys)} has {len_X} items whereas Y{green(c.current_Y_keys)} has only {len_Y}"
            return Explanation(msg)
        elif len_X < len_Y:
            if len_X == 0:
                msg = f"Y{green(c.current_Y_keys)} has {len_Y} items whereas X{red(c.current_X_keys)} is empty"
            else:
                msg = f"Y{green(c.current_Y_keys)} has {len_Y} items whereas X{red(c.current_X_keys)} has only {len_X}"

            return Explanation(msg)
        elif X == Y:
            return True
        else:
            for i, (value_X, value_Y) in enumerate(zip(X, Y)):
                self.key_X = self.key_Y = i
                instance = DeepComparison(
                    value_X,
                    value_Y,
                    epsilon=self.epsilon,
                    parent=self,
                ).compare()
                if isinstance(instance, Explanation):
                    return instance

    def compare(self):
        X, Y = self.operands

        if isinstance(X, MockCallListType):
            X = list(X)

        if isinstance(Y, MockCallListType):
            X = list(Y)

        c = self.get_context()
        if self.is_complex(X) and type(X) is type(Y):
            return self.compare_complex_instances(X, Y)

        def safe_format_repr(string):
            "Escape '{' and '}' in string for use with str.format()"
            if not isinstance(string, (str, bytes)):
                return string

            orig_str_type = type(string)
            if isinstance(string, bytes):
                safe_repr = string.replace(b'{', b'{{').replace(b'}', b'}}')
            else:
                safe_repr = string.replace('{', '{{').replace('}', '}}')

            # NOTE: str.replace() automatically converted the 'string' to 'unicode' in Python 2
            return orig_str_type(safe_repr)

        # get safe representation for X and Y
        safe_X, safe_Y = safe_format_repr(X), safe_format_repr(Y)

        # maintaining backwards compatibility between error messages
        kws = {}
        if self.is_simple(X) and self.is_simple(Y):
            kws['msg_format'] = 'X{{0}} is {0!r} whereas Y{{1}} is {1!r}'.format(safe_X, safe_Y)
        elif type(X) is not type(Y):
            kws['msg_format'] = 'X{{0}} is a {0} and Y{{1}} is a {1} instead'.format(
                type(X).__name__, type(Y).__name__)
        exp = self.compare_generic(X, Y, **kws)

        if isinstance(exp, Explanation):
            original_X, original_Y = c.parent.operands
            raise exp.as_assertion(original_X, original_Y)

        return exp


def itemize_length(items):
    length = len(items)
    return '{0} item{1}'.format(length, length > 1 and "s" or "")


def identify_caller_location(caller: Union[types.FunctionType, types.MethodType]):
    callable_name = caller.__name__
    filename = resolve_path(get_file_name(caller), os.getcwd())
    lineno = get_line_number(caller)
    return f'{callable_name} [{filename} line {lineno}]'
