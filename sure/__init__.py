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
"""Sure the sophisticated automated test library and runner for Python
"""

import re
import os
import sys

import builtins
import difflib
import inspect
import traceback

from functools import wraps, partial, reduce
from datetime import datetime

from sure.original import AssertionHelper
from sure.original import Iterable

from sure import registry
from sure.core import DeepComparison
from sure.core import Explanation
from sure.core import identify_caller_location
from sure.errors import SpecialSyntaxDisabledError
from sure.errors import WrongUsageError
from sure.errors import InternalRuntimeError
from sure.doubles.dummies import anything
from sure.loader import get_file_name
from sure.loader import get_line_number
from sure.loader import resolve_path
from sure.loader import CallerLocation
from sure.version import version
from sure.special import is_cpython, patchable_builtin
from sure.registry import context as _registry
import sure.reporters


original_obj_attrs = dir(object)
bugtracker = "https://github.com/gabrielfalcao/sure/issues"


class StagingArea(dict):
    """A :external+python:ref:`mapping <mapping>` primarily designated for providing
    a kind of "staging area" for test functions or methods decorated
    with :func:`~sure.scenario` so that in-memory test assets can be stored
    and retrieved within a `scenario's <https://en.wikipedia.org/wiki/Scenario_(computing)>`_ lifecycle.

    Test assets can be stored and retrieved both via :external+python:ref:`attribute-references` and :external+python:ref:`subscriptions`.

    An :exc:`AssertionError` is raised in the event of attempting to
    retrive a test asset not explicitly assigned to a
    :class:`StagingArea` instance. The error message contains a clear
    indication of the mistake along with a list of valid test assets
    presently available that particular instance of
    :class:`StagingArea`.

    Staging areas can contain specific actions defined through the :func:`~sure.action_for` :external+python:term:`decorator`.
    """

    __asset_names__ = None
    __sure_actions_ran__ = None
    __sure_action_results__ = None
    __sure_providers_of__ = None

    def __init__(self, *args, **kw):
        self.__asset_names__ = []
        self.__sure_actions_ran__ = []
        self.__sure_action_results__ = []
        self.__sure_providers_of__ = {}
        return super(StagingArea, self).__init__(*args, **kw)

    def __getattr__(self, attr):
        try:
            return super(StagingArea, self).__getattribute__(attr)
        except AttributeError:
            if attr not in dir(self) and attr not in self:
                raise AssertionError(
                    f"attempt to access attribute with name `{attr}' from the context "
                    f"(also known as `StagingArea'), but there is no such attribute assigned to it. "
                    f"The presently available attributes in this context are: {repr(self.__asset_names__)}"
                )

    def __setattr__(self, attr, value):
        if attr not in dir(StagingArea):
            self[attr] = value
            self.__asset_names__.append(attr)
        return super(StagingArea, self).__setattr__(attr, value)


class CallBack(object):
    context_error = (
        "the function %s defined at %s line %d, is being "
        "decorated by either @that_with_context or @scenario, so it should "
        "take at least 1 parameter, which is the test context"
    )

    def __init__(self, cb, args, kws):
        self.callback = cb
        self.args = args or []
        self.kws = kws or {}
        self.callback_name = cb.__name__
        self.callback_filename = resolve_path(get_file_name(cb), os.getcwd())
        self.callback_lineno = get_line_number(cb) + 1

    def apply(self, *optional_args):
        args = list(optional_args)
        args.extend(self.args)
        try:
            return self.callback(*args, **self.kws)
        except Exception:
            exc_klass, exc_value, tb = sys.exc_info()
            err = traceback.format_exc().splitlines()[-1]
            err = err.replace("{0}:".format(exc_klass.__name__), "").strip()

            if err.startswith(self.callback_name) and (
                "takes no arguments (1 given)" in err) or \
                "takes 0 positional arguments but 1 was given" in err:
                raise TypeError(
                    self.context_error
                    % (
                        self.callback_name,
                        self.callback_filename,
                        self.callback_lineno,
                    )
                )
            raise


