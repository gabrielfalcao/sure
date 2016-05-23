## #!/usr/bin/env python
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
import mock
from datetime import datetime
from sure import this, these, those, it, expect, AssertionBuilder
from six import PY3
from sure.compat_py3 import compat_repr


def test_assertion_builder_synonyms():
    ("this, it, these and those are all synonyms")

    assert isinstance(it, AssertionBuilder)
    assert isinstance(this, AssertionBuilder)
    assert isinstance(these, AssertionBuilder)
    assert isinstance(those, AssertionBuilder)


def test_4_equal_2p2():
    ("this(4).should.equal(2 + 2)")

    time = datetime.now()

    assert this(4).should.equal(2 + 2)
    assert this(time).should_not.equal(datetime.now())

    def opposite():
        assert this(4).should.equal(8)

    def opposite_not():
        assert this(4).should_not.equal(4)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("X is 4 whereas Y is 8")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "4 should differ from 4, but is the same thing")


def test_2_within_0a2():
    ("this(1).should.be.within(0, 2)")

    assert this(1).should.be.within(0, 2)
    assert this(4).should_not.be.within(0, 2)

    def opposite():
        assert this(1).should.be.within(2, 4)

    def opposite_not():
        assert this(1).should_not.be.within(0, 2)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expected 1 to be within 2 and 4")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expected 1 to NOT be within 0 and 2")


def test_true_be_ok():
    ("this(True).should.be.ok")

    assert this(True).should.be.ok
    assert this(False).should_not.be.ok

    def opposite():
        assert this(False).should.be.ok

    def opposite_not():
        assert this(True).should_not.be.ok

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expected `False` to be truthy")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expected `True` to be falsy")


def test_false_be_falsy():
    ("this(False).should.be.false")

    assert this(False).should.be.falsy
    assert this(True).should_not.be.falsy

    def opposite():
        assert this(True).should.be.falsy

    def opposite_not():
        assert this(False).should_not.be.falsy

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expected `True` to be falsy")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expected `False` to be truthy")


def test_none():
    ("this(None).should.be.none")

    assert this(None).should.be.none
    assert this(not None).should_not.be.none

    def opposite():
        assert this("cool").should.be.none

    def opposite_not():
        assert this(None).should_not.be.none

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expected `cool` to be None")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expected `None` to not be None")


def test_should_be_a():
    ("this(None).should.be.none")

    assert this(1).should.be.an(int)
    assert this([]).should.be.a('collections.Iterable')
    assert this({}).should_not.be.a(list)

    def opposite():
        assert this(1).should_not.be.an(int)

    def opposite_not():
        assert this([]).should_not.be.a('list')

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expected `1` to not be an int")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expected `[]` to not be a list")


def test_should_be_callable():
    ("this(function).should.be.callable")

    assert this(lambda: None).should.be.callable
    assert this("aa").should_not.be.callable

    def opposite():
        assert this("foo").should.be.callable

    def opposite_not():
        assert this(opposite).should_not.be.callable

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(compat_repr(
        "expected 'foo' to be callable"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "expected `{0}` to not be callable but it is".format(repr(opposite)))


def test_iterable_should_be_empty():
    ("this(iterable).should.be.empty")

    assert this([]).should.be.empty
    assert this([1, 2, 3]).should_not.be.empty

    def opposite():
        assert this([3, 2, 1]).should.be.empty

    def opposite_not():
        assert this({}).should_not.be.empty

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expected `[3, 2, 1]` to be empty but it has 3 items")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expected `{}` to not be empty")


