# -*- coding: utf-8 -*-

"""
Test fix of bug described in GitHub Issue #134.
"""

from sure import expect
from six import PY2


def test_issue_132():
    "Correctly handle {} characters in matcher string"

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

    def __great_test_bytes():
        expect(b'hello{42world }}').should.be.equal(b'hello{42foo }}')

    if PY2:
        error_msg = "X is 'hello{42world }}' whereas Y is 'hello{42foo }}'"
    else:
        error_msg = "X is b'hello{42world }}' whereas Y is b'hello{42foo }}'"

    expect(__great_test_bytes).when.called.to.throw(AssertionError, error_msg)

    def __great_test_unicode():
        expect(u'hello{42world }}').should.be.equal(u'hello{42foo }}')

    if PY2:
        error_msg = "X is u'hello{42world }}' whereas Y is u'hello{42foo }}'"
    else:
        error_msg = "X is 'hello{42world }}' whereas Y is 'hello{42foo }}'"

    expect(__great_test_unicode).when.called.to.throw(AssertionError, error_msg)
