# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - assertion toolbox>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
import re
import os
import sys
import inspect
import traceback

from copy import deepcopy
from pprint import pformat
from functools import wraps
from datetime import datetime
try:
    from collections import Iterable
except ImportError:
    Iterable = (list, dict, tuple)

from sure.registry import context as _registry
version = '0.10.3'


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

not_here_error = \
    'you have tried to access the attribute "%s" from the context ' \
    '(aka VariablesBag), but there is no such attribute assigned to it. ' \
    'Maybe you misspelled it ? Well, here are the options: [%s]'


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
                    ", ".join(map(repr, self.__varnames__)),
                ))


class CallBack(object):
    context_error = "the function %s defined at %s line %d, is being "\
        "decorated by either @that_with_context or @scenario, so it should " \
        "take at least 1 parameter, which is the test context"

    def __init__(self, cb, args, kwargs):
        self.callback = cb
        self.args = args or []
        self.kwargs = kwargs or {}
        self.callback_name = cb.__name__
        self.callback_filename = os.path.split(cb.func_code.co_filename)[-1]
        self.callback_lineno = cb.func_code.co_firstlineno + 1

    def apply(self, *optional_args):
        args = list(optional_args)
        args.extend(self.args)
        try:
            return self.callback(*args, **self.kwargs)
        except:
            err = unicode(sys.exc_info()[1])
            if err.startswith(self.callback_name) and \
               'takes no arguments (1 given)' in err:
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
            err = str(e)
            exc = type(e)

            if isinstance(exc, basestring):
                msg = exc

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
            msg = '%r[%d].%s should be %r, but is %r'

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
        error = '%s does not look like %s' % (old_src, old_dst)
        assert self._src == dst, error
        return self._src == dst

    def every_one_is(self, dst):
        msg = 'all members of %r should be %r, but the %dth is %r'
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
            error = 'the length of the %s should be greater then %d, but is %d' % (
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
            error = 'the length of %r should be greater then or equals %d, but is %d' % (
                self._src,
                that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_lower_than(self, that):
        that = self._get_that(that)
        length = len(self._src)

        if length >= that:
            error = 'the length of %r should be lower then %d, but is %d' % (
                self._src,
                that,
                length,
            )
            raise AssertionError(error)

        return True

    def len_lower_than_or_equals(self, that):
        that = self._get_that(that)

        length = len(self._src)
        error = 'the length of %r should be lower then or equals %d, but is %d'

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
            error = 'the length of %r should be %d, but is %d' % (
                self._src,
                that,
                length,
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
        msg = '%r[%d].%s should be %r, but is %r'
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

    @property
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

    @property
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


def within(**units):
    assert len(units) == 1, 'use within(number=unit). e.g.: within(one=second)'

    word, unit = units.items()[0]
    value = word_to_number(word)

    convert_from, convert_to = UNITS[unit]
    timeout = convert_from(value)
    exc = []

    def dec(func):
        def wrap(*args, **kw):
            start = datetime.utcnow()

            try:
                func(start, *args, **kw)
            except TypeError, e:
                fmt = '%s() takes no arguments'
                err = unicode(e)
                if (fmt % func.__name__) in err:
                    func(*args, **kw)
                else:
                    exc.append(e)

            except Exception, e:
                exc.append(e)

            end = datetime.utcnow()
            delta = (end - start)
            took = convert_to(delta.microseconds)
            print took, timeout
            assert took < timeout, \
                   '%s did not run within %s %s' % (func.__name__, word, unit)
            if exc:
                raise AssertionError(traceback.format_exc(exc.pop(0)))

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

milisecond = miliseconds = 'miliseconds'
microsecond = microseconds = 'microseconds'
second = seconds = 'seconds'
minute = minutes = 'minutes'


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
        if re.search(ur'^[{]\d+[}]$', attr):
            return  # ignore dinamically declared provides

        if not attr in context.__sure_providers_of__:
            context.__sure_providers_of__[attr] = []

        context.__sure_providers_of__[attr].append(func)

    def register_dinamic_providers(func, attr, args, kwargs):
        found = re.search(ur'^[{](\d+)[}]$', attr)
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
        found = re.search(ur'^[{](\d+)[}]$', attr)
        if found:
            index = int(found.group(1))
            attr = args[index]

        assert attr in context, \
            'the action "%s" was supposed to provide the attribute "%s" ' \
            'into the context, but it did not. Please double check its ' \
            'implementation' % (func.__name__, attr)

    dependency_error_lonely = 'the action "%s" defined at %s:%d ' \
        'depends on the attribute "%s" to be available in the' \
        ' context. It turns out that there are no actions providing ' \
        'that. Please double-check the implementation'

    dependency_error_hints = 'the action "%s" defined at %s:%d ' \
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


class DeepExplanation(unicode):
    def get_header(self, X, Y, suffix):
        return """given
X = %r
    and
Y = %r
%s""".strip() % (X, Y, suffix)

    def as_assertion(self, X, Y):
        raise AssertionError(self.get_header(X, Y, self))


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
            m = 'X%s != Y%s' % (c.current_X_keys, c.current_Y_keys)
            return DeepExplanation(m)

    def compare_dicts(self, X, Y):
        c = self.get_context()

        x_keys = list(sorted(X.keys()))
        y_keys = list(sorted(Y.keys()))

        diff_x = list(set(x_keys).difference(set(y_keys)))
        diff_y = list(set(y_keys).difference(set(x_keys)))
        if diff_x:
            msg = "X%s has the key '%%s' whereas Y%s doesn't" % (
                c.current_X_keys,
                c.current_Y_keys,
            ) % diff_x[0]
            return DeepExplanation(msg)

        elif diff_y:
            msg = "X%s doesn't have the key '%%s' whereas Y%s has it" % (
                c.current_X_keys,
                c.current_Y_keys,
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
            m = "X%s is %%r whereas Y%s is %%r"
            msg = m % (c.current_X_keys, c.current_Y_keys) % (X, Y)
            return DeepExplanation(msg)

        elif type(X) is not type(Y):  # different types
            xname, yname = map(lambda _: type(_).__name__, (X, Y))
            msg = 'X%s is a %%s and Y%s is a %%s instead' % (
                c.current_X_keys,
                c.current_Y_keys,
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


def work_in_progress(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _registry['is_running'] = True
        ret = func(*args, **kwargs)
        _registry['is_running'] = False
        return ret

    return wrapper


def it(name, *args, **kw):
    return _registry.get(name, *args, **kw)
