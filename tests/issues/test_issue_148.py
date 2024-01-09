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
Regression test for GitHub Issue #148
"""


def test_should_compare_dict_with_non_orderable_key_types():
    # given
    class Foo(object):
        def __eq__(self, other):
            return isinstance(other, Foo)

        def __hash__(self):
            return hash("Foo")

    class Bar(object):
        def __eq__(self, other):
            return isinstance(other, Bar)

        def __hash__(self):
            return hash("Bar")

    # when
    foo = Foo()
    bar = Bar()

    # then
    {foo: 0, bar: 1}.should.equal({foo: 0, bar: 1})


def test_should_compare_dict_with_enum_keys():
    try:
        from enum import Enum
    except ImportError:  # Python 2 environment
        # skip this test
        return

    # given
    class SomeEnum(Enum):
        A = 'A'
        B = 'B'

    # when & then
    {SomeEnum.A: 0, SomeEnum.B: 1}.should.equal({SomeEnum.A: 0, SomeEnum.B: 1})
