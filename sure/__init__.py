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

import re
import os
import sys

import inspect
import traceback

from functools import wraps
from datetime import datetime

from sure.old import AssertionHelper
from sure.old import Iterable
from sure.old import builtins

<<<<<<< HEAD
from sure.core import DeepComparison
from sure.core import DeepExplanation
from sure.core import _get_file_name
from sure.core import _get_line_number
from sure.core import safe_repr
=======
version = '1.0.6'


class Anything(object):
    pass

anything = Anything()


def _get_file_name(func):
    try:
        name = inspect.getfile(func)
    except AttributeError:
        name = func.func_code.co_filename
>>>>>>> 35e78bec5113be399022c64da70204fac4cc9c16

from sure.magic import is_cpython, patchable_builtin
from sure.registry import context as _registry
from sure.six import string_types, text_type, PY3, get_function_code
from sure.six.moves import reduce


if PY3:
    basestring = str

version = '1.2.2'


not_here_error = \
    'you have tried to access the attribute %r from the context ' \
    '(aka VariablesBag), but there is no such attribute assigned to it. ' \
    'Maybe you misspelled it ? Well, here are the options: %s'


original_obj_attrs = dir(object)


class VariablesBag(dict):
    __varnames__ = None
    __sure_actions_ran__ = None
    __sure_action_results__ = None
    __sure_providers_of__ = None

    def __init__(self, *args, **kw):
        self.__varnames__ = []
        self.__sure_actions_ran__ = []
        self.__sure_action_results__ = []
        self.__sure_providers_of__ = {}
        return super(VariablesBag, self).__init__(*args, **kw)

    def __setattr__(self, attr, value):
        if attr not in dir(VariablesBag):
            self[attr] = value
            self.__varnames__.append(attr)
        return super(VariablesBag, self).__setattr__(attr, value)

    def __getattr__(self, attr):
        try:
            return super(VariablesBag, self).__getattribute__(attr)
        except AttributeError:
            if attr not in dir(VariablesBag):
                raise AssertionError(not_here_error % (
                    attr,
                    safe_repr(self.__varnames__),
                ))


class CallBack(object):
    context_error = u"the function %s defined at %s line %d, is being "\
        "decorated by either @that_with_context or @scenario, so it should " \
        "take at least 1 parameter, which is the test context"

    def __init__(self, cb, args, kwargs):
        self.callback = cb
        self.args = args or []
        self.kwargs = kwargs or {}
        self.callback_name = cb.__name__
        self.callback_filename = os.path.split(get_function_code(cb).co_filename)[-1]
        self.callback_lineno = get_function_code(cb).co_firstlineno + 1

    def apply(self, *optional_args):
        args = list(optional_args)
        args.extend(self.args)
        try:
            return self.callback(*args, **self.kwargs)
        except Exception:
            exc_klass, exc_value, tb = sys.exc_info()
            err = traceback.format_exc().splitlines()[-1]
            err = err.replace('{0}:'.format(exc_klass.__name__), '').strip()

            if err.startswith(self.callback_name) and \
               ('takes no arguments (1 given)' in err or
                'takes 0 positional arguments but 1 was given' in err):
                raise TypeError(self.context_error % (
                    self.callback_name,
                    self.callback_filename,
                    self.callback_lineno,
                    )
                )
            raise


def that_with_context(setup=None, teardown=None):
    def dec(func):
        @wraps(func)
        def wrap(*args, **kw):
            context = VariablesBag()

            if callable(setup):
                cb = CallBack(setup, args, kw)
                cb.apply(context)

            elif isinstance(setup, Iterable):
                for s in setup:
                    cb = CallBack(s, args, kw)
                    cb.apply(context)

            test = CallBack(func, args, kw)
            try:
                res = test.apply(context)
            finally:
                if callable(teardown):
                    cb = CallBack(teardown, args, kw)
                    cb.apply(context)

                elif isinstance(teardown, Iterable):
                    for s in teardown:
                        cb = CallBack(s, args, kw)
                        cb.apply(context)

            return res
        return wrap

    return dec

