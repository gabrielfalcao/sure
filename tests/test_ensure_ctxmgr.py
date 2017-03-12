# -*- coding: utf-8 -*-

import sure


def test_ensure_simple_assertion():
    """Test ensure simple assertion"""

    def __test_something():
        # same calculated value
        name = 'Hodor'
        with sure.ensure('the return value actually looks like: {0}', name):
            sure.expect(name).should.contain('whatever')


    # check if the test function raises the custom AssertionError
    sure.expect(__test_something).when.called_with().should.throw(AssertionError, \
                                                                  'the return value actually looks like: Hodor')


def test_ensure_just_assertion_error():
    """Test that ensure only captures AssertionErrors"""
    def __test_something():
        # same calculated value
        with sure.ensure('neverused'):
            raise Exception('This is not an AssertionError')


    # check if the test function does not override the original exception
    # if it is not an AssertionError exception
    sure.expect(__test_something).when.called_with().should.throw(Exception, \
                                                                  'This is not an AssertionError')
