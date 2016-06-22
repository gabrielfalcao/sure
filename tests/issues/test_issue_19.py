# -*- coding: utf-8 -*-

"""
Test fix of bug described in GitHub Issue #19.
"""

from sure import expect, AssertionBuilder
from sure.magic import is_cpython


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
