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
from threading import local
version = '0.1.3-unreleased'

def that_with_context(setup=None, teardown=None):
    def dec(func):
        func.__name__ = "test_%s" % func.__name__
        def wrap(*args, **kw):
            context = local()
            if callable(setup):
                setup(context)
            func(context, *args, **kw)

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
    try:
        list(obj)
        return True
    except TypeError:
        return hasattr(obj, '__iter__')

def all_integers(obj):
    if not is_iterable(obj):
        return

    for element in obj:
        if not isinstance(element, int):
            return

    return True

class that(object):
    def __init__(self, src, within_range=None):
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
        else:
            error = '%r should be equals to %r, but is not' % (self._src, dst)
            assert self._src == dst, error
            return self._src == dst, error

        return True

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

    def len_is(self, that):
        try:
            that = int(that)
        except TypeError:
            that = len(that)

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
        if self._eval and is_iterable(self._src):
            if isinstance(items, basestring):
                items = [items for x in range(len(items))]

            for index, (item, other) in enumerate(zip(self._src, items)):
                if self._range:
                    if index < self._range[0] or index > self._range[1]:
                        continue

                value = eval("%s.%s" % ('current', self._eval), {}, {'current': item})

                error = msg % (self._src, index, self._eval, other, value)
                if other != value:
                    raise AssertionError(error)
        return True

    def __contains__(self, what):
        if isinstance(self._src, dict):
            items = self._src.keys()

        try:
            list(self._src)
            items = self._src
        except TypeError:
            items = dir(self._src)

        return what in items
