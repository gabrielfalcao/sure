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