scenario = that_with_context


<<<<<<< HEAD
=======
def explanation(msg):
    def dec(func):
        def wrap(self, what):
            ret = func(self, what)
            assert ret, msg % (self._src, what)
            return True

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        return wrap

    return dec


def is_iterable(obj):
    return hasattr(obj, '__iter__') and not isinstance(obj, basestring)


def all_integers(obj):
    if not is_iterable(obj):
        return

    for element in obj:
        if not isinstance(element, int):
            return

    return True


class that(object):
    def __init__(self, src,
                 within_range=None,
                 with_args=None,
                 with_kwargs=None,
                 and_kwargs=None):

        self._src = src
        self._attribute = None
        self._eval = None
        self._range = None
        if all_integers(within_range):
            if len(within_range) != 2:
                raise TypeError(
                    'within_range parameter must be a tuple with 2 objects',
                )

            self._range = within_range

        self._callable_args = []
        if isinstance(with_args, (list, tuple)):
            self._callable_args = list(with_args)

        self._callable_kw = {}
        if isinstance(with_kwargs, dict):
            self._callable_kw.update(with_kwargs)

        if isinstance(and_kwargs, dict):
            self._callable_kw.update(and_kwargs)

    @classmethod
    def is_a_matcher(cls, func):
        def match(self, *args, **kw):
            return func(self._src, *args, **kw)

        new_matcher = deepcopy(match)
        new_matcher.__name__ = func.__name__
        setattr(cls, func.__name__, new_matcher)

        return new_matcher

    def raises(self, exc, msg=None):
        if not callable(self._src):
            raise TypeError('%r is not callable' % self._src)

        try:
            self._src(*self._callable_args, **self._callable_kw)

        except Exception, e:
            if isinstance(exc, basestring):
                msg = exc

            err = str(e)
            exc = type(e)

            if isinstance(exc, type) and issubclass(exc, Exception):
                if not isinstance(e, exc):
                    raise AssertionError(
                        '%r should raise %r, but raised %r' % (
                            self._src, exc, e.__class__))

                if isinstance(msg, basestring) and msg not in err:
                    raise AssertionError('''
                    %r raised %s, but the exception message does not
                    match.\n\nEXPECTED:\n%s\n\nGOT:\n%s'''.strip() % (
                            self._src,
                            type(e).__name__,
                            msg, err))

            elif isinstance(msg, basestring) and msg not in err:
                raise AssertionError(
                    'When calling %r the exception message does not match. ' \
                    'Expected: %r\n got:\n %r' % (self._src, msg, err))

            else:
                raise e
        else:
            if inspect.isbuiltin(self._src):
                _src_filename = '<built-in function>'
            else:
                _src_filename = _get_file_name(self._src)

            if inspect.isfunction(self._src):
                _src_lineno = _get_line_number(self._src)
                raise AssertionError(
                    'calling function %s(%s at line: "%d") with args %r and kwargs %r did not raise %r' % (
                        self._src.__name__,
                        _src_filename, _src_lineno,
                        self._callable_args,
                        self._callable_kw, exc))
            else:
                raise AssertionError(
                    'at %s:\ncalling %s() with args %r and kwargs %r did not raise %r' % (
                        _src_filename,
                        self._src.__name__,
                        self._callable_args,
                        self._callable_kw, exc))

        return True

    def deep_equals(self, dst):
        deep = DeepComparison(self._src, dst)
        comparison = deep.compare()
        if isinstance(comparison, bool):
            return comparison
        raise comparison.as_assertion(self._src, dst)

    def equals(self, dst):
        if self._attribute and is_iterable(self._src):
            msg = u'%r[%d].%s should be %r, but is %r'

            for index, item in enumerate(self._src):
                if self._range:
                    if index < self._range[0] or index > self._range[1]:
                        continue

                attribute = getattr(item, self._attribute)
                error = msg % (
                    self._src, index, self._attribute, dst, attribute)
                if attribute != dst:
                    raise AssertionError(error)
        else:
            return self.deep_equals(dst)

        return True

    def looks_like(self, dst):
        old_src = pformat(self._src)
        old_dst = pformat(dst)
        self._src = re.sub(r'\s', '', self._src).lower()
        dst = re.sub(r'\s', '', dst).lower()
        error = u'%s does not look like %s' % (old_src, old_dst)
        assert self._src == dst, error
        return self._src == dst

    def every_one_is(self, dst):
        msg = u'all members of %r should be %r, but the %dth is %r'
        for index, item in enumerate(self._src):
            if self._range:
                if index < self._range[0] or index > self._range[1]:
                    continue

            error = msg % (self._src, dst, index, item)
            if item != dst:
                raise AssertionError(error)

        return True

    @explanation('%r should differ to %r, but is the same thing')
    def differs(self, dst):
        return self._src != dst

    @explanation('%r should be a instance of %r, but is not')
    def is_a(self, dst):
        return isinstance(self._src, dst)

    def at(self, key):
        assert self.has(key)
        if isinstance(self._src, dict):
            return that(self._src[key])

        else:
            return that(getattr(self._src, key))

    @explanation('%r should have %r, but have not')
    def has(self, that):
        return that in self

    def _get_that(self, that):
        try:
            that = int(that)
        except TypeError:
            that = len(that)
        return that

    def len_greater_than(self, that):
        that = self._get_that(that)
        length = len(self._src)

        if length <= that:
            error = u'the length of the %s should be greater then %d, but is %d' % (
                type(self._src).__name__,
                that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_greater_than_or_equals(self, that):
        that = self._get_that(that)

        length = len(self._src)

        if length < that:
            error = u'the length of %r should be greater then or equals %d, but is %d' % (
                self._src,
                that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_lower_than(self, that):
        original_that = that
        if isinstance(that, Iterable):
            that = len(that)
        else:
            that = self._get_that(that)
        length = len(self._src)

        if length >= that:
            error = u'the length of %r should be lower then %r, but is %d' % (
                self._src,
                original_that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_lower_than_or_equals(self, that):
        that = self._get_that(that)

        length = len(self._src)
        error = u'the length of %r should be lower then or equals %d, but is %d'

        if length > that:
            msg = error % (
                self._src,
                that,
                length,
            )
            raise AssertionError(msg)

        return True

    def len_is(self, that):
        that = self._get_that(that)
        length = len(self._src)

        if length != that:
            error = u'the length of %r should be %d, but is %d' % (
                self._src,
                that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_is_not(self, that):
        that = self._get_that(that)
        length = len(self._src)

        if length == that:
            error = u'the length of %r should not be %d' % (
                self._src,
                that,
            )
            raise AssertionError(error)

        return True

    def like(self, that):
        return self.has(that)

    def the_attribute(self, attr):
        self._attribute = attr
        return self

    def in_each(self, attr):
        self._eval = attr
        return self

    def matches(self, items):
        msg = u'%r[%d].%s should be %r, but is %r'
        get_eval = lambda item: eval(
            "%s.%s" % ('current', self._eval), {}, {'current': item},
        )

        if self._eval and is_iterable(self._src):
            if isinstance(items, basestring):
                items = [items for x in range(len(items))]
            else:
                if len(items) != len(self._src):
                    source = map(get_eval, self._src)
                    source_len = len(source)
                    items_len = len(items)

                    raise AssertionError(
                        '%r has %d items, but the matching list has %d: %r'
                        % (source, source_len, items_len, items),
                    )

            for index, (item, other) in enumerate(zip(self._src, items)):
                if self._range:
                    if index < self._range[0] or index > self._range[1]:
                        continue

                value = get_eval(item)

                error = msg % (self._src, index, self._eval, other, value)
                if other != value:
                    raise AssertionError(error)
        else:
            return self.equals(items)

        return True

    @__builtin__.property
    def is_empty(self):
        try:
            lst = list(self._src)
            length = len(lst)
            assert length == 0, \
                   '%r is not empty, it has %s' % (self._src,
                                                   itemize_length(self._src))
            return True

        except TypeError:
            raise AssertionError("%r is not iterable" % self._src)

    @__builtin__.property
    def are_empty(self):
        return self.is_empty

    def __contains__(self, what):
        if isinstance(self._src, dict):
            items = self._src.keys()

        if isinstance(self._src, Iterable):
            items = self._src
        else:
            items = dir(self._src)

        return what in items

    def contains(self, what):
        assert what in self._src, '%r should be in %r' % (what, self._src)
        return True

    def does_not_contain(self, what):
        assert what not in self._src, \
            '%r should NOT be in %r' % (what, self._src)

        return True

    doesnt_contain = does_not_contain


>>>>>>> 35e78bec5113be399022c64da70204fac4cc9c16
def within(**units):
    assert len(units) == 1, 'use within(number=unit). e.g.: within(one=second)'

    word, unit = list(units.items())[0]
    value = word_to_number(word)

    convert_from, convert_to = UNITS[unit]
    timeout = convert_from(value)
    exc = []

    def dec(func):
        def wrap(*args, **kw):
            start = datetime.utcnow()

            try:
                func(start, *args, **kw)
            except TypeError as e:
                if PY3:
                    # PY3 has different error message
                    fmt = u'{0}() takes 0 positional arguments but 1 was given'
                else:
                    fmt = u'{0}() takes no arguments'
                err = text_type(e)
                if fmt.format(func.__name__) in err:
                    func(*args, **kw)
                else:
                    exc.append(traceback.format_exc())

            except Exception as e:
                exc.append(traceback.format_exc())

            end = datetime.utcnow()
            delta = (end - start)
            took = convert_to(delta.microseconds)
            print(took, timeout)
            assert took < timeout, \
                   '%s did not run within %s %s' % (func.__name__, word, unit)
            if exc:
                raise AssertionError(exc.pop(0))

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        wrap.__dict__ = func.__dict__
        return wrap

    return dec

UNITS = {
    'minutes': (
        lambda from_num: from_num / 60.0,
        lambda to_num: to_num * 6000000,
    ),
    'seconds': (
        lambda from_num: from_num,
        lambda to_num: to_num / 100000,
    ),
    'miliseconds': (
        lambda from_num: from_num * 1000,
        lambda to_num: to_num / 100,
    ),
    'microseconds': (
        lambda from_num: from_num * 100000,
        lambda to_num: to_num,
    ),
}

milisecond = miliseconds = u'miliseconds'
microsecond = microseconds = u'microseconds'
second = seconds = u'seconds'
minute = minutes = u'minutes'


def word_to_number(word):
    basic = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'eleven': 11,
        'twelve': 12,
    }
    try:
        return basic[word]
    except KeyError:
        raise AssertionError(
            'sure supports only literal numbers from one to twelve, ' \
            'you tried the word "twenty"')


def action_for(context, provides=None, depends_on=None):
    if not provides:
        provides = []

    if not depends_on:
        depends_on = []

    def register_providers(func, attr):
        if re.search(r'^[{]\d+[}]$', attr):
            return  # ignore dinamically declared provides

        if not attr in context.__sure_providers_of__:
            context.__sure_providers_of__[attr] = []

        context.__sure_providers_of__[attr].append(func)

    def register_dinamic_providers(func, attr, args, kwargs):
        found = re.search(r'^[{](\d+)[}]$', attr)
        if not found:
            return  # ignore dinamically declared provides

        index = int(found.group(1))
        assert index < len(args), \
            'the dinamic provider index: {%d} is bigger than %d, which is ' \
            'the length of the positional arguments passed to %s' % (
            index, len(args), func.__name__)

        attr = args[index]

        if not attr in context.__sure_providers_of__:
            context.__sure_providers_of__[attr] = []

        context.__sure_providers_of__[attr].append(func)

    def ensure_providers(func, attr, args, kwargs):
        found = re.search(r'^[{](\d+)[}]$', attr)
        if found:
            index = int(found.group(1))
            attr = args[index]

        assert attr in context, \
            'the action "%s" was supposed to provide the attribute "%s" ' \
            'into the context, but it did not. Please double check its ' \
            'implementation' % (func.__name__, attr)

    dependency_error_lonely = u'the action "%s" defined at %s:%d ' \
        'depends on the attribute "%s" to be available in the' \
        ' context. It turns out that there are no actions providing ' \
        'that. Please double-check the implementation'

    dependency_error_hints = u'the action "%s" defined at %s:%d ' \
        'depends on the attribute "%s" to be available in the context.'\
        ' You need to call one of the following actions beforehand:\n'

    def check_dependencies(func):
        action = func.__name__
        filename = _get_file_name(func)
        lineno = _get_line_number(func)

        for dependency in depends_on:
            if dependency in context.__sure_providers_of__:
                providers = context.__sure_providers_of__[dependency]
                err = dependency_error_hints % (
                    action,
                    filename,
                    lineno,
                    dependency,
                )
                err += '\n'.join([
                    ' -> %s at %s:%d' % (
                        p.__name__,
                        _get_file_name(p),
                        _get_line_number(p)) for p in providers])

            else:
                err = dependency_error_lonely % (
                    action,
                    filename,
                    lineno,
                    dependency,
                )

            assert dependency in context, err

    def decorate_and_absorb(func):
        [register_providers(func, attr) for attr in provides]

        @wraps(func)
        def wrapper(*args, **kw):
            [register_dinamic_providers(func, attr, args, kw)
             for attr in provides]
            context.__sure_actions_ran__.append((func, args, kw))
            check_dependencies(func)
            result = func(*args, **kw)
            [ensure_providers(func, attr, args, kw) for attr in provides]
            context.__sure_action_results__.append(result)
            return context

        setattr(context, func.__name__, wrapper)
        return wrapper

    return decorate_and_absorb


<<<<<<< HEAD
=======
class DeepExplanation(unicode):
    def get_header(self, X, Y, suffix):
        return (u"given\nX = %s\n    and\nY = %s\n%s" % (
            repr(X).decode('utf-8'),
            repr(Y).decode('utf-8'),
            suffix)).strip()

    def as_assertion(self, X, Y):
        raise AssertionError(self.get_header(X, Y, self))


class DeepComparison(object):
    def __init__(self, X, Y, parent=None):
        self.operands = X, Y
        self.parent = parent
        self._context = None

    def is_simple(self, obj):
        return isinstance(obj, (
            int, long, float, basestring, Anything,
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

            return '[%s]' % ']['.join(map(repr, i))

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
            if X == Y or anything in (X, Y):
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

        # If compare_complex_stuff() call does not return a
        # DeepExplanation, we're good to say that things worked.
        return exp or True

    def explanation(self):
        return self._explanation


>>>>>>> 35e78bec5113be399022c64da70204fac4cc9c16
def work_in_progress(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _registry['is_running'] = True
        ret = func(*args, **kwargs)
        _registry['is_running'] = False
        return ret

    return wrapper


def assertionmethod(func):
    @wraps(func)
    def wrapper(self, *args, **kw):
        value = func(self, *args, **kw)
        msg = "{0}({1}) failed".format(
            func.__name__,
            ", ".join(map(safe_repr, args)),
            ", ".join(["{0}={1}".format(k, safe_repr(kw[k])) for k in kw]),
        )
        if not PY3:
            msg = text_type(msg)

        assert value, msg
        return value

    return wrapper


def assertionproperty(func):
    return builtins.property(assertionmethod(func))

POSITIVES = [
    'should',
    'does',
    'do',
    'must',
    'when',
]

NEGATIVES = [
    'shouldnt',
    'dont',
    'do_not',
    'doesnt',
    'does_not',
    'doesnot',
    'should_not',
    'shouldnot',
]


class AssertionBuilder(object):
    def __init__(self, name=None, negative=False, obj=None):
        self._name = name
        self.negative = negative
        self.obj = obj
        self._callable_args = []
        self._callable_kw = {}
        self._that = AssertionHelper(self.obj)

    def __call__(self, obj):
        self.obj = obj

        if isinstance(obj, self.__class__):
            self.obj = obj.obj

        self._that = AssertionHelper(self.obj)
        return self

    def __getattr__(self, attr):
        special_case = False
        special_case = attr in (POSITIVES + NEGATIVES)

        negative = attr in NEGATIVES

        if special_case:
            return AssertionBuilder(attr, negative=negative, obj=self.obj)

        return super(AssertionBuilder, self).__getattribute__(attr)

    @assertionproperty
    def callable(self):
        if self.negative:
            assert not callable(self.obj), (
                'expected `{0}` to not be callable but it is'.format(safe_repr(self.obj)))
        else:
            assert callable(self.obj), (
                'expected {0} to be callable'.format(safe_repr(self.obj)))

        return True

    @assertionproperty
    def be(self):
        return self

    @assertionproperty
    def being(self):
        return self

    @assertionproperty
    def not_being(self):
        return self.should_not

    @assertionproperty
    def not_be(self):
        return self.should_not

    @assertionproperty
    def not_have(self):
        return self.should_not

    @assertionproperty
    def to_not(self):
        return self.should_not

    @assertionproperty
    def to(self):
        return self

    @assertionproperty
    def when(self):
        return self

    @assertionproperty
    def have(self):
        return self

    @assertionproperty
    def with_value(self):
        return self

    def property(self, name):
        has_it = hasattr(self.obj, name)
        if self.negative:
            assert not has_it, (
                '%r should not have the property `%s`, '
                'but it is %r' % (self.obj, name, getattr(self.obj, name)))
            return True

        assert has_it, (
            "%r should have the property `%s` but does not" % (
                self.obj, name))
        return expect(getattr(self.obj, name))

    def key(self, name):
        has_it = name in self.obj
        if self.negative:
            assert not has_it, (
                '%r should not have the key `%s`, '
                'but it is %r' % (self.obj, name, self.obj[name]))
            return True

        assert has_it, (
            "%r should have the key `%s` but does not" % (
                self.obj, name))
        return expect(self.obj[name])

    @assertionproperty
    def empty(self):
        representation = safe_repr(self.obj)
        length = len(self.obj)
        if self.negative:
            assert length > 0, (
                u"expected `{0}` to not be empty".format(representation))
        else:
            assert length is 0, (
                u"expected `{0}` to be empty but it has {1} items".format(representation, length))

        return True

    @assertionproperty
    def ok(self):
        if self.negative:
            msg = u'expected `{0}` to be falsy'.format(self.obj)
            assert not bool(self.obj), msg
        else:
            msg = u'expected `{0}` to be truthy'.format(self.obj)
            assert bool(self.obj), msg

        return True

    truthy = ok
    true = ok

    @assertionproperty
    def falsy(self):
        if self.negative:
            msg = u'expected `{0}` to be truthy'.format(self.obj)
            assert bool(self.obj), msg
        else:
            msg = u'expected `{0}` to be falsy'.format(self.obj)
            assert not bool(self.obj), msg

        return True

    false = falsy

    @assertionproperty
    def none(self):
        if self.negative:
            assert self.obj is not None, (
                r"expected `{0}` to not be None".format(self.obj))
        else:
            assert self.obj is None, (
                r"expected `{0}` to be None".format(self.obj))

        return True

    @assertionmethod
    def within(self, first, *rest):
        if isinstance(first, Iterable):
            collection_should = AssertionHelper(first)
        else:
            args = [first] + list(rest)
            collection_should = AssertionHelper(list(range(*args)))

        if self.negative:
            return collection_should.does_not_contain(self.obj)
        else:
            return collection_should.contains(self.obj)

    @assertionmethod
    def equal(self, what):
        try:
            comparison = DeepComparison(self.obj, what).compare()
            error = False
        except AssertionError as e:
            error = e
            comparison = None

        if isinstance(comparison, DeepExplanation):
            error = comparison.get_assertion(self.obj, what)

        if self.negative:
            if error:
                return True

            msg = '%s should differ to %s, but is the same thing'
            raise AssertionError(msg % (safe_repr(self.obj), safe_repr(what)))

        else:
            if not error:
                return True
            raise error

    eql = equal
    equals = equal
    equal_to = equal

    @assertionmethod
    def an(self, klass):
        if isinstance(klass, type):
            class_name = klass.__name__
        elif isinstance(klass, string_types):
            class_name = klass.strip()
        else:
            class_name = text_type(klass)

        is_vowel = class_name[0] in 'aeiou'

        if isinstance(klass, string_types):
            if '.' in klass:
                items = klass.split('.')
                first = items.pop(0)
                if not items:
                    items = [first]
                    first = '_abcoll'
            else:
                if sys.version_info <= (3, 0, 0):
                    first = u'__builtin__'
                else:
                    first = u'builtins'
                items = [klass]

            klass = reduce(getattr, items, __import__(first))

        suffix = is_vowel and "n" or ""

        if self.negative:
            assert not isinstance(self.obj, klass), (
                'expected `{0}` to not be a{1} {2}'.format(
                    self.obj, suffix, class_name))

        else:
            assert isinstance(self.obj, klass), (
                'expected `{0}` to be a{1} {2}'.format(
                    self.obj, suffix, class_name))
        return True

    a = an

    @assertionmethod
    def greater_than(self, dest):
        if self.negative:
            msg = u"expected `{0}` to not be greater than `{1}`".format(
                self.obj, dest)

            assert not self.obj > dest, msg

        else:
            msg = u"expected `{0}` to be greater than `{1}`".format(
                self.obj, dest)
            assert self.obj > dest, msg

        return True

    @assertionmethod
    def greater_than_or_equal_to(self, dest):
        if self.negative:
            msg = u"expected `{0}` to not be greater than or equal to `{1}`".format(
                self.obj, dest)

            assert not self.obj >= dest, msg

        else:
            msg = u"expected `{0}` to be greater than or equal to `{1}`".format(
                self.obj, dest)
            assert self.obj >= dest, msg

        return True

    @assertionmethod
    def lower_than(self, dest):
        if self.negative:
            msg = u"expected `{0}` to not be lower than `{1}`".format(
                self.obj, dest)

            assert not self.obj < dest, msg

        else:
            msg = u"expected `{0}` to be lower than `{1}`".format(
                self.obj, dest)
            assert self.obj < dest, msg

        return True

    @assertionmethod
    def lower_than_or_equal_to(self, dest):
        if self.negative:
            msg = u"expected `{0}` to not be lower than or equal to `{1}`".format(
                self.obj, dest)

            assert not self.obj <= dest, msg

        else:
            msg = u"expected `{0}` to be lower than or equal to `{1}`".format(
                self.obj, dest)
            assert self.obj <= dest, msg

        return True

    @assertionmethod
    def below(self, num):
        if self.negative:
            msg = u"{0} should not be below {1}".format(self.obj, num)
            assert not self.obj < num, msg
        else:
            msg = u"{0} should be below {1}".format(self.obj, num)
            assert self.obj < num, msg

        return True

    @assertionmethod
    def above(self, num):
        if self.negative:
            msg = u"{0} should not be above {1}".format(self.obj, num)
            assert not self.obj > num, msg
        else:
            msg = u"{0} should be above {1}".format(self.obj, num)
            assert self.obj > num, msg
        return True

    @assertionmethod
    def length_of(self, num):
        if self.negative:
            return self._that.len_is_not(num)

        return self._that.len_is(num)

    @assertionmethod
    def called_with(self, *args, **kw):
        self._callable_args = args
        self._callable_kw = kw
        return self

    called = builtins.property(called_with)

    @assertionmethod
    def throw(self, *args, **kw):
        _that = AssertionHelper(self.obj,
                     with_args=self._callable_args,
                     and_kwargs=self._callable_kw)

        if self.negative:
            msg = (u"{0} called with args {1} and kwargs {2} should "
                   "not raise {3} but raised {4}")

            exc = args and args[0] or Exception
            try:
                self.obj(*self._callable_args, **self._callable_kw)
                return True
            except Exception as e:
                err = msg.format(
                    self.obj,
                    self._that._callable_args,
                    self._that._callable_kw,
                    exc,
                    e,
                )
                raise AssertionError(err)

        return _that.raises(*args, **kw)

    @assertionmethod
    def return_value(self, value):
        return_value = self.obj(*self._callable_args, **self._callable_kw)
        return this(return_value).should.equal(value)

    @assertionmethod
    def look_like(self, value):
        if self.negative:
            try:
                self._that.looks_like(value)
            except AssertionError:
                return True
            else:
                msg = '%r should not look like %r but does'
                raise AssertionError(msg % (self.obj, value))

        return self._that.looks_like(value)

    @assertionmethod
    def contain(self, what):
        if self.negative:
            return expect(what).to.not_be.within(self.obj)
        else:
            return expect(what).to.be.within(self.obj)

    @assertionmethod
    def match(self, regex, *args):
        obj_repr = repr(self.obj)
        assert isinstance(self.obj, basestring), (
            "{0} should be a string in order to compare using .match()".format(obj_repr)
        )
        matched = re.search(regex, self.obj, *args)

        modifiers_map = {
            re.I: "i",
            re.L: "l",
            re.M: "m",
            re.S: "s",
            re.U: "u",
        }
        modifiers = "".join([modifiers_map.get(x, "") for x in args])
        regex_representation = '/{0}/{1}'.format(regex, modifiers)

        if self.negative:
            assert matched is None, (
                "{0} should not match the regular expression {1}".format(
                    obj_repr, regex_representation))

        else:
            assert matched is not None, (
                "{0} doesn't match the regular expression {1}".format(
                    obj_repr, regex_representation))

        return True

this = AssertionBuilder('this')
the = AssertionBuilder('the')
it = AssertionBuilder('it')
these = AssertionBuilder('these')
those = AssertionBuilder('those')
expect = AssertionBuilder('expect')


allows_new_syntax = not os.getenv('SURE_DISABLE_NEW_SYNTAX')


if is_cpython and allows_new_syntax:

    def make_safe_property(method, name, should_be_property=True):
        if not should_be_property:
            return method(None)

        def deleter(self, *args, **kw):
            pass

        def setter(self, other):
            pass

        return builtins.property(
            fget=method,
            fset=setter,
            fdel=deleter,
        )

    def positive_assertion(name, prop=True):
        def method(self):
            builder = AssertionBuilder(name, negative=False)
            instance = builder(self)
            callable_args = getattr(self, '_callable_args', None)
            if callable_args:
                instance._callable_args = callable_args
            callable_kw = getattr(self, '_callable_kw', None)
            if callable_kw:
                instance._callable_kw = callable_kw
            return instance

        method.__name__ = str(name)
        return make_safe_property(method, name, prop)

    def negative_assertion(name, prop=True):
        def method(self):
            builder = AssertionBuilder(name, negative=True)
            instance = builder(self)
            callable_args = getattr(self, '_callable_args', None)
            if callable_args:
                instance._callable_args = callable_args
            callable_kw = getattr(self, '_callable_kw', None)
            if callable_kw:
                instance._callable_kw = callable_kw
            return instance

        method.__name__ = str(name)
        return make_safe_property(method, name, prop)

    object_handler = patchable_builtin(object)

    # None does not have a tp_dict associated to its PyObject, so this
    # is the only way we could make it work like we expected.
    none = patchable_builtin(None.__class__)

    for name in POSITIVES:
        object_handler[name] = positive_assertion(name)
        none[name] = positive_assertion(name, False)

    for name in NEGATIVES:
        object_handler[name] = negative_assertion(name)
        none[name] = negative_assertion(name, False)


old_dir = dir


if allows_new_syntax:
    @wraps(builtins.dir)
    def _new_dir(obj=None):
        if obj is None:
            frame = inspect.currentframe()
            return sorted(frame.f_back.f_locals.keys())
        else:
            return sorted(set(old_dir(obj)).difference(POSITIVES + NEGATIVES))

    builtins.dir = _new_dir
