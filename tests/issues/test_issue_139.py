# -*- coding: utf-8 -*-

"""
Test fix of bug described in GitHub Issue #139.
"""

from sure import expect


def test_issue_139():
    "Test for GitHub Issue #139"
    # test with big epsilon
    expect(1.).should.equal(5., 4.)

    # shouldn't raise IndexError: tuple index out of range
    try:
        expect(1.).should.equal(5., 3.)
    except AssertionError:
        pass
    else:
        raise RuntimeError('should not be equal')
