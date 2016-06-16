# -*- coding: utf-8 -*-

"""
Test custom assertions.
"""

from sure import expect, assertion


def test_custom_assertion():
    "test extending sure with a custom assertion."

    class Response(object):
        def __init__(self, return_code):
            self.return_code = return_code


    @assertion
    def return_code(self, return_code):
        if self.negative:
            assert return_code != self.obj.return_code, "Expected was a return code different from {0}.".format(return_code)
        else:
            assert return_code == self.obj.return_code, "Expected return code is: {0}\nGiven return code was: {1}".format(
                return_code, self.obj.return_code)

        return True


    expect(Response(200)).should.have.return_code(200)
    expect(Response(200)).shouldnt.have.return_code(201)
