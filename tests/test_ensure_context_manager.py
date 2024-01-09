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

from sure import ensure, expects


def test_ensure_simple_assertion():
    """:func:`~sure.ensure` should capture :exc:`AssertionError` instances other than :exc:`Exception`"""

    def __test_something():
        # same calculated value
        name = "Hodor"
        with ensure("the return value actually looks like: {0}", name):
            expects(name).should.contain("whatever")

    # check if the test function raises the custom AssertionError
    expects(__test_something).when.called_with().should.throw(
        AssertionError, "the return value actually looks like: Hodor"
    )


def test_ensure_just_assertion_error():
    """:class:`~sure.ensure` should not capture :exc:`Exception` instances other than :exc:`AssertionError`"""

    def __test_something():
        # same calculated value
        with ensure("neverused"):
            raise Exception("This is not an AssertionError")

    # check if the test function does not override the original exception
    # if it is not an AssertionError exception
    expects(__test_something).when.called_with().should.throw(
        Exception, "This is not an AssertionError"
    )