def test_iterable_should_have_length_of():
    ("this(iterable).should.have.length_of(N)")

    assert this({'foo': 'bar', 'a': 'b'}).should.have.length_of(2)
    assert this([1, 2, 3]).should_not.have.length_of(4)

    def opposite():
        assert this(('foo', 'bar', 'a', 'b')).should.have.length_of(1)

    def opposite_not():
        assert this([1, 2, 3]).should_not.have.length_of(3)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(compat_repr(
        "the length of ('foo', 'bar', 'a', 'b') should be 1, but is 4"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "the length of [1, 2, 3] should not be 3")


def test_greater_than():
    ("this(X).should.be.greater_than(Y)")

    assert this(5).should.be.greater_than(4)
    assert this(1).should_not.be.greater_than(2)

    def opposite():
        assert this(4).should.be.greater_than(5)

    def opposite_not():
        assert this(2).should_not.be.greater_than(1)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expected `4` to be greater than `5`")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "expected `2` to not be greater than `1`")


def test_greater_than_or_equal_to():
    ("this(X).should.be.greater_than_or_equal_to(Y)")

    assert this(4).should.be.greater_than_or_equal_to(4)
    assert this(1).should_not.be.greater_than_or_equal_to(2)

    def opposite():
        assert this(4).should.be.greater_than_or_equal_to(5)

    def opposite_not():
        assert this(2).should_not.be.greater_than_or_equal_to(1)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expected `4` to be greater than or equal to `5`")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "expected `2` to not be greater than or equal to `1`")


def test_lower_than():
    ("this(X).should.be.lower_than(Y)")

    assert this(4).should.be.lower_than(5)
    assert this(2).should_not.be.lower_than(1)

    def opposite():
        assert this(5).should.be.lower_than(4)

    def opposite_not():
        assert this(1).should_not.be.lower_than(2)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expected `5` to be lower than `4`")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "expected `1` to not be lower than `2`")


def test_lower_than_or_equal_to():
    ("this(X).should.be.lower_than_or_equal_to(Y)")

    assert this(5).should.be.lower_than_or_equal_to(5)
    assert this(2).should_not.be.lower_than_or_equal_to(1)

    def opposite():
        assert this(5).should.be.lower_than_or_equal_to(4)

    def opposite_not():
        assert this(1).should_not.be.lower_than_or_equal_to(2)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expected `5` to be lower than or equal to `4`")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "expected `1` to not be lower than or equal to `2`")


def test_be():
    ("this(X).should.be(X) when X is a reference to the same object")

    d1 = {}
    d2 = d1
    d3 = {}

    assert isinstance(this(d2).should.be(d1), bool)
    assert this(d2).should.be(d1)
    assert this(d3).should_not.be(d1)

    def wrong_should():
        return this(d3).should.be(d1)

    def wrong_should_not():
        return this(d2).should_not.be(d1)

    wrong_should_not.when.called.should.throw(
        AssertionError,
        '{} should not be the same object as {}, but it is',
    )
    wrong_should.when.called.should.throw(
        AssertionError,
        '{} should be the same object as {}, but it is not',
    )


def test_have_property():
    ("this(instance).should.have.property(property_name)")

    class Person(object):
        name = "John Doe"

        def __repr__(self):
            return r"Person()"

    jay = Person()

    assert this(jay).should.have.property("name")
    assert this(jay).should_not.have.property("age")

    def opposite():
        assert this(jay).should_not.have.property("name")

    def opposite_not():
        assert this(jay).should.have.property("age")

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(compat_repr(
        "Person() should not have the property `name`, but it is 'John Doe'"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "Person() should have the property `age` but does not")


def test_have_property_with_value():
    ("this(instance).should.have.property(property_name).being or "
     ".with_value should allow chain up")

    class Person(object):
        name = "John Doe"

        def __repr__(self):
            return r"Person()"

    jay = Person()

    assert this(jay).should.have.property("name").being.equal("John Doe")
    assert this(jay).should.have.property("name").not_being.equal("Foo")

    def opposite():
        assert this(jay).should.have.property("name").not_being.equal(
            "John Doe")

    def opposite_not():
        assert this(jay).should.have.property("name").being.equal(
            "Foo")

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(compat_repr(
        "'John Doe' should differ from 'John Doe', but is the same thing"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(compat_repr(
        "X is 'John Doe' whereas Y is 'Foo'"))


def test_have_key():
    ("this(dictionary).should.have.key(key_name)")

    jay = {'name': "John Doe"}

    assert this(jay).should.have.key("name")
    assert this(jay).should_not.have.key("age")

    def opposite():
        assert this(jay).should_not.have.key("name")

    def opposite_not():
        assert this(jay).should.have.key("age")

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(compat_repr(
        "{'name': 'John Doe'} should not have the key `name`, "
        "but it is 'John Doe'"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(compat_repr(
        "{'name': 'John Doe'} should have the key `age` but does not"))


def test_have_key_with_value():
    ("this(dictionary).should.have.key(key_name).being or "
     ".with_value should allow chain up")

    jay = dict(name="John Doe")

    assert this(jay).should.have.key("name").being.equal("John Doe")
    assert this(jay).should.have.key("name").not_being.equal("Foo")

    def opposite():
        assert this(jay).should.have.key("name").not_being.equal(
            "John Doe")

    def opposite_not():
        assert this(jay).should.have.key("name").being.equal(
            "Foo")

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(compat_repr(
        "'John Doe' should differ from 'John Doe', but is the same thing"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(compat_repr(
        "X is 'John Doe' whereas Y is 'Foo'"))


def test_look_like():
    ("this('   aa  \n  ').should.look_like('aa')")

    assert this('   \n  aa \n  ').should.look_like('AA')
    assert this('   \n  bb \n  ').should_not.look_like('aa')

    def opposite():
        assert this('\n aa \n').should.look_like('bb')

    def opposite_not():
        assert this('\n aa \n').should_not.look_like('aa')

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(compat_repr(r"'\n aa \n' does not look like 'bb'"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(compat_repr(r"'\n aa \n' should not look like 'aa' but does"))


def test_equal_with_repr_of_complex_types_and_unicode():
    ("test usage of repr() inside expect(complex1).to.equal(complex2)")

    class Y(object):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            if PY3:
                # PY3K should return the regular (unicode) string
                return self.x
            else:
                return self.x.encode('utf-8')

        def __eq__(self, other):
            return self.x == other.x

    y1 = dict(
        a=2,
        b=Y('Gabriel Falcão'),
        c='Foo',
    )

    expect(y1).to.equal(dict(
        a=2,
        b=Y('Gabriel Falcão'),
        c='Foo',
    ))


def test_equal_with_repr_of_complex_types_and_repr():
    ("test usage of repr() inside expect(complex1).to.equal(complex2)")

    class Y(object):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            if PY3:
                # PY3K should return the regular (unicode) string
                return self.x
            else:
                return self.x.encode('utf-8')

        def __eq__(self, other):
            return self.x == other.x

    y1 = {
        'a': 2,
        'b': Y('Gabriel Falcão'),
        'c': 'Foo',
    }

    expect(y1).to.equal({
        'a': 2,
        'b': Y('Gabriel Falcão'),
        'c': 'Foo',
    })

    expect(y1).to_not.equal({
        'a': 2,
        'b': Y('Gabriel Falçao'),
        'c': 'Foo',
    })

    def opposite():
        expect(y1).to.equal({
            'a': 2,
            'b': Y('Gabriel Falçao'),
            'c': 'Foo',
        })

    def opposite_not():
        expect(y1).to_not.equal({
            'a': 2,
            'b': Y('Gabriel Falcão'),
            'c': 'Foo',
        })

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(compat_repr("X['b'] != Y['b']"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(compat_repr(
        "{'a': 2, 'b': Gabriel Falcão, 'c': 'Foo'} should differ from {'a': 2, 'b': Gabriel Falcão, 'c': 'Foo'}, but is the same thing"))


def test_match_regex():
    ("expect('some string').to.match(r'\w{4} \w{6}') matches regex")

    assert this("some string").should.match(r"\w{4} \w{6}")
    assert this("some string").should_not.match(r"^\d*$")

    def opposite():
        assert this("some string").should.match(r"\d{2} \d{4}")

    def opposite_not():
        assert this("some string").should_not.match(r"some string")

    expect(opposite).when.called.to.throw(
        AssertionError,
        "'some string' doesn't match the regular expression /\d{2} \d{4}/")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "'some string' should not match the regular expression /some string/")


def test_match_contain():
    ("expect('some string').to.contain('tri')")

    assert this("some string").should.contain("tri")
    assert this("some string").should_not.contain('foo')

    def opposite():
        assert this("some string").should.contain("bar")

    def opposite_not():
        assert this("some string").should_not.contain(r"string")

    expect(opposite).when.called.to.throw(AssertionError)
    if PY3:
        expect(opposite).when.called.to.throw(
            "'bar' should be in 'some string'")
    else:
        expect(opposite).when.called.to.throw(
            "u'bar' should be in u'some string'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    if PY3:
        expect(opposite_not).when.called.to.throw(
            "'string' should NOT be in 'some string'")
    else:
        expect(opposite_not).when.called.to.throw(
            "u'string' should NOT be in u'some string'")


def test_catching_exceptions():

    # Given that I have a function that raises an exceptiont that does *not*
    # inherit from the `Exception` class
    def blah():
        raise SystemExit(2)

    # When I call it testing which exception it's raising, Then it should be
    # successful
    expect(blah).when.called_with().should.throw(SystemExit)


def test_catching_exceptions_with_params():

    # Given that I have a function that raises an exceptiont that does *not*
    # inherit from the `Exception` class
    def blah(foo):
        raise SystemExit(2)

    # When I call it testing which exception it's raising, Then it should be
    # successful
    expect(blah).when.called_with(0).should.throw(SystemExit)


def test_success_with_params():
    def blah(foo):
        pass

    expect(blah).when.called_with(0).should_not.throw(TypeError)


def test_success_with_params_exception():
    def blah():
        pass

    expect(blah).when.called_with(0).should.throw(TypeError)


def test_throw_matching_regex():
    def blah(num):
        if num == 1:
            msg = 'this message'
        else:
            msg = 'another thing'

        raise ValueError(msg)

    expect(blah).when.called_with(1).should.throw(ValueError, 'this message')
    expect(blah).when.called_with(1).should.throw(re.compile(r'(this message|another thing)'))
    expect(blah).when.called_with(2).should.throw(ValueError, 'another thing')
    expect(blah).when.called_with(2).should.throw(ValueError, re.compile(r'(this message|another thing)'))

    try:
        expect(blah).when.called_with(1).should.throw(re.compile(r'invalid regex'))
        raise RuntimeError('should not have reached here')

    except AssertionError as e:
        if PY3:
            expect(str(e)).to.equal("When calling b'blah [tests/test_assertion_builder.py line 633]' the exception message does not match. Expected to match regex: 'invalid regex'\n against:\n 'this message'")
        else:
            expect(str(e)).to.equal("When calling 'blah [tests/test_assertion_builder.py line 633]' the exception message does not match. Expected to match regex: u'invalid regex'\n against:\n u'this message'")

    try:
        expect(blah).when.called_with(1).should.throw(ValueError, re.compile(r'invalid regex'))
        raise RuntimeError('should not have reached here')
    except AssertionError as e:
        if PY3:
            expect(str(e)).to.equal("When calling b'blah [tests/test_assertion_builder.py line 633]' the exception message does not match. Expected to match regex: 'invalid regex'\n against:\n 'this message'")
        else:
            expect(str(e)).to.equal("When calling 'blah [tests/test_assertion_builder.py line 633]' the exception message does not match. Expected to match regex: u'invalid regex'\n against:\n u'this message'")

def test_should_not_be_different():
    ("'something'.should_not.be.different('SOMETHING'.lower())")

    part1 = '''<root>
  <a-tag with-attribute="one">AND A VALUE</a-tag>
</root>'''

    part2 = '''<root>
  <a-tag with-attribute="two">AND A VALUE</a-tag>
</root>'''

    assert this(part1).should.be.different_of(part2)
    assert this(part2).should_not.be.different_of(part2)

    def opposite():
        assert this(part2).should.be.different_of(part2)

    def opposite_not():
        assert this(part1).should_not.be.different_of(part2)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw('''<root>
  <a-tag with-attribute="two">AND A VALUE</a-tag>
</root> should be different of <root>
  <a-tag with-attribute="two">AND A VALUE</a-tag>
</root>''')

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw('''Difference:

  <root>
-   <a-tag with-attribute="one">AND A VALUE</a-tag>
?                           --
+   <a-tag with-attribute="two">AND A VALUE</a-tag>
?                          ++
  </root>''')


def test_equals_handles_mock_call_list():
    ".equal() Should convert mock._CallList instances to lists"

    # Given the following mocked callback
    callback = mock.Mock()

    # When I call the callback with a few parameters twice
    callback(a=1, b=2)
    callback(a=3, b=4)

    # Then I see I can compare the call list without manually
    # converting anything

    callback.call_args_list.should.equal([
        mock.call(a=1, b=2),
        mock.call(a=3, b=4),
    ])


def test_equals_handles_float_with_epsilon():
    ".equal(what, epsilon=XXX) should check for equality with an epsilon for float values"
    float1 = 4.242423
    float2 = 4.242420

    expect(float1).should_not.be.equal(float2)
    expect(float1).should.be.equal(float2, epsilon=0.000005)

    float_list1 = [4.242421, 4.242422, 4.242423, 4.242424, 4.242425]
    float_list2 = [4.242420, 4.242420, 4.242420, 4.242420, 4.242420]

    expect(float_list1).should_not.be.equal(float_list2)
    expect(float_list1).should.be.equal(float_list2, epsilon=0.000005)

    float_dict1 = {"f1": 4.242421, "f2": 4.242422, "f3": 4.242423, "f4": 4.242424, "f5": 4.242425}
    float_dict2 = {"f1": 4.242420, "f2": 4.242420, "f3": 4.242420, "f4": 4.242420, "f5": 4.242420}

    expect(float_dict1).should_not.be.equal(float_dict2)
    expect(float_dict1).should.be.equal(float_dict2, epsilon=0.000005)


def test_equals_dictionaries_with_tuple_keys():
    ('.equal() with dict containing tuples as keys should work')

    X = {
        ("0.0.0.0", 3478): "chuck norris",
    }

    Y = {
        ("0.0.0.0", 400): "chuck norris",
    }

    X.should_not.equal(Y)
    Y.should_not.equal(X)
