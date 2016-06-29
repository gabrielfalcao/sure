# -*- coding: utf-8 -*-

"""
Test custom assertions.
"""

from sure import expect, assertion, chain, chainproperty
from sure.magic import is_cpython


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


def test_custom_chain_method():
    "test extending sure with a custom chain method."

    class Response(object):
        def __init__(self, headers, return_code):
            self.headers = headers
            self.return_code = return_code


    @chain
    def header(self, header_name):
        expect(self.obj.headers).should.have.key(header_name)
        return self.obj.headers[header_name]


    # FIXME(TF): 'must' does not sound right in this method chain.
    #            it should rather be ...header("foo").which.equals("bar")
    #            however, which is an assertionproperty in AssertionBuilder
    #            and is not a monkey patched property.
    if is_cpython:
        Response({"foo": "bar", "bar": "foo"}, 200).should.have.header("foo").must.be.equal("bar")
    else:
        expect(expect(Response({"foo": "bar", "bar": "foo"}, 200)).should.have.header("foo")).must.be.equal("bar")


def test_custom_chain_property():
    "test extending sure with a custom chain property."

    class Response(object):
        magic = 41

    @chainproperty
    def having(self):
        return self

    @chainproperty
    def implement(self):
        return self


    @assertion
    def attribute(self, name):
        has_it = hasattr(self.obj, name)
        if self.negative:
            assert not has_it, "Expected was that object {0} does not have attribute {1}".format(
                self.obj, name)
        else:
            assert has_it, "Expected was that object {0} has attribute {1}".format(
                self.obj, name)

        return True


    expect(Response).having.attribute("magic")
    expect(Response).doesnt.implement.attribute("nomagic")
