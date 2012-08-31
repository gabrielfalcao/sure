## #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - assertion toolbox>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from sure import this, these, those, it, that, AssertionBuilder


def test_assertion_builder_synonyms():
    (u"this, it, these and those are all synonyms")

    assert that(it).is_a(AssertionBuilder)
    assert that(this).is_a(AssertionBuilder)
    assert that(these).is_a(AssertionBuilder)
    assert that(those).is_a(AssertionBuilder)


def test_4_equal_2p2():
    (u"this(4).should.equal(2 + 2)")

    assert this(4).should.equal(2 + 2)
    assert this(4).should_not.equal(8)

    def opposite():
        assert this(4).should.equal(8)

    def opposite_not():
        assert this(4).should_not.equal(4)

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises("X is 4 whereas Y is 8")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises(
        "4 should differ to 4, but is the same thing")


def test_2_within_0a2():
    (u"this(1).should.be.within(0, 2)")

    assert this(1).should.be.within(0, 2)
    assert this(4).should_not.be.within(0, 2)

    def opposite():
        assert this(1).should.be.within(2, 4)

    def opposite_not():
        assert this(1).should_not.be.within(0, 2)

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises("1 should be in [2, 3]")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises("1 should NOT be in [0, 1]")


def test_true_be_ok():
    (u"this(True).should.be.ok")

    assert this(True).should.be.ok
    assert this(False).should_not.be.ok

    def opposite():
        assert this(False).should.be.ok

    def opposite_not():
        assert this(True).should_not.be.ok

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises("expected `False` to be truthy")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises("expected `True` to be falsy")


def test_false_be_falsy():
    (u"this(False).should.be.false")

    assert this(False).should.be.falsy
    assert this(True).should_not.be.falsy

    def opposite():
        assert this(True).should.be.falsy

    def opposite_not():
        assert this(False).should_not.be.falsy

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises("expected `True` to be falsy")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises("expected `False` to be truthy")


def test_none():
    (u"this(None).should.be.none")

    assert this(None).should.be.none
    assert this(not None).should_not.be.none

    def opposite():
        assert this("cool").should.be.none

    def opposite_not():
        assert this(None).should_not.be.none

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises("expected `cool` to be None")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises("expected `None` to not be None")


def test_should_be_a():
    (u"this(None).should.be.none")

    assert this(1).should.be.an(int)
    assert this([]).should.be.a('collections.Iterable')
    assert this({}).should_not.be.a(list)

    def opposite():
        assert this(1).should_not.be.an(int)

    def opposite_not():
        assert this([]).should_not.be.a('list')

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises("expected `1` to not be an int")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises("expected `[]` to not be a list")


def test_should_be_callable():
    (u"this(function).should.be.callable")

    assert this(lambda: None).should.be.callable
    assert this("aa").should_not.be.callable

    def opposite():
        assert this("foo").should.be.callable

    def opposite_not():
        assert this(opposite).should_not.be.callable

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises("expected 'foo' to be callable")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises(
        "expected `{0}` to not be callable but it is".format(repr(opposite)))


def test_iterable_should_be_empty():
    (u"this(iterable).should.be.empty")

    assert this([]).should.be.empty
    assert this([1, 2, 3]).should_not.be.empty

    def opposite():
        assert this([3, 2, 1]).should.be.empty

    def opposite_not():
        assert this({}).should_not.be.empty

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises(
        "expected `[3, 2, 1]` to be empty but it has 3 items")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises("expected `{}` to not be empty")


def test_iterable_should_have_length_of():
    (u"this(iterable).should.have.length_of(N)")

    assert this({'foo': 'bar', 'a': 'b'}).should.have.length_of(2)
    assert this([1, 2, 3]).should_not.have.length_of(4)

    def opposite():
        assert this(('foo', 'bar', 'a', 'b')).should.have.length_of(1)

    def opposite_not():
        assert this([1, 2, 3]).should_not.have.length_of(3)

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises(
        "the length of ('foo', 'bar', 'a', 'b') should be 1, but is 4")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises(
        "the length of [1, 2, 3] should not be 3")


def test_greater_than():
    (u"this(X).should.be.greater_than(Y)")

    assert this(5).should.be.greater_than(4)
    assert this(1).should_not.be.greater_than(2)

    def opposite():
        assert this(4).should.be.greater_than(5)

    def opposite_not():
        assert this(2).should_not.be.greater_than(1)

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises(
        "expected `4` to be greater than `5`")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises(
        "expected `2` to not be greater than `1`")


def test_lower_than():
    (u"this(X).should.be.lower_than(Y)")

    assert this(4).should.be.lower_than(5)
    assert this(2).should_not.be.lower_than(1)

    def opposite():
        assert this(5).should.be.lower_than(4)

    def opposite_not():
        assert this(1).should_not.be.lower_than(2)

    assert that(opposite).raises(AssertionError)
    assert that(opposite).raises(
        "expected `5` to be lower than `4`")

    assert that(opposite_not).raises(AssertionError)
    assert that(opposite_not).raises(
        "expected `1` to not be lower than `2`")
