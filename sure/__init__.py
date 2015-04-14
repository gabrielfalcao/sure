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

import difflib
import inspect
import traceback

from functools import wraps
from datetime import datetime

from six import string_types, text_type, PY3, get_function_code
from six.moves import reduce

from sure.old import AssertionHelper
from sure.old import Iterable
from sure.old import builtins

from sure.core import DeepComparison
from sure.core import DeepExplanation
from sure.core import _get_file_name
from sure.core import _get_line_number
from sure.core import safe_repr

from sure.magic import is_cpython, patchable_builtin
from sure.registry import context as _registry


if PY3:
    basestring = str

version = '1.2.10'


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


def ensure_type(caller_name, cast, obj):
    try:
        return cast(obj)
    except TypeError:
        raise AssertionError('{0} tried to  ')


class CallBack(object):
    context_error = "the function %s defined at %s line %d, is being "\
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
                    fmt = '{0}() takes 0 positional arguments but 1 was given'
                else:
                    fmt = '{0}() takes no arguments'
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


class IdentityAssertion(object):
    def __init__(self, assertion_builder):
        self._ab = assertion_builder

    def __call__(self, other):
        if self._ab.negative:
            assert self._ab.obj is not other, "{0} should not be the same object as {1}, but it is".format(self._ab.obj, other)
            return True
        assert self._ab.obj is other, "{0} should be the same object as {1}, but it is not".format(self._ab.obj, other)
        return True

    def __getattr__(self, name):
        return getattr(self._ab, name)


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
        return IdentityAssertion(self)

    being = be

    @assertionproperty
    def not_be(self):
        return IdentityAssertion(self.should_not)

    not_being = not_be

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
                "expected `{0}` to not be empty".format(representation))
        else:
            assert length == 0, (
                "expected `{0}` to be empty but it has {1} items".format(representation, length))

        return True

    @assertionproperty
    def ok(self):
        if self.negative:
            msg = 'expected `{0}` to be falsy'.format(self.obj)
            assert not bool(self.obj), msg
        else:
            msg = 'expected `{0}` to be truthy'.format(self.obj)
            assert bool(self.obj), msg

        return True

    truthy = ok
    true = ok

    @assertionproperty
    def falsy(self):
        if self.negative:
            msg = 'expected `{0}` to be truthy'.format(self.obj)
            assert bool(self.obj), msg
        else:
            msg = 'expected `{0}` to be falsy'.format(self.obj)
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
    def within_range(self, start, end):
        start = ensure_type('within_range', int, start)
        end = ensure_type('within_range', int, end)
        subject = ensure_type('within_range', int, self.obj)
        is_within_range = subject >= start and subject <= end

        if self.negative:
            if is_within_range:
                raise AssertionError('expected {0} to NOT be within {1} and {2}'.format(subject, start, end))
            return not is_within_range

        else:
            if not is_within_range:
                raise AssertionError('expected {0} to be within {1} and {2}'.format(subject, start, end))
            return is_within_range

    @assertionmethod
    def within(self, first, *rest):
        if isinstance(first, Iterable):
            collection_should = AssertionHelper(first)
            if self.negative:
                return collection_should.does_not_contain(self.obj)
            else:
                return collection_should.contains(self.obj)

        elif len(rest) == 1:
            return self.within_range(first, rest[0])
        else:
            if self.negative:
                ppath = '{0}.should_not.be.within'.format(self.obj)
            else:
                ppath = '{0}.should.be.within'.format(self.obj)

            raise AssertionError((
                '{0}({1}, {2}) must be called with either a iterable:\n'
                '{0}([1, 2, 3, 4])\n'
                'or with a range of numbers:'
                '{0}(1, 3000)'
            ).format(ppath, first, ", ".join([repr(x) for x in rest])))

    @assertionmethod
    def equal(self, what, epsilon=None):
        try:
            comparison = DeepComparison(self.obj, what, epsilon).compare()
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
    def different_of(self, what):
        differ = difflib.Differ()

        source = self.obj.strip().splitlines(True)
        destination = what.strip().splitlines(True)
        result = differ.compare(source, destination)
        difference = "".join(result)
        if self.negative:
            if self.obj != what:
                assert not difference, "Difference:\n\n{0}".format(difference)
        else:
            if self.obj == what:
                raise AssertionError("{0} should be different of {1}".format(self.obj, what))

        return True

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
                    first = '__builtin__'
                else:
                    first = 'builtins'
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
            msg = "expected `{0}` to not be greater than `{1}`".format(
                self.obj, dest)

            assert not self.obj > dest, msg

        else:
            msg = "expected `{0}` to be greater than `{1}`".format(
                self.obj, dest)
            assert self.obj > dest, msg

        return True

    @assertionmethod
    def greater_than_or_equal_to(self, dest):
        if self.negative:
            msg = "expected `{0}` to not be greater than or equal to `{1}`".format(
                self.obj, dest)

            assert not self.obj >= dest, msg

        else:
            msg = "expected `{0}` to be greater than or equal to `{1}`".format(
                self.obj, dest)
            assert self.obj >= dest, msg

        return True

    @assertionmethod
    def lower_than(self, dest):
        if self.negative:
            msg = "expected `{0}` to not be lower than `{1}`".format(
                self.obj, dest)

            assert not self.obj < dest, msg

        else:
            msg = "expected `{0}` to be lower than `{1}`".format(
                self.obj, dest)
            assert self.obj < dest, msg

        return True

    @assertionmethod
    def lower_than_or_equal_to(self, dest):
        if self.negative:
            msg = "expected `{0}` to not be lower than or equal to `{1}`".format(
                self.obj, dest)

            assert not self.obj <= dest, msg

        else:
            msg = "expected `{0}` to be lower than or equal to `{1}`".format(
                self.obj, dest)
            assert self.obj <= dest, msg

        return True

    @assertionmethod
    def below(self, num):
        if self.negative:
            msg = "{0} should not be below {1}".format(self.obj, num)
            assert not self.obj < num, msg
        else:
            msg = "{0} should be below {1}".format(self.obj, num)
            assert self.obj < num, msg

        return True

    @assertionmethod
    def above(self, num):
        if self.negative:
            msg = "{0} should not be above {1}".format(self.obj, num)
            assert not self.obj > num, msg
        else:
            msg = "{0} should be above {1}".format(self.obj, num)
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
            msg = ("{0} called with args {1} and kwargs {2} should "
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

    thrown = throw
    raised = thrown

    @assertionmethod
    def return_value(self, value):
        return_value = self.obj(*self._callable_args, **self._callable_kw)
        return this(return_value).should.equal(value)

    returned_the_value = return_value

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
            callable_args = getattr(self, '_callable_args', ())
            if callable_args:
                instance._callable_args = callable_args
            callable_kw = getattr(self, '_callable_kw', {})
            if callable_kw:
                instance._callable_kw = callable_kw
            return instance

        method.__name__ = str(name)
        return make_safe_property(method, name, prop)

    def negative_assertion(name, prop=True):
        def method(self):
            builder = AssertionBuilder(name, negative=True)
            instance = builder(self)
            callable_args = getattr(self, '_callable_args', ())
            if callable_args:
                instance._callable_args = callable_args
            callable_kw = getattr(self, '_callable_kw', {})
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
