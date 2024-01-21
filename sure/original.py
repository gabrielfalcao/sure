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

"""original module from sure's inception prior to the creation of
:mod:`sure.special`"""

import os
import re
import traceback
import inspect
import typing
import types

from copy import deepcopy
from pprint import pformat
from functools import wraps
from typing import Union
from collections.abc import Iterable

from sure.astuneval import parse_accessor
from sure.core import Explanation
from sure.core import DeepComparison
from sure.core import itemize_length
from sure.core import identify_caller_location
from sure.errors import treat_error, CallerLocation
from sure.loader import get_file_name
from sure.loader import get_line_number
from sure.loader import resolve_path


def is_iterable(obj):
    """returns ``True`` the given object is iterable

    :param obj: :class:`object`
    """
    return not isinstance(obj, (str, )) and hasattr(obj, '__iter__')


def all_integers(obj: typing.Iterable) -> bool:
    """returns ``True`` if all members of the given iterable are integers

    :param obj: an iterable object
    """
    if not is_iterable(obj):
        return

    for element in obj:
        if not isinstance(element, int):
            return False

    return True


class AssertionHelper(object):
    """Accompanies :class:`~sure.AssertionBuilder` in performing
    assertions.
    """
    def __init__(self, src,
                 within_range=None,
                 with_args=None,
                 with_kws=None,
                 and_kws=None):

        self.actual = src
        self._attribute = None
        self.__element_access_expr__ = None
        self._range = None
        if all_integers(within_range):
            if len(within_range) != 2:
                raise TypeError(
                    f"within_range parameter must be a tuple with 2 objects, received a `{type(within_range).__name__}' with {len(within_range)} objects instead",
                )

            self._range = within_range

        self._callable_args = []
        if isinstance(with_args, (list, tuple)):
            self._callable_args = list(with_args)

        self._callable_kw = {}
        if isinstance(with_kws, dict):
            self._callable_kw.update(with_kws)

        if isinstance(and_kws, dict):
            self._callable_kw.update(and_kws)

    @property
    def src(self):
        return self.actual

    @classmethod
    def is_a_matcher(cls, func):
        def match(self, *args, **kw):
            return func(self.actual, *args, **kw)

        new_matcher = deepcopy(match)
        new_matcher.__name__ = func.__name__
        setattr(cls, func.__name__, new_matcher)

        return new_matcher

    def raises(self, exc, msg=None):
        if not callable(self.actual):
            raise TypeError(f'{repr(self.actual)} is not callable')

        try:
            self.actual(*self._callable_args, **self._callable_kw)
        except BaseException as e:
            e = err = treat_error(e)
            if isinstance(exc, (str, )):
                msg = exc
                exc = type(err)

            elif isinstance(exc, re.Pattern):
                msg = exc
                exc = type(err)

            caller = CallerLocation.most_recent()
            if isinstance(exc, type) and issubclass(exc, BaseException):
                if not isinstance(e, exc):
                    raise AssertionError(
                        f'{self.actual} should raise {exc}, but raised {e.__class__}:\nORIGINAL EXCEPTION:\n\n{traceback.format_exc()}'
                    )

                if isinstance(msg, (str, )) and msg not in str(err):
                    raise AssertionError(
                        f'{caller.path_and_lineno} raised {type(e).__name__}, but the exception message does not match.\n\nACTUAL:\n{str(err)}\n\nEXPECTATION:\n{msg}\n'
                    )

                elif isinstance(msg, re.Pattern) and not msg.search(str(err)):
                    raise AssertionError(
                        f"When calling {repr(identify_caller_location(self.actual))} the exception message does not match. "
                        f'Expected to match regex: {repr(msg.pattern)}\n against:\n {repr(str(err))}'
                    )

            else:
                raise e
        else:
            if inspect.isbuiltin(self.actual):
                _src_filename = '<built-in function>'
            else:
                _src_filename = get_file_name(self.actual)

            if inspect.isfunction(self.actual):
                _src_lineno = get_line_number(self.actual)
                raise AssertionError(
                    'calling function %s(%s at line: "%d") with args %r and kws %r did not raise %r' % (
                        self.actual.__name__,
                        _src_filename, _src_lineno,
                        self._callable_args,
                        self._callable_kw, exc))
            else:
                raise AssertionError(
                    f'at {_src_filename}:\ncalling {self.actual.__name__}() with args {repr(self._callable_args)} and kws {repr(self._callable_kw)} did not raise {repr(exc)}'
                )

        return True

    def deep_equals(self, expectation):
        deep = DeepComparison(self.actual, expectation)
        comparison = deep.compare()
        if isinstance(comparison, bool):
            return comparison

        raise comparison.as_assertion(self.actual, expectation, "Equality Error")

    def equals(self, expectation):
        if self._attribute and is_iterable(self.actual):
            msg = '%r[%d].%s should be %r, but is %r'

            for index, item in enumerate(self.actual):
                if self._range:
                    if index < self._range[0] or index > self._range[1]:
                        continue

                attribute = getattr(item, self._attribute)
                error = msg % (
                    self.actual, index, self._attribute, expectation, attribute)
                if attribute != expectation:
                    raise AssertionError(error)
        else:
            return self.deep_equals(expectation)

        return True

    def looks_like(self, expectation):
        old_src = pformat(self.actual)
        old_dst = pformat(expectation)
        self.actual = re.sub(r'\s', '', self.actual).lower()
        expectation = re.sub(r'\s', '', expectation).lower()
        error = '%s does not look like %s' % (old_src, old_dst)
        if self.actual == expectation:
            return True
        else:
            raise AssertionError(error)

    def _get_int_or_length(self, obj: Union[int, typing.Iterable]):
        if isinstance(obj, Iterable):
            return len(obj)
        return int(obj)

    def len_greater_than(self, that: Union[int, typing.Iterable]):
        that = self._get_int_or_length(that)
        length = len(self.actual)

        if length <= that:
            error = 'the length of the %s should be greater then %d, but is %d' % (
                type(self.actual).__name__,
                that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_greater_than_or_equals(self, that: Union[int, typing.Iterable]):
        that = self._get_int_or_length(that)

        length = len(self.actual)

        if length < that:
            error = 'the length of %r should be greater then or equals %d, but is %d' % (
                self.actual,
                that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_lower_than(self, that: Union[int, typing.Iterable]):
        original_that = that
        if isinstance(that, Iterable):
            that = len(that)
        else:
            that = self._get_int_or_length(that)
        length = len(self.actual)

        if length >= that:
            error = 'the length of %r should be lower then %r, but is %d' % (
                self.actual,
                original_that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_lower_than_or_equals(self, that: Union[int, typing.Iterable]):
        that = self._get_int_or_length(that)

        length = len(self.actual)
        error = 'the length of %r should be lower then or equals %d, but is %d'

        if length > that:
            msg = error % (
                self.actual,
                that,
                length,
            )
            raise AssertionError(msg)

        return True

    def len_is(self, that: Union[int, typing.Iterable]):
        that = self._get_int_or_length(that)
        length = len(self.actual)

        if length != that:
            error = 'the length of %r should be %d, but is %d' % (
                self.actual,
                that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_is_not(self, that: Union[int, typing.Iterable]):
        that = self._get_int_or_length(that)
        length = len(self.actual)

        if length == that:
            error = 'the length of %r should not be %d' % (
                self.actual,
                that,
            )
            raise AssertionError(error)

        return True

    def the_attribute(self, attr):
        self._attribute = attr
        return self

    def in_each(self, attr):
        self.__element_access_expr__ = attr
        return self

    def matches(self, items):
        msg = '%r[%d].%s should be %r, but is %r'

        get_eval = self.__element_access_expr__ and parse_accessor(self.__element_access_expr__) or (lambda x: None)

        if bool(self.__element_access_expr__) and is_iterable(self.actual):
            if isinstance(items, (str, )):
                items = [items for x in range(len(items))]
            else:
                if len(items) != len(self.actual):
                    source = list(map(get_eval, self.actual))
                    source_len = len(source)
                    items_len = len(items)

                    raise AssertionError(
                        '%r has %d items, but the matching list has %d: %r'
                        % (source, source_len, items_len, items),
                    )

            for index, (item, other) in enumerate(zip(self.actual, items)):
                value = get_eval(item)

                error = msg % (self.actual, index, self.__element_access_expr__, other, value)
                if other != value:
                    raise AssertionError(error)
        else:
            return self.equals(items)

        return True

    @property
    def is_empty(self):
        try:
            lst = list(self.actual)
            length = len(lst)
            if length == 0:
                return True
            else:
                raise AssertionError('%r is not empty, it has %s' % (
                    self.actual,
                    itemize_length(self.actual)
                ))

        except TypeError:
            raise AssertionError("%r is not iterable" % self.actual)

    @property
    def are_empty(self):
        return self.is_empty

    def contains(self, expectation):
        if expectation in self.actual:
            return True
        else:
            raise Explanation(f"`{expectation}' should be in `{self.actual}'").as_assertion(self.actual, expectation, "Content Verification Error")

    contain = contains
    to_contain = contains

    def does_not_contain(self, expectation):
        if expectation not in self.actual:
            return True
        else:
            raise Explanation(f"`{expectation}' should not be in `{self.actual}'").as_assertion(self.actual, expectation, "Content Verification Error")

    doesnt_contain = does_not_contain
    to_not_contain = does_not_contain