def scenario(setup=None, teardown=None):
    """
Turns a test function or method into a kind of `scenario <https://en.wikipedia.org/wiki/Scenario_(computing)>`_

This :term:`python:decorator` that adds setup and teardown methods to a test
function.

The decorated function along with the provided setup and
teardown methods are required to take at least one position
argument ``context`` being an instance of
:class:`~sure.StagingArea`, an ephemeral object that only
exists within the scope of each test function decorated
thusly.

The conceptual function of the ``context`` argument is to
provide a kind of "staging area" wherewith assets pertaining
to the scope of a particular test can be added during the
"setup" phase, used during the "test" phase and properly
disposed during the "teardown" phase.

A hypothetical example of the utility or applicability of this
behavior would be a situation where a test requires a database
schema to be created before a test and dropped after a test in
order to prevent a race-condition between tests running
against a shared database.

The code below takes the :ref:`basic usage of psycopg2 module
<psycopg2:Usage>` as way to illustrate the example above:

.. code::

  import psycopg2
  from sure import expects, scenario


  def setup_database(context):
      context.conn = psycopg2.connect("dbname=test user=postgres")
      context.cursor = context.conn.cursor()
      # drop table in case that already exists
      context.cursor.execute(
          "DROP TABLE test;"
      )
      context.cursor.execute(
          "CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);"
      )
      context.cursor.execute(
          "INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def")
      )


  def teardown_database(context):
      context.cursor.close()
      context.conn.close()


  @scenario([setup_database], [teardown_database])
  def test_querying_for_one_column(context):
      context.cursor.execute("SELECT num FROM test;")
      row = context.cur.fetchone()
      expects(row).to.equal((100, ))

  @scenario([setup_database], [teardown_database])
  def test_querying_for_two_columns(context):
      context.cursor.execute("SELECT num, data FROM test;")
      row = context.cur.fetchone()
      expects(row).to.equal((100, "abc'def"))

.. seealso:: The documentation of :class:`StagingArea` contains more details about intrinsic behaviors to be expected in using a ``context``, in special the fact that trying to access attributes not explicitly assigned causes an :exc:`AsserionError` to be raised indicating the mistake.
    """
    def dec(func):
        @wraps(func)
        def wrap(*args, **kw):
            context = StagingArea()

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


that_with_context = scenario


def within(**units):
    if len(units) != 1:
        raise WrongUsageError(
            "within() takes a single keyword argument where the argument must be "
            "a numerical description from one to eighteen and the value. "
            "For example: within(eighteen=miliseconds)"
        )

    word, unit = list(units.items())[0]
    value = word_to_number(word)

    convert_from, convert_to = UNITS[unit]
    timeout = convert_from(value)

    def dec(func):
        exc = []

        @wraps(func)
        def wrap(*args, **kw):
            start = datetime.utcnow()

            try:
                func(*args, **kw)

            except Exception as e:
                exc.append(e)

            end = datetime.utcnow()
            delta = end - start
            took = convert_to(delta.microseconds)

            if not took < timeout:
                raise AssertionError(
                    f"{identify_caller_location(func)} did not run within {word} {unit}"
                )
            if exc:
                raise exc.pop(0)

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        wrap.__dict__ = func.__dict__
        return wrap

    return dec


UNITS = {
    "minutes": (
        lambda from_num: from_num / 60.0,
        lambda to_num: to_num * 6000000,
    ),
    "seconds": (
        lambda from_num: from_num,
        lambda to_num: to_num / 100000,
    ),
    "miliseconds": (
        lambda from_num: from_num * 1000,
        lambda to_num: to_num / 100,
    ),
    "microseconds": (
        lambda from_num: from_num * 100000,
        lambda to_num: to_num,
    ),
}

milisecond = miliseconds = "miliseconds"
microsecond = microseconds = "microseconds"
second = seconds = "seconds"
minute = minutes = "minutes"


def word_to_number(word):
    basic = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
    }
    # TODO: refactor
    try:
        return basic[word]
    except KeyError:
        raise AssertionError(
            "sure supports only literal numbers from one to sixteen, "
            f'you tried the word "{word}"'
        )


