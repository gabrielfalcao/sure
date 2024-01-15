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
