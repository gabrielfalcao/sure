# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - assertion toolbox>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from datetime import datetime
from pprint import pformat
from threading import local

version = '0.1.9'

def itemize_length(items):
    length = len(items)
    return '%d item%s' % (length, length > 1 and "s" or "")

def that_with_context(setup=None, teardown=None):
    def dec(func):
        func.__name__ = "test_%s" % func.__name__
        def wrap(*args, **kw):
            context = local()
            if callable(setup):
                setup(context)
            try:
                func(context, *args, **kw)
            finally:
                if callable(teardown):
                    teardown(context)

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        return wrap

    return dec

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
                    'within_range parameter must be a tuple with 2 objects'
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

    def raises(self, exc, msg=None):
        if not callable(self._src):
            raise TypeError('%r is not callable' % self._src)

        try:
            self._src(*self._callable_args, **self._callable_kw)

        except Exception, e:
            if isinstance(exc, basestring):
                msg = exc
                exc = type(e)

            if isinstance(exc, type) and issubclass(exc, Exception):
                if not isinstance(e, exc):
                    raise AssertionError('%r should raise %r, but raised %r' % (self._src, exc, e.__class__))

                if isinstance(msg, basestring) and msg not in unicode(e):
                    raise AssertionError('%r raised %s, but the exception message does not match. Expected %r, got %r' % (self._src, e, msg, unicode(e)))

            elif isinstance(msg, basestring) and msg not in unicode(e):
                raise AssertionError('When calling %r the exception message does not match. Expected %r, got %r' % (self._src, msg, unicode(e)))

            else:
                raise e
        else:
            raise AssertionError('calling function %s(%s at line: "%d") with args %r and kwargs %r did not raise %r' % (self._src.__name__, self._src.func_code.co_filename, self._src.func_code.co_firstlineno, self._callable_args, self._callable_kw, exc))

        return True

    def equals(self, dst):
        if self._attribute and is_iterable(self._src):
            msg = '%r[%d].%s should be %r, but is %r'

            for index, item in enumerate(self._src):
                if self._range:
                    if index < self._range[0] or index > self._range[1]:
                        continue

                attribute = getattr(item, self._attribute)
                error = msg % (self._src, index, self._attribute, dst, attribute)
                if attribute != dst:
                    raise AssertionError(error)
        elif is_iterable(self._src) and is_iterable(dst):
            length_src = len(self._src)
            length_dst = len(dst)
            assert length_src == length_dst, '%r has %s, but %r has %s' % (self._src, itemize_length(self._src), dst, itemize_length(dst))

            for i, (x, y) in enumerate(zip(self._src, dst)):
                assert x == y, '%r != %r at index %d' % (x, y, i)

        else:
            error = '%s != %s' % (
                pformat(self._src), pformat(dst)
            )
            assert self._src == dst, error
            return self._src == dst

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
                length
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
                length
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
                length
            )
            raise AssertionError(error)

        return True

    def len_lower_than_or_equals(self, that):
        that = self._get_that(that)

        length = len(self._src)

        if length > that:
            error = 'the length of %r should be lower then or equals %d, but is %d' % (
                self._src,
                that,
                length
            )
            raise AssertionError(error)

        return True

    def len_is(self, that):
        that = self._get_that(that)
        length = len(self._src)

        if length != that:
            error = 'the length of %r should be %d, but is %d' % (
                self._src,
                that,
                length
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
            "%s.%s" % ('current', self._eval), {}, {'current': item}
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
                        % (source, source_len, items_len, items)
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
            assert length == 0, '%r is not empty, it has %s' % (self._src, itemize_length(self._src))
            return True

        except TypeError:
            raise AssertionError("%r is not iterable" % self._src)

    @property
    def are_empty(self):
        return self.is_empty

    def __contains__(self, what):
        if isinstance(self._src, dict):
            items = self._src.keys()

        try:
            list(self._src)
            items = self._src
        except TypeError:
            items = dir(self._src)

        return what in items

    def contains(self, what):
        assert isinstance(what, basestring), '%r should be a string' % what
        assert isinstance(self._src, basestring), '%r is not a string, so is is impossible to check if "%s" is there' % (self._src, what)
        assert what in self._src, '"%s" should be in "%s"' % (what, self._src)
        return True

def within(**units):
    assert len(units) == 1, 'use within(number=unit). e.g.: within(one=second)'

    word, unit = units.items()[0]
    value = word_to_number(word)

    convert_from, convert_to = UNITS[unit]
    timeout = convert_from(value)
    exc = []
    def dec(func):
        def wrap(*args, **kw):
            start = datetime.now()

            try:
                func(*args, **kw)
            except Exception, e:
                exc.append(e)

            end = datetime.now()
            delta = (end - start)
            took = convert_to(delta.microseconds)
            print took, timeout
            assert took < timeout, \
                   '%s did not run within %s %s' % (func.__name__, word, unit)
            if exc:
                raise exc[0]

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        wrap.__dict__ = func.__dict__
        return wrap

    return dec

UNITS = {
    'minutes': (lambda from_num: from_num / 60.0, lambda to_num: to_num * 6000000),
    'seconds': (lambda from_num: from_num, lambda to_num: to_num / 100000),
    'miliseconds': (lambda from_num:from_num * 1000, lambda to_num: to_num/100),
    'microseconds': (lambda from_num:from_num * 100000, lambda to_num: to_num),
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
