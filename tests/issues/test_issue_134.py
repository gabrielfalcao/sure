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
Test fix of bug described in GitHub Issue #134.
"""

from sure import expect


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

    error_msg = "X is b'hello{42world }}' whereas Y is b'hello{42foo }}'"

    expect(__great_test_bytes).when.called.to.throw(AssertionError, error_msg)

    def __great_test_unicode():
        expect(u'hello{42world }}').should.be.equal(u'hello{42foo }}')

    error_msg = "X is 'hello{42world }}' whereas Y is 'hello{42foo }}'"

    expect(__great_test_unicode).when.called.to.throw(AssertionError, error_msg)
