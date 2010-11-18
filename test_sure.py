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

import sure
from sure import that
from threading import local
from nose.tools import assert_equals, assert_raises

def test_setup_with_context():
    "sure.with_context() runs setup before the function itself"

    def setup(context):
        context.name = "John Resig"

    @sure.that_with_context(setup)
    def john_is_within_context(context):
        assert isinstance(context, local)
        assert hasattr(context, "name")

    john_is_within_context()
    assert_equals(
        john_is_within_context.__name__,
        'test_john_is_within_context'
    )

def test_teardown_with_context():
    "sure.with_context() runs teardown before the function itself"

    class something:
        pass

    def setup(context):
        something.modified = True

    def teardown(context):
        del something.modified

    @sure.that_with_context(setup, teardown)
    def something_was_modified(context):
        assert hasattr(something, "modified")
        assert something.modified

    something_was_modified()
    assert not hasattr(something, "modified")

def test_that_is_a():
    "sure.that() is_a(object)"

    something = "something"

    assert that(something).is_a(str)
    assert isinstance(something, str)

def test_that_equals():
    "sure.that() equals(object)"

    something = "something"

    assert that(something).equals(something)
    assert something == something

def test_that_differs():
    "sure.that() differs(object)"

    something = "something"

    assert that(something).differs("23123%FYTUGIHOfdf")
    assert something != "23123%FYTUGIHOfdf"

def test_that_has():
    "sure.that() has(object)"

    class Class:
        name = "some class"
    Object = Class()
    dictionary = {
        'name': 'John'
    }
    name = "john"

    assert hasattr(Class, 'name')
    assert that(Class).has("name")
    assert that(Class).like("name")
    assert "name" in sure.that(Class)

    assert hasattr(Object, 'name')
    assert that(Object).has("name")
    assert that(Object).like("name")
    assert "name" in sure.that(Object)

    assert dictionary.has_key('name')
    assert that(dictionary).has("name")
    assert that(dictionary).like("name")
    assert "name" in sure.that(dictionary)

    assert that(name).has("john")
    assert that(name).like("john")
    assert "john" in sure.that(name)
    assert that(name).has("hn")
    assert that(name).like("hn")
    assert "hn" in sure.that(name)
    assert that(name).has("jo")
    assert that(name).like("jo")
    assert "jo" in sure.that(name)

def test_that_len_is():
    "sure.that() len_is(number)"

    lst = range(1000)

    assert that(lst).len_is(1000)
    assert len(lst) == 1000
    assert that(lst).len_is(lst)

def test_that_len_greater_than():
    "sure.that() len_greater_than(number)"

    lst = range(1000)
    lst2 = range(100)

    assert that(lst).len_greater_than(100)
    assert len(lst) == 1000
    assert that(lst).len_greater_than(lst2)

def test_that_len_greater_than_should_raise_assertion_error():
    "sure.that() len_greater_than(number) raise AssertionError"

    lst = range(1000)
    try:
        that(lst).len_greater_than(1000)
    except AssertionError, e:
        assert_equals(str(e), 'the length of %r should be greater then %d, but is %d' % (lst, 1000, 1000))

def test_that_len_greater_than_or_equals():
    "sure.that() len_greater_than_or_equals(number)"

    lst = range(1000)
    lst2 = range(100)

    assert that(lst).len_greater_than_or_equals(100)
    assert that(lst).len_greater_than_or_equals(1000)
    assert len(lst) == 1000
    assert that(lst).len_greater_than_or_equals(lst2)
    assert that(lst).len_greater_than_or_equals(lst)

def test_that_len_greater_than_or_equals_should_raise_assertion_error():
    "sure.that() len_greater_than_or_equals(number) raise AssertionError"

    lst = range(1000)
    try:
        that(lst).len_greater_than_or_equals(1001)
    except AssertionError, e:
        assert_equals(str(e), 'the length of %r should be greater then or equals %d, but is %d' % (lst, 1001, 1000))

def test_that_len_lower_than():
    "sure.that() len_lower_than(number)"

    lst = range(100)
    lst2 = range(1000)

    assert that(lst).len_lower_than(101)
    assert len(lst) == 100
    assert that(lst).len_lower_than(lst2)

def test_that_len_lower_than_should_raise_assertion_error():
    "sure.that() len_lower_than(number) raise AssertionError"

    lst = range(1000)
    try:
        that(lst).len_lower_than(1000)
    except AssertionError, e:
        assert_equals(str(e), 'the length of %r should be lower then %d, but is %d' % (lst, 1000, 1000))

def test_that_len_lower_than_or_equals():
    "sure.that() len_lower_than_or_equals(number)"

    lst = range(1000)
    lst2 = range(1001)

    assert that(lst).len_lower_than_or_equals(1001)
    assert that(lst).len_lower_than_or_equals(1000)
    assert len(lst) == 1000
    assert that(lst).len_lower_than_or_equals(lst2)
    assert that(lst).len_lower_than_or_equals(lst)

def test_that_len_lower_than_or_equals_should_raise_assertion_error():
    "sure.that() len_lower_than_or_equals(number) raise AssertionError"

    lst = range(1000)
    try:
        that(lst).len_lower_than_or_equals(100)
    except AssertionError, e:
        assert_equals(str(e), 'the length of %r should be lower then or equals %d, but is %d' % (lst, 100, 1000))

