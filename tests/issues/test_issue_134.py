# -*- coding: utf-8 -*-

"""
Test fix of bug described in GitHub Issue #19.
"""

from sure import expect


def test_issue_132():
    "Correctly handle % charachter in matcher string"

    def __great_test():
        expect('hello%world').should.be.equal('hello%other')

    expect(__great_test).when.called.to.throw(AssertionError, "X is 'hello%world' whereas Y is 'hello%other'")

    def __great_test_2():
        expect('hello{42}world').should.be.equal('hello{42}foo')

    expect(__great_test_2).when.called.to.throw(AssertionError, "X is 'hello{42}world' whereas Y is 'hello{42}foo'")

    def __great_test_3():
        expect('hello{42world }').should.be.equal('hello{42foo }')

    expect(__great_test_3).when.called.to.throw(AssertionError, "X is 'hello{42world }' whereas Y is 'hello{42foo }'")

    def __great_test_4():
        expect('hello{42world }}').should.be.equal('hello{42foo }}')

    expect(__great_test_4).when.called.to.throw(AssertionError, "X is 'hello{42world }}' whereas Y is 'hello{42foo }}'")