def action_for(context, provides=None, depends_on=None):
    """function decorator for defining functions which might provide a
    list of assets to the staging area and might declare a list of
    dependencies expected to exist within a :class:`StagingArea`
    """
    action_subaction_dependency = (
        'the action "%s" defined at %s:%d '
        'depends on the attribute "%s" to be available in the current context'
    )
    action_attribute_dependency = (
        'the action "%s" defined at %s:%d '
        'depends on the attribute "%s" to be available in the context.'
        " Perhaps one of the following actions might provide that attribute:\n"
    )

    if not provides:
        provides = []

    if not depends_on:
        depends_on = []

    def register_providers(func, attr):
        if re.search(r"^[{]\d+[}]$", attr):
            return  # ignore dynamically declared provides

        if attr not in context.__sure_providers_of__:
            context.__sure_providers_of__[attr] = []

        context.__sure_providers_of__[attr].append(func)

    def register_dynamic_providers(func, attr, args, kws):
        found = re.search(r"^[{](\d+)[}]$", attr)
        if not found:
            return  # ignore dynamically declared provides

        index = int(found.group(1))
        if index > len(args):
            raise AssertionError(
                f"the dynamic provider index: {index} is greater than {len(args)}, which is "
                f"the length of the positional arguments passed to {func.__name__}"
            )

        attr = args[index]

        if attr not in context.__sure_providers_of__:
            context.__sure_providers_of__[attr] = []

        context.__sure_providers_of__[attr].append(func)

    def ensure_providers(func, attr, args, kws):
        found = re.search(r"^[{](\d+)[}]$", attr)
        if found:
            index = int(found.group(1))
            attr = args[index]

        if attr not in context:
            raise AssertionError(
                f'the action "{func.__name__}" is supposed to provide the attribute "{attr}" '
                "into the context but does not. Check its "
                f"implementation for correctness or, if there is a bug in Sure, consider reporting that at {bugtracker}"
            )

    def check_dependencies(func):
        action = func.__name__
        filename = get_file_name(func)
        lineno = get_line_number(func)

        for dependency in depends_on:
            if dependency in context.__sure_providers_of__:
                providers = context.__sure_providers_of__[dependency]
                err = action_attribute_dependency % (
                    action,
                    filename,
                    lineno,
                    dependency,
                )
                err += "\n".join(
                    [
                        " -> %s at %s:%d"
                        % (p.__name__, get_file_name(p), get_line_number(p))
                        for p in providers
                    ]
                )

            else:
                err = action_subaction_dependency % (
                    action,
                    filename,
                    lineno,
                    dependency,
                )

            if dependency not in context:
                raise AssertionError(err)

    def decorate_and_absorb(func):
        [register_providers(func, attr) for attr in provides]

        @wraps(func)
        def wrapper(*args, **kw):
            [register_dynamic_providers(func, attr, args, kw) for attr in provides]
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
    def wrapper(*args, **kws):
        _registry["is_running"] = True
        ret = func(*args, **kws)
        _registry["is_running"] = False
        return ret

    return wrapper


def assertionmethod(func):
    registry.KNOWN_ASSERTIONS.append(func.__name__)

    @wraps(func)
    def wrapper(self, *args, **kw):
        try:
            value = func(self, *args, **kw)
        except AssertionError as e:
            raise e

        if not value:
            raise AssertionError(
                f"{0}({1}{2}) failed".format(
                    func.__name__,
                    ", ".join(map(repr, args)),
                    ", ".join(["{0}={1}".format(k, repr(kw[k])) for k in kw]),
                )
            )
        return value

    return wrapper


def assertionproperty(func):
    registry.KNOWN_ASSERTIONS.append(func.__name__)
    return builtins.property(assertionmethod(func))


