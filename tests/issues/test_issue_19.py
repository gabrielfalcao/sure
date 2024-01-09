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

"""
Test fix of bug described in GitHub Issue #19.
"""

from sure import expect, AssertionBuilder
from sure.special import is_cpython


def test_issue_19():
    "Allow monkey-patching of methods already implemented by sure."

    class Foo(object):
        pass

        @property
        def should(self):
            return 42

    instance = Foo()
    instance.do = "anything"
    instance.doesnt = "foo"

    expect(instance.do).should.be.equal("anything")
    expect(instance.doesnt).should.be.equal("foo")

    if is_cpython:
        instance2 = Foo()
        instance2.do.shouldnt.be.equal("anything")
        instance.does.__class__.should.be.equal(AssertionBuilder)

    # remove attribute
    del instance.do

    if is_cpython:
        instance.do.shouldnt.be.equal("anything")
    else:
        expect(instance).shouldnt.have.property("do")

    if is_cpython:
        Foo.shouldnt.__class__.should.be.equal(AssertionBuilder)

    Foo.shouldnt = "bar"
    expect(Foo.shouldnt).should.be.equal("bar")
    del Foo.shouldnt

    if is_cpython:
        Foo.shouldnt.__class__.should.be.equal(AssertionBuilder)
    else:
        expect(Foo).shouldnt.have.property("shouldnt")


    expect(instance.should).should.be.equal(42)
