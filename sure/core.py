#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
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
import inspect
from sure.terminal import red, green, yellow


def safe_repr(x):
    try:
        return green(repr(x).decode('utf-8'))
    except UnicodeEncodeError:
        return red('a %r that cannot be represented' % type(x))


class DeepExplanation(unicode):
    def get_header(self, X, Y, suffix):
        return yellow(u"given\nX = %s\n    and\nY = %s\n%s" % (
            safe_repr(X),
            safe_repr(Y),
            suffix)).strip()

    def get_assertion(self, X, Y):
        return AssertionError(self.get_header(X, Y, self))

    def as_assertion(self, X, Y):
        raise self.get_assertion(X, Y)


class DeepComparison(object):
    def __init__(self, X, Y, parent=None):
        self.operands = X, Y
        self.parent = parent
        self._context = None

    def is_simple(self, obj):
        return isinstance(obj, (
            int, long, float, basestring,
        ))

    def compare_complex_stuff(self, X, Y):
        kind = type(X)
        mapping = {
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
            m = u'X%s != Y%s' % (red(c.current_X_keys), green(c.current_Y_keys))
            return DeepExplanation(m)

    def compare_dicts(self, X, Y):
        c = self.get_context()

        x_keys = list(sorted(X.keys()))
        y_keys = list(sorted(Y.keys()))

        diff_x = list(set(x_keys).difference(set(y_keys)))
        diff_y = list(set(y_keys).difference(set(x_keys)))
        if diff_x:
            msg = u"X%s has the key '%%s' whereas Y%s doesn't" % (
                red(c.current_X_keys),
                green(c.current_Y_keys),
            ) % diff_x[0]
            return DeepExplanation(msg)

        elif diff_y:
            msg = u"X%s doesn't have the key '%%s' whereas Y%s has it" % (
                red(c.current_X_keys),
                green(c.current_Y_keys),
            ) % diff_y[0]
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
            msg = u"X has %d items whereas Y has only %d" % (len_X, len_Y)
            return DeepExplanation(msg)
        elif len_X < len_Y:
            msg = u"Y has %d items whereas X has only %d" % (len_Y, len_X)
            return DeepExplanation(msg)
        elif X == Y:
            return True
        else:
            for i, (value_X, value_Y) in enumerate(zip(X, Y)):
                self.key_X = self.key_Y = i
                child = DeepComparison(
                    value_X,
                    value_Y,
                    parent=self,
                ).compare()
                if isinstance(child, DeepExplanation):
                    return child

    def compare(self):
        X, Y = self.operands
        c = self.get_context()
        if self.is_simple(X) and self.is_simple(Y):  # both simple
            if X == Y:
                return True
            c = self.get_context()
            m = u"X%s is %%r whereas Y%s is %%r"
            msg = m % (red(c.current_X_keys), green(c.current_Y_keys)) % (X, Y)
            return DeepExplanation(msg)

        elif type(X) is not type(Y):  # different types
            xname, yname = map(lambda _: type(_).__name__, (X, Y))
            msg = u'X%s is a %%s and Y%s is a %%s instead' % (
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
        name = func.func_code.co_filename

    return os.path.abspath(name)


def _get_line_number(func):
    try:
        return inspect.getlineno(func)
    except AttributeError:
        return func.func_code.co_firstlineno


def itemize_length(items):
    length = len(items)
    return '%d item%s' % (length, length > 1 and "s" or "")
