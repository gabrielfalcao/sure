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
from datetime import datetime
from sure import this, these, those, it, expect, AssertionBuilder
from sure.six import PY3, compat_repr


def test_assertion_builder_synonyms():
    (u"this, it, these and those are all synonyms")

    assert isinstance(it, AssertionBuilder)
    assert isinstance(this, AssertionBuilder)
    assert isinstance(these, AssertionBuilder)
    assert isinstance(those, AssertionBuilder)


def test_4_equal_2p2():
    (u"this(4).should.equal(2 + 2)")

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
        "4 should differ to 4, but is the same thing")


def test_2_within_0a2():
    (u"this(1).should.be.within(0, 2)")

    assert this(1).should.be.within(0, 2)
    assert this(4).should_not.be.within(0, 2)

    def opposite():
        assert this(1).should.be.within(2, 4)

    def opposite_not():
        assert this(1).should_not.be.within(0, 2)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("1 should be in [2, 3]")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("1 should NOT be in [0, 1]")


def test_true_be_ok():
    (u"this(True).should.be.ok")

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
    (u"this(False).should.be.false")

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
    (u"this(None).should.be.none")

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
    (u"this(None).should.be.none")

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
    (u"this(function).should.be.callable")

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
    (u"this(iterable).should.be.empty")

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
    (u"this(iterable).should.have.length_of(N)")

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
    (u"this(X).should.be.greater_than(Y)")

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
    (u"this(X).should.be.greater_than_or_equal_to(Y)")

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
    (u"this(X).should.be.lower_than(Y)")

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
    (u"this(X).should.be.lower_than_or_equal_to(Y)")

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


def test_have_property():
    (u"this(instance).should.have.property(property_name)")

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
    (u"this(instance).should.have.property(property_name).being or "
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
        "'John Doe' should differ to 'John Doe', but is the same thing"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(compat_repr(
        "X is 'John Doe' whereas Y is 'Foo'"))


def test_have_key():
    (u"this(dictionary).should.have.key(key_name)")

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
    (u"this(dictionary).should.have.key(key_name).being or "
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
        "'John Doe' should differ to 'John Doe', but is the same thing"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(compat_repr(
        "X is 'John Doe' whereas Y is 'Foo'"))


def test_look_like():
    (u"this('   aa  \n  ').should.look_like('aa')")

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
    (u"test usage of repr() inside expect(complex1).to.equal(complex2)")

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
        b=Y(u'Gabriel Falcão'),
        c='Foo',
    )

    expect(y1).to.equal(dict(
        a=2,
        b=Y(u'Gabriel Falcão'),
        c='Foo',
    ))


def test_equal_with_repr_of_complex_types_and_repr():
    (u"test usage of repr() inside expect(complex1).to.equal(complex2)")

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
        'b': Y(u'Gabriel Falcão'),
        'c': 'Foo',
    }

    expect(y1).to.equal({
        'a': 2,
        'b': Y(u'Gabriel Falcão'),
        'c': 'Foo',
    })

    expect(y1).to_not.equal({
        'a': 2,
        'b': Y(u'Gabriel Falçao'),
        'c': 'Foo',
    })

    def opposite():
        expect(y1).to.equal({
            'a': 2,
            'b': Y(u'Gabriel Falçao'),
            'c': 'Foo',
        })

    def opposite_not():
        expect(y1).to_not.equal({
            'a': 2,
            'b': Y(u'Gabriel Falcão'),
            'c': 'Foo',
        })

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(compat_repr("X['b'] != Y['b']"))

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(compat_repr(
        u"{'a': 2, 'b': Gabriel Falcão, 'c': 'Foo'} should differ to {'a': 2, 'b': Gabriel Falcão, 'c': 'Foo'}, but is the same thing"))


def test_match_regex():
    (u"expect('some string').to.match(r'\w{4} \w{6}') matches regex")

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
    (u"expect('some string').to.contain('tri')")

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