class AssertionBuilder(object):
    def __init__(
        self,
        name=None,
        negative=False,
        actual=None,
        with_args=None,
        with_kws=None,
        and_kws=None
    ):
        self._name = name
        self.negative = negative

        self.actual = actual
        self._callable_args = []
        self._callable_kw = {}
        if isinstance(with_args, (list, tuple)):
            self._callable_args = list(with_args)

        if isinstance(with_kws, dict):
            self._callable_kw.update(with_kws)

        if isinstance(and_kws, dict):
            self._callable_kw.update(and_kws)

        self.__caller__ = None

    def __call__(self,
                 actual,
                 with_args=None,
                 with_kws=None,
                 and_kws=None,
                 *args, **kw):
        self.__caller__ = CallerLocation.most_recent()

        if isinstance(actual, self.__class__):
            self.actual = actual.actual
            self._callable_args = actual._callable_args
            self._callable_kw = actual._callable_kw
        else:
            self.actual = actual

        self._callable_args = []
        self._callable_kw = {}
        if isinstance(with_args, (list, tuple)):
            self._callable_args = list(with_args)

        if isinstance(with_kws, dict):
            self._callable_kw.update(with_kws)

        if isinstance(and_kws, dict):
            self._callable_kw.update(and_kws)

        self._that = AssertionHelper(self.actual, *args, **kw)
        return self

    def __getattr__(self, attr):
        special_case = False
        special_case = attr in (POSITIVES + NEGATIVES)

        negative = attr in NEGATIVES

        if special_case:
            return AssertionBuilder(
                attr,
                negative=negative,
                actual=self.actual,
                with_args=self._callable_args,
                with_kws=self._callable_kw,
            )

        try:
            return getattr(self._that, attr)
        except AttributeError:
            return self.__getattribute__(attr)
        return super(AssertionBuilder, self).__getattribute__(attr)

    @assertionproperty
    def callable(self):
        if self.negative:
            if callable(
                self.actual
            ):
                raise AssertionError(
                    f"{self.__caller__.display_info} expects {repr(self.actual)} to not be callable"
                )
        else:
            if not callable(self.actual):
                raise AssertionError(
                    f"{self.__caller__.display_info} expects {repr(self.actual)} to be callable"
                )

        return True

    @assertionproperty
    def be(self):
        return ObjectIdentityAssertion(self)

    @assertionproperty
    def being(self):
        return ObjectIdentityAssertion(self)

    @assertionproperty
    def not_be(self):
        return ObjectIdentityAssertion(self.should_not)

    @assertionproperty
    def not_being(self):
        return ObjectIdentityAssertion(self.should_not)

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
    def which(self):
        return self

    @assertionproperty
    def have(self):
        return self

    @assertionproperty
    def with_value(self):
        return self

    @assertionmethod
    def property(self, name):
        """performs an assertion of whether the ``source`` object has an
        instance property with ``name``

        :param name: a string
        """
        has_it = hasattr(self.actual, name)
        if self.negative:
            if not not has_it:
                raise AssertionError(
                    f"{self.actual} should not have the property `{name}' which is actually present and holds the value `{getattr(self.actual, name)}'"
                )
            else:
                return True
        else:
            if not has_it:
                raise AssertionError(
                    f"{self.actual} should have the property `{name}' which is not present"
                )

        return expect(getattr(self.actual, name))

    @assertionmethod
    def key(self, name):
        actual = self.actual
        has_it = name in actual
        if self.negative:
            if has_it:
                raise AssertionError(
                    f"{actual} should not have the key `{name}' which is actually present and holds the value `{actual[name]}'"
                )
            else:
                return True
        else:
            if not has_it:
                raise AssertionError(
                    f"{actual} should have the key `{name}' which is not present"
                )
            else:
                return expect(actual[name])

    @assertionproperty
    def empty(self):
        actual = self.actual
        representation = repr(actual)
        length = len(actual)
        if self.negative:
            if length == 0:
                raise AssertionError(
                    f"{self.__caller__.display_info} expects `{representation}' to not be empty"
                )
            else:
                return True
        else:
            if length > 0:
                raise AssertionError(
                    f"{self.__caller__.display_info} expects '{representation}' to be empty but contains {length} items"
                )
            else:
                return True

    @assertionproperty
    def ok(self):
        if self.negative:
            if bool(self.actual):
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to be `{False}'")
        else:
            if not bool(self.actual):
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to be `{True}'")

        return True

    true = ok
    truthy = ok

    @assertionproperty
    def not_ok(self):
        if self.negative:
            if not bool(self.actual):
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to be `{True}'")
        else:
            if bool(self.actual):
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to be `{False}'")

        return True

    false = not_ok
    falsy = not_ok

    @assertionproperty
    def none(self):
        if self.negative:
            if self.actual is None:
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to not be None")
        else:
            if self.actual is not None:
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to be None")

        return True

    def __contains__(self, expectation):
        if isinstance(self.actual, dict):
            items = self.actual.keys()

        if isinstance(self.actual, Iterable):
            items = self.actual
        else:
            items = dir(self.actual)

        return expectation in items

    @assertionmethod
    def contains(self, expectation):
        if expectation in self.actual:
            return True
        else:
            raise Explanation(f'{expectation} should be in {self.actual}').as_assertion(self.actual, expectation, "Content Verification Error")

    contain = contains
    to_contain = contains

    @assertionmethod
    def does_not_contain(self, expectation):
        if expectation not in self.actual:
            return True
        else:
            raise Explanation(f'{expectation} should not be in {self.actual}').as_assertion(self.actual, expectation, "Content Verification Error")

    doesnt_contain = does_not_contain
    to_not_contain = does_not_contain

    @assertionmethod
    def within_range(self, start: int, end: int):
        start = int(start)
        end = int(end)
        subject = int(self.actual)
        is_within_range = subject >= start and subject <= end

        if self.negative:
            if is_within_range:
                raise AssertionError(
                    f"{self.__caller__.display_info} expects {subject} to NOT be within {start} and {end}"
                )
            return not is_within_range

        else:
            if not is_within_range:
                raise AssertionError(
                    f"{self.__caller__.display_info} expects {subject} to be within {start} and {end}"
                )
            return is_within_range

    @assertionmethod
    def within(self, first, *rest):
        if isinstance(first, Iterable):
            verification_of_whether_collection = AssertionHelper(first)
            if self.negative:
                return verification_of_whether_collection.does_not_contain(self.actual)
            else:
                return verification_of_whether_collection.contain(self.actual)

        elif len(rest) == 1:
            return self.within_range(first, rest[0])
        else:
            # TODO: return actual path to chain of attribute access
            # instead of hardcoding ``.should_not.be.within`` and ``.should.be.within`` in the
            # variable assignments below
            if self.negative:
                ppath = "{0}.should_not.be.within".format(self.actual)
            else:
                ppath = "{0}.should.be.within".format(self.actual)

            raise AssertionError(
                (
                    "{0}({1}, {2}) must be called with either a iterable:\n"
                    "{0}([1, 2, 3, 4])\n"
                    "or with a range of numbers:"
                    "{0}(1, 3000)"
                ).format(ppath, first, ", ".join([repr(x) for x in rest]))
            )

    @assertionmethod
    def equal(self, expectation, epsilon=None):
        """compares given object ``X'`  with an expected '`Y'` object.

        It primarily assures that the compared objects are absolute equal '`=='`.

        :param expectation: the expected value
        :param epsilon: a delta to leverage upper-bound floating point permissiveness
        """
        actual = self.actual

        try:
            comparison = DeepComparison(actual, expectation, epsilon).compare()
            error = False
        except AssertionError as e:
            error = e
            comparison = None

        if isinstance(comparison, Explanation):
            error = comparison.get_assertion(actual, expectation, "Equality Error")

        if self.negative:
            if error:
                return True

            msg = "expecting %s to be different of %s"
            raise AssertionError(msg % (repr(actual), repr(expectation)))

        else:
            if not error:
                return True
            raise error

    eql = equal
    equals = equal
    equal_to = equal

    @assertionmethod
    def different_of(self, expectation):
        differ = difflib.Differ()

        actual = isinstance(self.actual, AssertionHelper) and self.actual.src or self.actual
        if not isinstance(expectation, str):
            raise WrongUsageError(f".different_of only works for string comparison but in this case is expecting {repr(expectation)} ({type(expectation)}) instead")

        if not isinstance(self.actual, str):
            raise WrongUsageError(f".different_of only works for string comparison but in this case the actual source comparison object is {repr(self.actual)} ({type(self.actual)}) instead")

        source = actual.strip().splitlines(True)
        destination = expectation.strip().splitlines(True)
        result = differ.compare(source, destination)
        difference = "".join(result)
        if self.negative:
            if actual != expectation:
                raise AssertionError("Difference:\n\n{0}".format(difference))
        else:
            if actual == expectation:
                raise AssertionError(
                    "{0} should be different of {1}".format(actual, expectation)
                )

        return True

    @assertionmethod
    def a(self, klass):
        if isinstance(klass, type):
            class_name = klass.__name__
        elif isinstance(klass, (str, )):
            class_name = klass.strip()
        else:
            class_name = str(klass)

        is_vowel = class_name.lower()[0] in "aeiou"

        if isinstance(klass, (str, )):
            if "." in klass:
                items = klass.split(".")
                first = items.pop(0)
                if not items:
                    items = [first]
                    first = "_abcoll"
            else:
                if sys.version_info <= (3, 0, 0):
                    first = "__builtin__"
                else:
                    first = "builtins"
                items = [klass]

            klass = reduce(getattr, items, __import__(first))

        suffix = is_vowel and "n" or ""

        if self.negative:
            if isinstance(
                self.actual, klass
            ):
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to not be a{suffix} `{class_name}'")

        else:
            if not isinstance(self.actual, klass):
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to be a{suffix} `{class_name}'")

        return True

    an = a

    @assertionmethod
    def greater_than(self, expectation):
        if self.negative:
            msg = f"{self.__caller__.display_info} expects `{self.actual}' to not be greater than `{expectation}'"

            if self.actual > expectation:
                raise AssertionError(msg)

        else:
            msg = f"{self.__caller__.display_info} expects `{self.actual}' to be greater than `{expectation}'"
            if not self.actual > expectation:
                raise AssertionError(msg)

        return True

    @assertionmethod
    def greater_than_or_equal_to(self, expectation):
        if self.negative:
            if self.actual >= expectation:
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to not be greater than or equal to `{expectation}'")

        else:
            if not self.actual >= expectation:
                raise AssertionError(
                    f"{self.__caller__.display_info} expects `{self.actual}' to be greater than or equal to `{expectation}'"
                )

        return True

    @assertionmethod
    def lower_than(self, expectation):
        if self.negative:
            if self.actual < expectation:
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to not be lower than `{expectation}'")

        else:
            if not self.actual < expectation:
                raise AssertionError(f"{self.__caller__.display_info} expects `{self.actual}' to be lower than `{expectation}'")

        return True

    @assertionmethod
    def lower_than_or_equal_to(self, expectation):
        if self.negative:
            if self.actual <= expectation:
                raise AssertionError(
                    f"{self.__caller__.display_info} expects `{self.actual}' to not be lower than or equal to `{expectation}'"
                )

        else:
            if not self.actual <= expectation:
                raise AssertionError(
                    f"{self.__caller__.display_info} expects `{self.actual}' to be lower than or equal to `{expectation}'"
                )

        return True

    @assertionmethod
    def below(self, expectation):
        if self.negative:
            if self.actual < expectation:
                raise AssertionError(f"{self.actual} should not be below {expectation}")
        else:
            if not self.actual < expectation:
                raise AssertionError(f"{self.actual} should be below {expectation}")

        return True

    @assertionmethod
    def above(self, expectation):
        if self.negative:
            if self.actual > expectation:
                raise AssertionError(
                    f"{self.actual} should not be above {expectation}"
                )
        else:
            if not self.actual > expectation:
                raise AssertionError(f"{self.actual} should be above {expectation}")

        return True

    @assertionmethod
    def length_of(self, expectation):
        if self.negative:
            return self._that.len_is_not(expectation)

        return self._that.len_is(expectation)

    def called_with(self, *args, **kw):
        self._callable_args = args
        self._callable_kw = kw
        return self

    called = builtins.property(called_with)

    @assertionmethod
    def throw(self, *args, **kw):
        _that = AssertionHelper(
            self.actual, with_args=self._callable_args, and_kws=self._callable_kw
        )

        if self.negative:
            msg = (
                "{0} called with args {1} and keyword-args {2} should "
                "not raise {3} but raised {4}"
            )

            exc = args and args[0] or Exception
            try:
                self.actual(*self._callable_args, **self._callable_kw)
                return True
            except Exception as e:
                err = msg.format(
                    self.actual,
                    self._that._callable_args,
                    self._that._callable_kw,
                    exc,
                    e,
                )
                raise AssertionError(err)

        return _that.raises(*args, **kw)

    thrown = throw
    raises = thrown
    raised = thrown

    @assertionmethod
    def return_value(self, value):
        return_value = self.actual(*self._callable_args, **self._callable_kw)
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
                msg = "%r should not look like %r but does"
                raise AssertionError(msg % (self.actual, value))

        return self._that.looks_like(value)

    @assertionmethod
    def contain(self, expectation):
        actual = self.actual
        if self.negative:
            return expect(expectation).to.not_be.within(actual)
        else:
            return expect(expectation).to.be.within(actual)

    @assertionmethod
    def match(self, regex, *args):
        if not isinstance(
            self.actual, str
        ):
            raise f"{repr(self.actual)} should be a string in order to compare using .match()"
        matched = re.search(regex, self.actual, *args)

        modifiers_map = {
            re.I: "i",
            re.L: "l",
            re.M: "m",
            re.S: "s",
            re.U: "u",
        }
        modifiers = "".join(filter(bool, [modifiers_map.get(x, "") for x in args]))
        regex_representation = "/{0}/{1}".format(regex, modifiers)

        if self.negative:
            if matched is not None:
                raise AssertionError(
                    f"{repr(self.actual)} should not match the regular expression {regex_representation}"
                )

        else:
            if matched is None:
                raise AssertionError(
                    f"{repr(self.actual)} doesn't match the regular expression {regex_representation}"
                )

        return True