def test_that_checking_all_atributes():
    "sure.that(iterable).the_attribute('name').equals('value')"
    class shape(object):
        def __init__(self, name):
            self.kind = 'geometrical form'
            self.name = name

    shapes = [
        shape('circle'),
        shape('square'),
        shape('rectangle'),
        shape('triangle')
    ]

    assert that(shapes).the_attribute("kind").equals('geometrical form')

def test_that_checking_all_atributes_of_range():
    "sure.that(iterable, within_range=(1, 2)).the_attribute('name').equals('value')"
    class shape(object):
        def __init__(self, name):
            self.kind = 'geometrical form'
            self.name = name
        def __repr__(self):
            return '<%s:%s>' % (self.kind, self.name)

    shapes = [
        shape('circle'),
        shape('square'),
        shape('square'),
        shape('triangle')
    ]

    assert shapes[0].name != 'square'
    assert shapes[3].name != 'square'

    assert shapes[1].name == 'square'
    assert shapes[2].name == 'square'

    assert that(shapes, within_range=(1, 2)).the_attribute("name").equals('square')

def test_that_checking_all_elements():
    "sure.that(iterable).every_one_is('value')"
    shapes = [
        'cube',
        'ball',
        'ball',
        'piramid'
    ]

    assert shapes[0] != 'ball'
    assert shapes[3] != 'ball'

    assert shapes[1] == 'ball'
    assert shapes[2] == 'ball'

    assert that(shapes, within_range=(1, 2)).every_one_is('ball')

def test_that_checking_each_matches():
    "sure.that(iterable).in_each('').equals('value')"
    class animal(object):
        def __init__(self, kind):
            self.attributes = {
                'class': 'mammal',
                'kind': kind,
            }

    animals = [
        animal('dog'),
        animal('cat'),
        animal('cow'),
        animal('cow'),
        animal('cow'),
    ]

    assert animals[0].attributes['kind'] != 'cow'
    assert animals[1].attributes['kind'] != 'cow'

    assert animals[2].attributes['kind'] == 'cow'
    assert animals[3].attributes['kind'] == 'cow'
    assert animals[4].attributes['kind'] == 'cow'

    assert animals[0].attributes['class'] == 'mammal'
    assert animals[1].attributes['class'] == 'mammal'
    assert animals[2].attributes['class'] == 'mammal'
    assert animals[3].attributes['class'] == 'mammal'
    assert animals[4].attributes['class'] == 'mammal'

    assert that(animals).in_each("attributes['class']").matches('mammal')
    assert that(animals).in_each("attributes['class']").matches(['mammal','mammal','mammal','mammal','mammal'])

    assert that(animals).in_each("attributes['kind']").matches(['dog','cat','cow','cow','cow'])

    try:
        assert that(animals).in_each("attributes['kind']").matches(['dog'])
        assert False, 'should not reach here'
    except AssertionError, e:
        assert that(unicode(e)).equals(
            '%r has 5 items, but the matching list has 1: %r' % (
                ['dog','cat','cow','cow','cow'], ['dog']
            )
        )

def test_that_raises():
    "sure.that(callable, with_args=[arg1], and_kwargs={'arg2': 'value'}).raises(SomeException)"

    def function(arg1=None, arg2=None):
        if arg1 == 1 and arg2 == 2:
            raise RuntimeError('yeah, it failed')

        return "OK"

    try:
        function(1, 2)
        assert False, 'should not reach here'

    except RuntimeError, e:
        assert unicode(e) == 'yeah, it failed'

    except Exception:
        assert False, 'should not reach here'

    assert_raises(RuntimeError, function, 1, 2)
    assert_equals(function(3, 5), 'OK')

    assert that(function, with_args=[1], and_kwargs={'arg2': 2}).raises(RuntimeError)
    assert that(function, with_args=[1], and_kwargs={'arg2': 2}).raises(RuntimeError, 'yeah, it failed')
    assert that(function, with_args=[1], and_kwargs={'arg2': 2}).raises('yeah, it failed')

    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}).raises(RuntimeError)
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}).raises(RuntimeError, 'yeah, it failed')
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}).raises('yeah, it failed')

def test_that_looks_like():
    "sure.that('String\\n with BREAKLINE').looks_like('string with breakline')"
    assert that('String\n with BREAKLINE').looks_like('string with breakline')

def test_that_raises_with_args():
    "sure.that(callable, with_args=['foo']).raises(FooError)"

    class FooError(Exception):
        pass

    def my_function(string):
        if string == 'foo':
            raise FooError('OOps')

    assert that(my_function, with_args=['foo']).raises(FooError, 'OOps')

def test_that_contains_string():
    "sure.that('foobar').contains('foo')"

    assert 'foo' in 'foobar'
    assert that('foobar').contains('foo')

def test_that_contains_none():
    "sure.that('foobar').contains(None)"

    try:
        assert that('foobar').contains(None)
        assert False, 'should not reach here'
    except Exception, e:
        assert_equals(unicode(e), u'None should be a string')

def test_that_none_contains_string():
    "sure.that(None).contains('bungalow')"

    try:
        assert that(None).contains('bungalow')
        assert False, 'should not reach here'
    except Exception, e:
        assert_equals(unicode(e), u'None is not a string, so is is impossible to check if "bungalow" is there')