class ObjectIdentityAssertion(object):
    """Accompanies :class:`AssertionBuilder` in checking whether the
    actual object is entirely identical to the destination object,
    raising a :exc:`AssertionError` in case of identity mismatch.
    """
    def __init__(self, assertion_builder: AssertionBuilder):
        self.assertion_builder = assertion_builder

    def __call__(self, expectation):
        if self.assertion_builder.negative:
            return self.assure_nonidentical(expectation)
        else:
            return self.assure_identical(expectation)

    def assure_nonidentical(self, nonidentical):
        if self.assertion_builder.actual is nonidentical:
            raise AssertionError(
                f"{self.assertion_builder.actual} should not be the same object as {nonidentical}"
            )
        else:
            return True

    def assure_identical(self, identical):
        if self.assertion_builder.actual is not identical:
            raise AssertionError(
                f"{self.assertion_builder.actual} should be the same object as {identical}"
            )
        else:
            return True

    def __getattr__(self, name):
        return getattr(self.assertion_builder, name)

    def __repr__(self):
        return f"<ObjectIdentityAssertion assertion_builder={repr(self.assertion_builder)}>"


assert_that = AssertionBuilder("assert_that")
it = AssertionBuilder("it")
expect = AssertionBuilder("expect")
expects = AssertionBuilder("expect")
that = AssertionBuilder("that")
the = AssertionBuilder("the")
these = AssertionBuilder("these")
this = AssertionBuilder("this")
those = AssertionBuilder("those")


def assertion(func):
    """Extends :mod:`sure` with a custom assertion method."""
    func = assertionmethod(func)
    setattr(AssertionBuilder, func.__name__, func)
    return func


def chain(func):
    """Extends :mod:`sure` with a custom chaining method."""
    setattr(AssertionBuilder, func.__name__, func)
    return func


def chainproperty(func):
    """Extends :mod:`sure` with a custom chain property."""
    func = assertionproperty(func)
    setattr(AssertionBuilder, func.fget.__name__, func)
    return func


class ensure(object):
    """A :external+python:ref:`context-managers` that catches
:exc:`AssertionError` raised within it, substituting that initial
:exc:`AssertionError` one that contains the positional arguments and
keyword arguments passed to the context-manager.

    :param msg: :class:`str` passed to the :exc:`AssertionError`
    :param args: positional arguments used to format the assertion error message
    :param kws: keyword arguments used to format the assertion error message

    The `args'` and '`kws'` are used to format
    the message using :meth:`str.format`.
    """

    def __init__(self, msg, *args, **kws):
        self.msg = msg
        self.args = args
        self.kws = kws

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Catch all `AsertionError' exceptions and reraise them with
        the message provided to the context manager.
        """
        if exc_type is not AssertionError:
            return

        msg = self.msg.format(*self.args, **self.kws)
        raise AssertionError(msg)


old_dir = dir


def enable_special_syntax():
    """enables :mod:`sure`'s :ref:`Special Syntax`

    .. danger:: Enabling the special syntax in production code may cause unintended consequences.
    """
    @wraps(builtins.dir)
    def _new_dir(*obj):
        if not obj:
            frame = inspect.currentframe()
            return sorted(frame.f_back.f_locals.keys())

        if len(obj) > 1:
            raise TypeError(
                f"builtins.dir expected at most 1 arguments, got {len(obj)}"
            )
        patched = []
        try:
            import pytest
        except ImportError:
            pytest = None

        if not pytest:
            try:
                patched = [
                    x
                    for x in old_dir(obj[0])
                    if isinstance(getattr(obj[0], x, None), AssertionBuilder)
                ]
            except Exception:
                pass
        return sorted(set(old_dir(obj[0])).difference(set(patched)))

    builtins.dir = _new_dir

    def make_safe_property(method, name, should_be_property=True):
        if not should_be_property:
            return method(None)

        def deleter(method, self, *args, **kw):
            if isinstance(self, type):
                # In the event of deleting attributes from a "class
                # object" the call to ``self.__dict__.pop(name)`` would
                # not work because that would be equivalent to modifying a
                # mappingproxy object directly. Instead the expected
                # behavior is achieved in deleting the attribute
                # inside the ``overwritten_object_handlers`` dict.
                overwritten_object_handlers.pop((id(self), method.__name__), None)
            else:
                # Nevertheless, in the event of deleting attributes
                # from an "instance object the expected behavior is
                # achieved in a more common and straightforward
                # manner: pop directly at the instance's __dict__
                self.__dict__.pop(name, None)

        def setter(method, self, value):
            if isinstance(self, type):
                # In the event of setting attributes from a "class
                # object" the direct assignment ``self.__dict__[name] = value`` would
                # not work because that would be equivalent to modifying a
                # mappingproxy object directly. Instead the expected
                # behavior is achieved in deleting the attribute
                # inside the ``overwritten_object_handlers`` dict.
                overwritten_object_handlers[(id(self), method.__name__)] = value
            else:
                # Nevertheless, in the event of deleting attributes
                # from an "instance object the expected behavior is
                # achieved in a more common and straightforward
                # manner: set the attribute directly at instance's
                # __dict__
                self.__dict__[name] = value

        return builtins.property(
            fget=method,
            fset=partial(setter, method),
            fdel=partial(deleter, method),
        )

    def build_assertion_property(name, is_negative, prop=True):
        """Build assertion property

        This is the assertion property which is usually patched
        to the built-in '`object'` and '`NoneType'`.
        """

        def method(self):
            # avoid overwriting, patching attributes, methods or
            # properties that already exist in the type's __dict__
            try:
                if name in self.__dict__:
                    return self.__dict__[name]
            except AttributeError:
                # nevertheless objects that do not have a __dict__ can be patched
                pass

            overwritten_object_handler = overwritten_object_handlers.get(
                (id(self), name), None
            )
            if overwritten_object_handler:
                return overwritten_object_handler

            builder = AssertionBuilder(name, negative=is_negative)
            instance = builder(self)
            callable_args = getattr(self, "_callable_args", ())
            if callable_args:
                instance._callable_args = callable_args
            callable_kw = getattr(self, "_callable_kw", {})
            if callable_kw:
                instance._callable_kw = callable_kw
            return instance

        method.__name__ = name
        return make_safe_property(method, name, prop)

    object_handler = patchable_builtin(object)
    # Keeping track of all special properties of both `POSITIVES' and
    # `NEGATIVES' categories is paramount to avoid losing the newly
    # assigned object reference in the ``setter`` function within the
    # ``make_safe_property`` function.
    overwritten_object_handlers = {}

    # The `None' type does not have a "tp_dict" associated to its
    # PyObject. One way to patch Nonetypes is via its ``__class__``
    # attribute.
    none = patchable_builtin(None.__class__)

    for name in POSITIVES:
        object_handler[name] = build_assertion_property(name, is_negative=False)
        none[name] = build_assertion_property(name, is_negative=False, prop=False)

    for name in NEGATIVES:
        object_handler[name] = build_assertion_property(name, is_negative=True)
        none[name] = build_assertion_property(name, is_negative=not False, prop=False)

    _registry['special_syntax_enabled'] = not False


POSITIVES = [
    "do",
    "does",
    "must",
    "should",
    "when",
]

NEGATIVES = [
    "do_not",
    "dont",
    "does_not",
    "doesnt",
    "must_not",
    "mustnt",
    "should_not",
    "shouldnt",
]

registry.KNOWN_ASSERTIONS.extend(POSITIVES)
registry.KNOWN_ASSERTIONS.extend(NEGATIVES)


def is_special_syntax_enabled():
    return _registry.get('special_syntax_enabled')
